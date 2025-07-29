from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from backend import models,database
from  backend.database import engine, get_db
from datetime import date

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🟢 Home route
@app.get("/deadlines")
def read_root():
    return {"message": "Welcome to Deadline Manager!"}

# 🟢 Get all deadlines
@app.get("/deadlines/")
def get_deadlines(db: Session = Depends(get_db)):
    return db.query(models.Deadline).all()

# 🟢 Add a deadline
@app.post("/deadlines/")
def add_deadline(deadline: models.DeadlineCreate, db: Session = Depends(get_db)):
    db_deadline = models.Deadline(**deadline.dict())
    db.add(db_deadline)
    db.commit()
    db.refresh(db_deadline)
    return db_deadline

# 🟢 Delete a deadline
@app.delete("/deadlines/{deadline_id}")
def delete_deadline(deadline_id: int, db: Session = Depends(get_db)):
    deadline = db.query(models.Deadline).filter(models.Deadline.id == deadline_id).first()
    if not deadline:
        raise HTTPException(status_code=404, detail="Deadline not found")
    db.delete(deadline)
    db.commit()
    return {"message": "Deadline deleted"}

# 🟢 ✅ Update a deadline
@app.put("/deadlines/{deadline_id}")
def update_deadline(deadline_id: int, new_data: dict = Body(...), db: Session = Depends(get_db)):
    deadline = db.query(models.Deadline).filter(models.Deadline.id == deadline_id).first()
    if not deadline:
        raise HTTPException(status_code=404, detail="Deadline not found")

    # Update only if provided
    deadline.title = new_data.get("title", deadline.title)
    deadline.due_date = new_data.get("due_date", deadline.due_date)
    deadline.description = new_data.get("description", deadline.description)

    db.commit()
    return {"message": "Deadline updated successfully"}

@app.get("/due-today")
def get_today_deadlines():
    db = database.SessionLocal()
    today = date.today()
    deadlines = db.query(models.Deadline).filter(models.Deadline.due_date == today).all()
    return deadlines
