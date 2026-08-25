from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    def __init__(self, model):
        self.model = model

    def create(
        self,
        db: Session,
        obj: ModelType,
    ) -> ModelType:

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    def get_by_id(
        self,
        db: Session,
        obj_id,
    ) -> ModelType | None:

        statement = select(self.model).where(
            self.model.id == obj_id
        )

        return db.scalar(statement)

    def get_all(
        self,
        db: Session,
    ) -> list[ModelType]:

        statement = select(self.model)

        return list(db.scalars(statement).all())

    def update(
        self,
        db: Session,
        obj: ModelType,
    ) -> ModelType:

        db.commit()
        db.refresh(obj)

        return obj