from fastapi import FastAPI, APIRouter, Depends, HTTPException
from service import LeagueService

import parse

app = FastAPI()  # FastAPI 인스턴스 생성

ls = LeagueService()

# 전체전적조회
@app.get("/league/getRecord/{riot_name}")
async def get_record(riot_name: str):
    try:
        game = ls.get_record(riot_name)
        return game
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# 최근한달조회
@app.get("/league/getRecordMonth/{riot_name}")
async def get_record_month(riot_name: str):
    try:
        game = ls.get_record_month(riot_name)
        return game
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 모스트픽
@app.get("/league/getMostPick/{riot_name}")
async def get_most_pick(riot_name: str):
    try:
        game = ls.get_most_pick(riot_name)
        return game
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 최근 두 달간 같은 팀 시너지
@app.get("/league/getRecordWithTeam/{riot_name}")
async def get_record_with_team(riot_name: str):
    try:
        game = ls.get_record_with_team(riot_name)
        return game
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 나와 인간상성 찾기
@app.get("/league/getRecordOtherTeam/{riot_name}")
async def get_record_other_team(riot_name: str):
    try:
        game = ls.get_record_other_team(riot_name)
        return game
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# 특정 챔프 장인 조회
@app.get("/league/master/{champ_name}")
async def get_champ_master(champ_name: str):
    try:
        master_info = ls.get_champ_master(champ_name)
        return master_info
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 특정 연도, 월의 챔프 통계 조회
@app.get("/league/champStats/{year}/{month}")
async def get_champ_stats(year: int, month: int):
    try:
        champ_stats = ls.get_champ_stats(year, month)
        return champ_stats
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 특정 연도, 월의 게임 통계 조회
@app.get("/league/gameStats/{year}/{month}")
async def get_game_stats(year: int, month: int):
    try:
        game_stats = ls.get_game_stats(year, month)
        return game_stats
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 라인별 승률 조회
@app.get("/league/lineStats/{position}")
async def get_record_line(position: str):
    try:
        line_stats = ls.get_record_line(position)
        return line_stats
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 게임 결과 조회 (game_id로)
@app.get("/league/gameResult/{game_id}")
async def get_record_game_id(game_id: str):
    try:
        game_result = ls.get_record_game_id(game_id)
        return game_result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 최근 Top 10 게임 조회
@app.get("/league/getTopTen/{riot_name}")
async def get_top_ten(riot_name: str):
    try:
        game = ls.get_top_ten(riot_name)
        return game
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# Post

# 리플레이 파싱 api 
@app.post("/league/parse", status_code=201)
async def replay_parse(file_url: str, file_name: str, create_user: str):
    try:
        return parse.save(file_url, file_name, create_user)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))