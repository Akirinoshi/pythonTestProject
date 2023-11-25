from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, root_validator

from app.common.schemas.pager import SortablePager
from app.common.utils.create_filter_model import create_filter_model_with_limits


class PostValueFilters(BaseModel):
    id: Optional[int]
    user_id: Optional[int]


PostValueFilters = create_filter_model_with_limits(
    PostValueFilters
)


class PostQuery(PostValueFilters):
    pager: SortablePager = SortablePager()
    value_filters: Optional[PostValueFilters]

    @root_validator(pre=True)
    def set_pager_and_filters(cls, values: dict) -> dict:
        pager_params = {}
        value_filter_params = {}

        for param, value in values.items():
            if param in SortablePager.__fields__:
                pager_params[param] = value

            elif param in PostValueFilters.__fields__:
                value_filter_params[param] = value

        result = {}

        if pager_params:
            result["pager"] = pager_params

        if value_filter_params:
            result["value_filters"] = value_filter_params

        return result


class PostPutModel(BaseModel):
    content: str


class PostCreateModel(BaseModel):
    content: str


class PostAssessModel(BaseModel):
    post_id: int
    like: bool
