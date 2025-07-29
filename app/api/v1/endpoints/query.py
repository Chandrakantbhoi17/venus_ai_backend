from fastapi import APIRouter, Depends,UploadFile,File,Form
from fastapi.responses import JSONResponse
from app.utils.s3_util import upload_file_to_s3
from sqlalchemy.orm import Session
from app.services import query as query_service
from app.schemas.query import QueryCreate, QueryRead
from app.models.base import Base,get_db

from app.models.query import Query
router = APIRouter(prefix="/query", tags=["Query"])

@router.post("/", response_model=QueryRead)
def submit_query(query_data: QueryCreate, db: Session = Depends(get_db)):
    return query_service.create_query(db, query_data)

@router.get("/", response_model=list[QueryRead])
def list_queries(db: Session = Depends(get_db)):
    return query_service.get_all_queries(db)


@router.post("/upload/")
async def upload(query_id: int = Form(...), file: UploadFile = File(...),db: Session = Depends(get_db)):
    query = db.query(Query).filter(Query.id == query_id).first()
    if not query:
            return JSONResponse(status_code=404, content={"success": False, "error": "Query not found"})

    try:
        file_url = upload_file_to_s3(file, query_id)
        query.file_url = file_url
        db.commit()
        db.refresh(query)
        return {"success": True, "url": file_url}
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})