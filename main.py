from enum import Enum
from typing import Dict
from typing import List
from typing import Optional

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Path
# main point of interaction with the app
from pydantic import BaseModel

app = FastAPI()


class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"


class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category


items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES),
}


# simple get request returning hello world
@app.get("/helloworld")
def helloworld():
    return {"message": "hello world"}


# get request that returns all items
@app.get("/items")
def query_all_items():
    return items


# get request that returns all items as a dictionary
@app.get("/")
def query_all_items() -> Dict[str, Dict[int, Item]]:
    return {"items": items}


# get request that returns an item based on item_id as a path parameter
@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        print(item_id)
        raise HTTPException(status_code=404, detail=f"Item with item id {item_id} does not exist")
    return items[item_id]


# get request that returns an item based on item_id as an optional path parameter
@app.get("/items/getitem/{item_id}")
def query_an_item_by_id(id: Optional[int] = None):
    if id:
        return items[id]
    return None


# get request that returns a list of items based on the object values as query parameters
@app.get("/items/")
def query_item_by_parameters(
        name: Optional[str] = None,
        price: Optional[float] = None,
        count: Optional[int] = None,
        category: Optional[Category] = None,
) -> Dict[str, List[Item]]:
    def check_item(item: Item):
        """Check if the item matches the query arguments from the outer scope."""
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count != count,
                category is None or item.category is category,
            )
        )

    selection = [item for item in items.values() if check_item(item)]

    if selection:
        return {"item": selection}

    raise HTTPException(status_code=404, detail=f"No items found with the specified parameters")


# post request that adds an item to the dictionary if it does not already exist
@app.post("/")
def add_item(item: Item) -> Dict[str, Item]:
    if item.id in items:
        raise HTTPException(status_code=400, detail=f"Item with item id {item.id} already exists")

    items[item.id] = item
    return {"added": item}


# put request that updates an item if it does already exist
@app.put("/update/{item_id}")
def update(
        item_id: int = Path(ge=1),
        name: Optional[str] = None,
        price: Optional[float] = None,
        count: Optional[int] = None,
        category: Optional[Category] = None,
) -> Dict[str, Item]:
    if item_id not in items:
        raise HTTPException(status_code=400, detail=f"Item with item id {item_id} does not exist")
    if all(info is None for info in (name, price, count, category)):
        raise HTTPException(status_code=400, detail="No parameters provided for update.")

    item = items[item_id]

    if name is not None:
        item.name = name
    if price is not None and price > 0:
        item.price = price
    if count is not None:
        item.count = count
    if category is not None:
        item.category = category
    return {"updated": item}


# delete request that removes an item from the dictionary if it does already exist
@app.delete("/{item_id")
def delete_item(item_id: int) -> Dict[str, Item]:
    if item_id not in items:
        raise HTTPException(status_code=400, detail="No parameters provided for update.")

    item = items.pop(item_id)
    return {"deleted": item}
