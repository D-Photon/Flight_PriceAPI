# Import libraries

import sys, os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
import uvicorn 
import requests
from pydantic import BaseModel


model_path = 'flght_price_lgb_model.pkl'
FEEDBACK_file = 'Incoming_data.csv'
API_KEY = os.getenv("api_key")

if not os.path.exists(model_path):
    sys.exit(
        f"'{model_path}' not found Path not found in this folder\n"
        "Run flight_price_prediction.py (or the notebook) first to train"
        "and save the model, then re-run this script"
        )

model = joblib.load(model_path)

app = FastAPI(title= "Flight Prie Prediction API")

def get_INR_to_NGN():
    try:
        response = requests.get(url=f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/INR",
                                timeout=3)
        response.raise_for_status()
        return float(response.json()["rates"]["NGN"])

    except Exception as e:
        print(f"Could not fetch live rate ({e}) using fallback rate")
        return 18.50

class FlightInput(BaseModel):
    airline:str
    from_city: str 
    to_city: str
    travel_class: str
    stop:str
    day_of_week:str
    arrival_time:str
    depature_time:str
    duration_minutes:float
    days_left:int
    actual_price:Optional[float]=None

@app.get('/')
def health_check():
    return {"status": "ok", "message": "Flight Price Prediction API is running"}

@app.post('/predict')
def predict(data:FlightInput):
    Input_dict = {
        'airline':[data.airline],
        'from':[data.from_city],
        'to':[data.to_city],
        'Class':[data.travel_class],
        'stop':[data.stop],
        'day_of_week':[data.day_of_week],
        'arrival_time':[data.arrival_time],
        'depature_time':[data.depature_time],
        'duration_minutes':[data.duration_minutes],
        'days_left':[data.days_left]
    }

    df_input = pd.DataFrame(Input_dict)

    try:
        predicted_inr = float(model.predict(df_input)[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not score this input: {e}")

    ngn_rate = get_INR_to_NGN()
    predicted_ngn = round(predicted_inr * ngn_rate, 2)

    # Log the request into a csv file
    log_dict = Input_dict.copy()

    log_dict['predicted_price_inr'] = [predicted_inr]
    log_dict['exchange_rate'] = [ngn_rate]
    log_dict['predicted_price_ngn'] = [predicted_ngn]
    log_dict['actual_price'] = [data.actual_price]

    pd.DataFrame(log_dict).to_csv(
        FEEDBACK_file, mode='a',
        header=not os.path.exists(FEEDBACK_file), index=False,
    )

    return {
        "predicted_price_inr" : f"{predicted_inr:.2f} Indian Rupies",
        "exchange_rate" : f"1 INR = {ngn_rate:.2f} NGN",
        "predicted_price_ngn" : f"{predicted_ngn:.2f} NGN",
        "status" : "Logged Successfully",
    }

if __name__=='__main__':
    print(f"Loaded Model '{model_path}'.")
    print("Starting FAstAPI server on http://127.0.0.1:8000 (docs at /docs) ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
