from sqlalchemy import select, text, desc
from sqlalchemy.sql.elements import SQLCoreOperations

from app import db
from app.common.repositories.pagination_repository import PaginationRepository, PageableResult
from app.common.schemas.pager import SortType
from app.main.models.posts import Post


class PostRepository(PaginationRepository[Post]):
    @classmethod
    def get_all(
        cls,
        page: int,
        per_page: int,
        sort: SortType,
        value_filters: list[SQLCoreOperations],
    ) -> PageableResult[Post]:
        stmt = select(Post)

        if value_filters:
            stmt = stmt.filter(*value_filters)

        if sort is SortType.ASCENDING:
            stmt = stmt.order_by(Post.id)
        else:
            stmt = stmt.order_by(Post.id.desc())

        pageable_result = cls.paginate(statement=stmt, page=page, per_page=per_page)

        return pageable_result

    @classmethod
    def get(cls, record_id: int) -> Post:
        stmt = select(Post).where(Post.id == record_id)

        result = db.session.execute(stmt)

        return result.scalar()
