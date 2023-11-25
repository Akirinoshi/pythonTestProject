from enum import Enum

from pydantic import BaseModel, PositiveInt


class SortType(str, Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class SortablePager(BaseModel):
    page: PositiveInt = 1
    per_page: PositiveInt = 15
    sort: SortType = SortType.ASCENDING
