from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional
from . import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/", response_model=List[schemas.VoteOut])
def get_posts(db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user), 
                limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cr.execute(""" SELECT * FROM posts """)
    # posts = cr.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)):
    # print(post.published)         # print(post.rating)            # print(post.dict())

    # post_dict = post.dict()               # post_dict['id'] = randrange(0, 1000000)               # my_posts.append(post_dict)

    # cr.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,                 #     (post.title, post.content, post.published))                   # new_post = cr.fetchone()                  # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print("#############")
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.VoteOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)):
    # post = find_post(id)

    # cr.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))         # post = cr.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"id {id} does not exist"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)):
    # index = find_index(id)

    # cr.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))           # post = cr.fetchone()          # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="forbidden from performing requested ection")
    # my_posts.pop(index)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)):
    # cr.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))              # updated_post = cr.fetchone()              # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="forbidden from performing requested ection")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     # index = find_index(id)
#     cr.execute(""" UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING * """, (post.title, post.content, post.published, (id),))
#     updated_post = cr.fetchone()
#     conn.commit()
#     print(updated_post)
#     # if updated_post == None:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#     #                         detail=f"id {id} does not exist")
#     # post_dict = post.dict()
#     # post_dict['id'] = id
#     # my_posts[index] = post_dict
#     return {"updated": "updated_post"}
