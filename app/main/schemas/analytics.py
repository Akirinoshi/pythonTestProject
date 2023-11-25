from datetime import date

from pydantic.main import BaseModel


class AnalyticsLikeQuery(BaseModel):
    date_from: date
    date_to: date
