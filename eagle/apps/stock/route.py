from eagle.workers.stock import tasks
from fastapi import APIRouter

from .resource import Stock

router = APIRouter(
    prefix="/stock",
)


@router.get("/get_data/{date_str}")
async def get_stock_data(date_str: str):
    stock_data = Stock().list(filters={'trade_date': date_str})
    return {"data": stock_data}


@router.put("/sync_data/{date_str}")
async def sync_stock_data(date_str: str):
    tasks.get_top_list(date_str)
    return {"date": date_str}
