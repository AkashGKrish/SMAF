from typing import List, Optional
from fastapi import Body, FastAPI, Response ,status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from .. import model, schemas, oauth2
from .. database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags= ['Posts'])

# @router.get("/",response_model=List[schemas.PostOut])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit:int=10, skip: int=0, search: Optional[str]= ""):
    
    # posts =  db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
        model.Vote,model.Vote.post_id == model.Post.id, isouter= True).group_by(model.Post.id).filter(
        model.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

#   With SQL query
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print (posts)
#     return{"data": posts}


@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id : int, response : Response, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_post =  db.query(model.Post).filter(model.Post.id == id).first()
    post = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
        model.Vote,model.Vote.post_id == model.Post.id, isouter= True).group_by(model.Post.id).filter(
        model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"post with {str(id)} id was not found.")
    if post_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform this action")

    return post

#   With SQL query
# def get_post(id : int, response : Response):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
#     post = cursor.fetchone()
#     return{"data":post}

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostRespose)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = model.Post(title = post.title, content = post.content, published = post.published)
    # print(current_user.id)
    new_post = model.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#   With SQL query
# def create_posts(post: Post):
#     cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *""",
#                    (post.title,post.content,post.published))
#     new_post =cursor.fetchone()
#     conn.commit()
#     return{"data":new_post}


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query =  db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with {id} do not exist ")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform this action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# With SQL
# def delete_post(id):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
#     deleted_post = cursor.fetchone( )
#     conn.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model= schemas.PostRespose)
def update_post(id : int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with {id} do not exist ")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform this action")
    post_query. update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

# With SQL Query
# def update_post(id : int, post: Post):
#     cursor.execute("""UPDATE  posts SET title = %s, content = %s WHERE id = %s RETURNING *""",
#                    (post.title, post.content,str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()  