from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from . import models
from .database import en_async, get_db

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup():
    async with en_async.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

async def get_summary_data(db: AsyncSession):
    # More efficient queries
    refill_count_result = await db.execute(select(func.count(models.Margarita.id)))
    refill_count = refill_count_result.scalar_one()

    total_refill_cost_result = await db.execute(select(func.sum(models.Margarita.price)))
    total_refill_cost = total_refill_cost_result.scalar_one_or_none() or 0

    initial_cup_cost = 28.0
    non_refill_price = 28.0  # Using $28 to calculate savings against a non-refill purchase

    total_spent = initial_cup_cost + total_refill_cost
    drinks_count = refill_count + 1  # Add 1 for the initial drink
    cost_per_drink = total_spent / drinks_count if drinks_count > 0 else 0
    savings = (non_refill_price * drinks_count) - total_spent

    return {
        "refill_count": refill_count,
        "total_spent": total_spent,
        "cost_per_drink": cost_per_drink,
        "savings": savings,
        "break_even": savings > non_refill_price,
    }

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: AsyncSession = Depends(get_db)):
    summary_data = await get_summary_data(db)
    return templates.TemplateResponse("index.html", {"request": request, **summary_data})

@app.get("/refill", response_class=HTMLResponse)
async def get_refill_partial(request: Request, db: AsyncSession = Depends(get_db)):
    summary_data = await get_summary_data(db)
    return templates.TemplateResponse("partials/cards.html", {"request": request, **summary_data})

@app.post("/add_margarita", response_class=HTMLResponse)
async def add_margarita(request: Request, db: AsyncSession = Depends(get_db)):
    new_margarita = models.Margarita(price=24.0)
    db.add(new_margarita)
    await db.commit()
    
    # Return the updated cards partial
    summary_data = await get_summary_data(db)
    return templates.TemplateResponse("partials/cards.html", {"request": request, **summary_data})
