from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["Точка работы с задачами"])


@router.get("/")
async def get_all_items():
    return {"action": "Fetching data of all items"}


@router.get("/{id}")
async def get_item_data(id: int):
    return {"action": "Get data of specified item"}
