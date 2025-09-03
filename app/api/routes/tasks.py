import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_
from app.db.session import get_session
from app.api.deps import get_current_user
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut

router = APIRouter()

@router.post("", response_model=TaskOut, status_code=201)
async def create_task(
    payload: TaskCreate, 
    session: AsyncSession = Depends(get_session), 
    user: User = Depends(get_current_user)
):
    task = Task(
        title=payload.title, 
        description=payload.description, 
        status=payload.status, 
        user_id=user.id
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    
    return TaskOut.model_validate(task)

@router.get("", response_model=List[TaskOut])
async def list_tasks(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    conditions = [Task.user_id == user.id]
    if status_filter in {"pending", "completed"}:
        conditions.append(Task.status == status_filter)
    if search:
        like = f"%{search.lower()}%"
        conditions.append(or_(Task.title.ilike(like), Task.description.ilike(like)))
    stmt = select(Task).where(and_(*conditions)).order_by(Task.created_at.desc()).limit(limit).offset(offset)
    rows = (await session.execute(stmt)).scalars().all()
    return [TaskOut.model_validate(t.__dict__) for t in rows]

@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: uuid.UUID, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user.id)
    task = (await session.execute(stmt)).scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskOut.model_validate(task.__dict__)

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: uuid.UUID, payload: TaskUpdate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user.id)
    task = (await session.execute(stmt)).scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(task, k, v)
    await session.commit()
    await session.refresh(task)
    return TaskOut.model_validate(task.__dict__)

@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: uuid.UUID, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    stmt = delete(Task).where(Task.id == task_id, Task.user_id == user.id)
    result = await session.execute(stmt)
    await session.commit()
    if result.rowcount == 0:
        # To avoid leaking task ownership info, return 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return
