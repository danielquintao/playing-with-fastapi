from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional
import random

app = FastAPI()


# Eletric Capacity model
class EletricCapacity(SQLModel, table=True):
    __tablename__ = "eleccap"
    index: Optional[int] = Field(default=None, primary_key=True)
    country: str
    tech: str
    grid_conn_type: str
    year: int | None = None
    capacity: float | None = None


# SQLite connection
engine = create_engine("sqlite:///data/world_eletric_cap.db", echo=True)

# ------------------------------------------------------------------------------
# CREATE
# ------------------------------------------------------------------------------

# consumes JSON with a country, technology, grid type, year and 
# capacity on MW normalized by country area
# NOTE: error if the (country, tech, grid type, year) combination already exists
@app.post("/", response_model=EletricCapacity)
async def create(item: EletricCapacity):
    if item.year is None or item.capacity is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="missing year or capacity")
    # STUB #
    item.index = random.choice(range(10000, 100000))  # small chance of conflict, just for demonstration
    ########
    with Session(engine) as session:
        statement = select(EletricCapacity).where(
            EletricCapacity.country == item.country,
            EletricCapacity.tech == item.tech,
            EletricCapacity.grid_conn_type == item.grid_conn_type,
            EletricCapacity.year == item.year
        )
        ecs = session.exec(statement).all()
        if len(ecs) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="an item with given (country, tech, grid type, year) combination already exists"
            )
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

# ------------------------------------------------------------------------------
# READ
# ------------------------------------------------------------------------------

# per country, technology, grid type or any non-empty combination of them
# NOTE: error if the (country, tech, grid type) combination absent from DB
@app.get("/", response_model=list[EletricCapacity])
async def read(country: str, tech: str, grid_conn_type: str):
    with Session(engine) as session:
        statement = select(EletricCapacity).where(
            EletricCapacity.country == country,
            EletricCapacity.tech == tech,
            EletricCapacity.grid_conn_type == grid_conn_type
        )
        ecs = session.exec(statement).all()
        return ecs
