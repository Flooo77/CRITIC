from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session

from api.database import get_db
from .schemas import UserCreate, UserListing, UserStatusUpdate, LoginData
from .controller import create_user, get_all_users, get_user_by_id, update_user_status, authenticate_user, delete_user_session, require_session, get_local_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', response_model=UserCreate)
def user_create(user: UserCreate, 
                db: Session = Depends(get_db)
                ):
    db_user = create_user(db, user)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return db_user

@router.get('/', response_model=list[UserListing])
def users_get_all(request: Request, 
                  skip: int = 0, 
                  limit: int = 10, 
                  db: Session = Depends(get_db)
                  ):
    require_session(request, db)
    users = get_all_users(db, skip=skip, limit=limit)
    return users

@router.get('/{user_id}', response_model=UserListing)
def user_get(request: Request,
             user_id: int, 
             db: Session = Depends(get_db)
             ):
    require_session(request, db)
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put('/{user_id}/status', response_model=UserStatusUpdate)
def user_update_status(user_id: int, 
                       status_update: UserStatusUpdate, 
                       db: Session = Depends(get_db)
                       ):
    user = update_user_status(db, user_id, status_update.is_active)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get('/local/')
def user_get_local(request: Request,
                    db: Session = Depends(get_db)
                    ):
    require_session(request, db)
    user = get_local_user(db)
    if user is None:
        raise HTTPException(status_code=404, detail="Local user not found")
    return user

@router.post('/login/')
def user_login(login_data: LoginData,
               db: Session = Depends(get_db)
               ):
    auth = authenticate_user(db, login_data.username, login_data.password)
    return auth

@router.post('/logout/')
def user_logout(request: Request,
                db: Session = Depends(get_db)
                ):
    require_session(request, db)
    try:
        delete_user_session(request.cookies.get('session'), db)
    except:
        raise HTTPException(status_code=400, detail="Logout failed")
    return {"detail": "Logout successful"}