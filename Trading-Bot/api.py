from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from Bot.client import get_client
from Bot.orders import place_order, get_futures_balance
import os

app = FastAPI(title="Binance Trading Bot API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrderRequest(BaseModel):
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None

@app.get("/balance")
async def fetch_balance():
    try:
        client = get_client()
        balance = get_futures_balance(client)
        if not balance:
            raise HTTPException(status_code=404, detail="USDT balance not found")
        return balance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/order")
async def execute_order(request: OrderRequest):
    try:
        client = get_client()
        order = place_order(
            client,
            request.symbol,
            request.side,
            request.order_type,
            request.quantity,
            request.price,
            request.stop_price
        )
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/logs")
async def get_logs():
    try:
        log_path = "logs/trading.log"
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                logs = f.readlines()
            # Return last 50 lines
            return logs[-50:]
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
