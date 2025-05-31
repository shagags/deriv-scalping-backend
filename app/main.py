# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import uvicorn

from utils import generate_signal_from_csv

app = FastAPI(title="Deriv Scalping Strategy API")

class SignalRequest(BaseModel):
    # Optional: Add parameters like 'symbol' or 'timeframe' if needed
    pass

class SignalResponse(BaseModel):
    signal: str
    explanation: str

@app.get("/")
def root():
    return {"message": "Deriv Scalping Strategy API is running!"}

@app.get("/signal", response_model=SignalResponse)
def get_signal():
    """
    Fetch the latest 1-minute OHLC data from your source (e.g., CSV, database, or API),
    run the scalping logic, and return a signal.
    """
    try:
        # For demonstration, load the latest CSV stored in /app/data/latest.csv
        df = pd.read_csv("data/latest.csv")  # Ensure you upload or sync this file
        sig, explanation = generate_signal_from_csv(df)
        return {"signal": sig, "explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating signal: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
