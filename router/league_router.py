from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.league_service import find_game_by_id, find_league
from database import get_db

router = APIRouter()

@router.get("/games/{game_id}")
def read_game(game_id: str, db: Session = Depends(get_db)):
    try:
        game = find_game_by_id(db, game_id)
        return game
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/league")
def get_game(db: Session = Depends(get_db)):
    try:
        game = find_league(db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))        

