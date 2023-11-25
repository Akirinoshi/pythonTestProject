import math
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, TypedDict

from sqlalchemy import func, select

from app import db

T = TypeVar("T")


class PageableResultDict(TypedDict):
    page: int
    per_page: int
    total_pages: int
    total_items: int
    prev_page: Optional[int]
    next_page: Optional[int]
    result: list[T]


@dataclass
class PageableResult(Generic[T]):
    page: int
    total_pages: int
    total_items: int
    prev_page: Optional[int]
    next_page: Optional[int]
    per_page: int
    result: list[T]

    def to_dict(self, excluded_columns: list[str] = None) -> PageableResultDict[T]:
        dict_result = []
        for model in self.result:
            model_dict = model.to_dict()
            if excluded_columns:
                for column in excluded_columns:
                    model_dict.pop(column, None)
            dict_result.append(model_dict)

        return {
            "page": self.page,
            "total_pages": self.total_pages,
            "total_items": self.total_items,
            "prev_page": self.prev_page,
            "next_page": self.next_page,
            "per_page": self.per_page,
            "result": dict_result
        }


class PaginationRepository(Generic[T]):

    @classmethod
    def paginate(cls, statement, page: int = 1, per_page: int = 10) -> PageableResult[T]:
        """
        Paginate the given query.

        :param statement: SQLAlchemy's statement object.
        :param page: Page number.
        :param per_page: Number of items per page.
        :return: A tuple containing the items for the current page and the total number of items.
        """
        offset = (page - 1) * per_page

        paged_stmt = statement.offset(offset).limit(per_page)

        result = db.session.execute(paged_stmt)

        total_items = cls.get_total_items(statement)
        total_pages = cls.get_total_pages(total_items=total_items, per_page=per_page)

        prev_page = None if page == 1 else page - 1
        next_page = None if total_pages == page else page + 1
            
        pageable_result = PageableResult(
            page=page,
            total_pages=total_pages,
            total_items=total_items,
            prev_page=prev_page,
            next_page=next_page,
            per_page=per_page,
            result=result.scalars().all()
        )
        
        return pageable_result

    @staticmethod
    def get_total_items(statement) -> int:
        """
        Calculate the total number of items based on a given query.

        :param statement: SQLAlchemy's statement object.
        :return: Total number of pages.
        """
        statement = select(func.count()).select_from(statement.alias())
        result = db.session.execute(statement)
        return result.scalar()

    @staticmethod
    def get_total_pages(total_items: int, per_page=10) -> int:
        total_pages = math.ceil(total_items / per_page)

        if total_pages:
            return total_pages

        return 1
