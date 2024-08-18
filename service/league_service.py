# from sqlalchemy.orm import Session
# from repository.league_repository import get_game_by_id, get_league

# def find_game_by_id(db: Session, game_id: str):
#     game = get_game_by_id(db, game_id)
#     if not game:
#         raise ValueError("Game not found")
#     return game

# def find_league(db: Session):
#     game = get_league(db)
#     if not game:
#         raise ValueError("not found data")
#     return game
