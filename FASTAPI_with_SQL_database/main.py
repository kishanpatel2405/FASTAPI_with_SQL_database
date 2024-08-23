from fastapi import FastAPI, Depends, HTTPException
from models import Base, User
from schemas import UserSchema
from database import SessionLocal, engine
from sqlalchemy.orm import session, Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def home():
    return {"message": "my first fastapi app"}

@app.post("/adduser")
async def add_user(request: UserSchema, db: Session = Depends(get_db)):
    user = User(name=request.name, email=request.email, nickname=request.nickname)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"detail": "User Add successfully"}


@app.get("/user/{user_id}")
async def get_user(user_name, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.name == user_name).all()
    return {"detail": "User get successfully"}


@app.put("/user/{user_id}")
async def update_user(user_id: int, request: UserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = request.name
    user.email = request.email
    user.nickname = request.nickname

    db.commit()
    db.refresh(user)
    return {'detail': 'User Update successfully'}


@app.delete("/user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}
