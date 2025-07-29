from sqlalchemy.orm import Session
from app.models.query import Query
from app.schemas.query import QueryCreate

def create_query(db: Session, query_data: QueryCreate):
    new_query = Query(
        name=query_data.name,
        email=query_data.email,
        user_input=query_data.user_input,
    )
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query

def get_all_queries(db: Session):
    return db.query(Query).all()
