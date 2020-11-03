import datetime
from typing import Dict, List

from app.schemas.rates import RateBase
from fastapi import APIRouter, HTTPException, Body

from app.models.rates import Rate

from app.schemas.rates import RateCalculateOut, RateCalculateIn, rate_example_schema

router = APIRouter()


@router.post(
    '/',
    response_model=Dict[datetime.date, List[RateBase]],
)
async def create_rates(
        rates: Dict[datetime.date, List[RateBase]] = Body(
            ...,
            example=rate_example_schema
        )
):
    """
    Skips rates that already exist

    **Returns added rates**
    """
    print(rates)
    rates_dict = dict()

    for date in rates.keys():
        for rate in rates[date]:
            if not await Rate.filter(date=date, cargo_type=rate.cargo_type).first():
                await Rate.create(date=date, **rate.dict())
                if date in rates_dict.keys():
                    rates_dict[date].append(rate)
                else:
                    rates_dict[date] = [rate]

    return rates_dict


@router.get(
    '/',
    response_model=Dict[datetime.date, List[RateBase]],
)
async def get_rates():
    """
    **Returns all created rates**
    """
    dates = await Rate.all().distinct().values_list("date", flat=True)

    rates_dict = {}

    for date in dates:
        rates = await Rate.filter(date=date)
        rates_dict[date] = []

        for rate in rates:
            rates_dict[date].append(RateBase(cargo_type=rate.cargo_type, rate=rate.rate))

    return rates_dict


@router.put(
    '/',
    response_model=Dict[datetime.date, List[RateBase]],
)
async def update_rates(
        rates: Dict[datetime.date, List[RateBase]] = Body(
            ...,
            example=rate_example_schema
        )
):
    """
    Updates rate coefficients in created rates, searched by date and cargo type

    **Returns updated rates**
    """
    rates_dict = {}

    for date in rates.keys():
        for rate in rates[date]:
            if rate_in_db := await Rate.filter(date=date, cargo_type=rate.cargo_type).first():
                if rate_in_db.rate != rate.rate:
                    await Rate.filter(id=rate_in_db.id).update(rate=rate.rate)

                    if date in rates_dict.keys():
                        rates_dict[date].append(RateBase(cargo_type=rate.cargo_type, rate=rate.rate))
                    else:
                        rates_dict[date] = [RateBase(cargo_type=rate.cargo_type, rate=rate.rate)]

    return rates_dict


@router.delete(
    '/',
    response_model=Dict[datetime.date, List[RateBase]],
)
async def delete_rates(
        rates: Dict[datetime.date, List[RateBase]] = Body(
            ...,
            example=rate_example_schema
        )
):
    """
    Deletes created rates

    **Returns deleted rates**
    """
    rates_dict = {}

    for date in rates.keys():
        for rate in rates[date]:
            if rate_in_db := await Rate.filter(date=date, cargo_type=rate.cargo_type).first():
                if date in rates_dict.keys():
                    rates_dict[date].append(RateBase(cargo_type=rate.cargo_type, rate=rate.rate))
                else:
                    rates_dict[date] = [RateBase(cargo_type=rate.cargo_type, rate=rate.rate)]

                await rate_in_db.delete()

    return rates_dict


@router.post(
    '/calculate',
    response_model=RateCalculateOut
)
async def calculate_rate(data: RateCalculateIn):
    """
    Calculates insurance price using rates by data and cargo type

    **Returns data, cargo type and calculated price**
    """
    if rate := await Rate.filter(date=data.date, cargo_type=data.cargo_type).first():
        return RateCalculateOut(**data.dict(), calculated_price=rate.rate * data.price)
    else:
        raise HTTPException(400, 'Rate not found')
