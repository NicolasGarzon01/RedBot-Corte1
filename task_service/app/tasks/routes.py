from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from .. import models, schemas, database
from .dependencies import get_current_user_id

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db), current_user_id: str = Depends(get_current_user_id)):
    # validación: verificar que la cuenta pertenece al usuario
    account = db.execute(
        text("SELECT * FROM accounts WHERE id = :id AND user_id = :uid"),
        {"id": task.account_id, "uid": current_user_id}
    ).fetchone()
    if not account:
        raise HTTPException(status_code=403, detail="Not allowed")

    new_task = models.Task(account_id=task.account_id, type=task.type, config_json=task.config_json)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=list[schemas.Task])
def list_tasks(db: Session = Depends(database.get_db), current_user_id: str = Depends(get_current_user_id)):
    tasks = db.execute(text("""
        SELECT t.* FROM tasks t
        JOIN accounts a ON t.account_id = a.id
        WHERE a.user_id = :uid
    """), {"uid": current_user_id}).fetchall()
    return tasks

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_db), current_user_id: str = Depends(get_current_user_id)):
    task = db.execute(text("""
        SELECT t.* FROM tasks t
        JOIN accounts a ON t.account_id = a.id
        WHERE t.id = :tid AND a.user_id = :uid
    """), {"tid": task_id, "uid": current_user_id}).fetchone()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.execute("DELETE FROM tasks WHERE id = :tid", {"tid": task_id})
    db.commit()
    return {"detail": "Task deleted"}
