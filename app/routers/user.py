from fastapi import Body, FastAPI, Response ,status, HTTPException, Depends, APIRouter
from .. import model, schemas, utils
from .. database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags= ['Users']
)

@router.post("/", status_code= status.HTTP_201_CREATED,response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db) ):
    
    # hash the password
    user.password = utils.hash(user.password)

    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id : int, db:Session = Depends(get_db)):
    user =  db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"user with {str(id)} id was not found.")
    return user
