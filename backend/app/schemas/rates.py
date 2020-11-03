import datetime

from pydantic import BaseModel

rate_example_schema = \
    {
        "2020-06-01": [
            {
                "cargo_type": "Glass",
                "rate": "0.04"
            },
            {
                "cargo_type": "Other",
                "rate": "0.01"
            }
        ],
        "2020-07-01": [
            {
                "cargo_type": "Glass",
                "rate": "0.035"
            },
            {
                "cargo_type": "Other",
                "rate": "0.015"
            }
        ]
    }


class RateBase(BaseModel):
    cargo_type: str
    rate: float


class RateCalculateIn(BaseModel):
    date: datetime.date
    cargo_type: str
    price: float


class RateCalculateOut(BaseModel):
    date: datetime.date
    cargo_type: str
    calculated_price: float
