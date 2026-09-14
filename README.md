# Flight Price Prediction API

A machine learning-powered REST API built with FastAPI that predicts flight ticket prices and converts them into Nigerian Naira (NGN) using live exchange rates.

## Features
- **Machine Learning Pipeline:** Uses a trained LightGBM regressor to predict ticket prices based on flight duration, stops, airline, and days left.
- **Live Currency Conversion:** Fetches real-time exchange rates (INR to NGN) using the ExchangeRate-API.
- **Logging System:** Automatically logs incoming predictions and feedback data to `Incoming_data.csv`.
- **Interactive Documentation:** Built-in Swagger UI via FastAPI.

## Project Structure
- `flight_price_api.py` - Main FastAPI application script.
- `flght_price_lgb_model.pkl` - Trained LightGBM model pipeline.
- `requirements.txt` - Python project dependencies.
- `.env` - Environment variables configuration (API keys).

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/D-Photon/Flight_Price_Prediction.git)
   cd Flight_Price_Prediction