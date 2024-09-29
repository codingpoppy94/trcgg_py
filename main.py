from fastapi import FastAPI, APIRouter, Depends, HTTPException
from service import LeagueService
from pydantic import BaseModel

import parse

app = FastAPI()  # FastAPI 인스턴스 생성

ls = LeagueService()

class Replay(BaseModel):
    file_url: str
    file_name: str
    create_user: str
    
class Mapping(BaseModel):
    sub_name: str
    main_name: str
    
# 전적 조회에 필요한 서비스들
@app.get("/league/getAllRecord/{riot_name}")
async def get_all_record(riot_name: str):
    try:
        data = {
            "record_data": ls.get_record(riot_name),
            "month_data": ls.get_record_month(riot_name),
            "recent_data": ls.get_top_ten(riot_name),
            "with_team_data": ls.get_record_with_team(riot_name),
            "other_team_data": ls.get_record_other_team(riot_name),
            "most_pick_data": ls.get_most_pick(riot_name)
        }
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

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
    
@app.get("/league/getMappingName")
async def get_mapping_name():
    try:
        result = ls.get_mapping_name()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))    
    
# Post =====================

# 리플레이 저장
@app.post("/league/parse", status_code=200)
async def replay_parse(data: Replay):
    try:
        return parse.save(data.file_url, data.file_name, data.create_user)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# 부캐 저장
@app.post("/league/mapping", status_code=200)
async def replay_parse(data: Mapping):
    try:
        return ls.save_mapping_name(data.sub_name, data.main_name)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# PUT =====================

# 탈퇴 - 리그 정보
@app.put("/league/deleteYn", status_code=200)
async def put_league_delete_yn(delete_yn: str, riot_name: str):
    try:
        return ls.update_delete_yn(delete_yn, riot_name)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 탈퇴 - 부캐 닉네임
@app.put("/league/mapping/deleteYn", status_code=200)
async def put_mapping_delete_yn(delete_yn: str, riot_name: str):
    try:
        return ls.update_mapping_delete_yn(delete_yn, riot_name)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 닉변 - 리그 정보 
@app.put("/league/riotName", status_code=200)
async def put_league_riot_name(new_name: str, old_name: str):
    try:
        return ls.update_riot_name(new_name, old_name)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 닉변 - 부캐 닉네임
@app.put("/league/mapping/riotName", status_code=200)
async def put_mapping_riot_name(new_name: str, old_name: str):
    try:
        return ls.update_mapping_riot_name(new_name, old_name)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 리플 삭제
@app.delete("/league/game", status_code=200)
async def delete_league_by_game_id(game_id: str):
    try:
        return ls.delete_league_by_game_id(game_id)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# DELETE =====================

# 부캐 삭제
@app.delete("/league/mapping/subName", status_code=200)
async def delete_mapping_sub_name(riot_name: str):
    try:
        return ls.delete_mapping_sub_name(riot_name)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))