from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud, database, models
from .dependencies import get_current_user_id, ensure_account_owner

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/", response_model=schemas.Account)
def create_account(
    account: schemas.AccountCreate,
    db: Session = Depends(database.get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    account_data = schemas.AccountCreate(
        user_id=current_user_id,
        platform=account.platform,
        handle=account.handle,
        token=account.token,
    )
    return crud.create_account(db, account_data)


@router.get("/", response_model=list[schemas.Account])
def get_my_accounts(
    db: Session = Depends(database.get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    return crud.get_accounts(db, current_user_id)


@router.delete("/{account_id}", response_model=schemas.Account)
def delete_account(
    account: models.Account = Depends(ensure_account_owner),
    db: Session = Depends(database.get_db),
):
    db.delete(account)
    db.commit()
    return account
