from fastapi import APIRouter, HTTPException
from core.setting import Rate
from repositories.reviews import ReviewsRepositories
from schemas.new_review import ReviewSchema
rt = APIRouter()

@rt.post("/taxi_api/reviews/add")
def add_review(schem: ReviewSchema):
    try:
        new_rev = ReviewsRepositories()
        new_rev.add_review(username=schem.username, driver_name=schem.driver_name,
                           rate=schem.rate, text=schem.text)
        return "Review has been added"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

