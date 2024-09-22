from fastapi import FastAPI
# from router import league_router  # 라우터 파일을 가져옵니다.
# import repository.league_repository
from database import Database

app = FastAPI()  # FastAPI 인스턴스 생성
# app.include_router(league_router.router)  # 라우터를 앱에 포함
db=Database()
db.connect()
print(db.findRecordByGameId("testtest"))
# params = [
#      {
#         'game_id': 'testtest',
#         'riot_name': 'Player1',
#         'champ_name': 'Champ1',
#         'position': 'TOP',
#         'kill': 5,
#         'death': 2,
#         'assist': 3,
#         'game_result': '승',
#         'game_team': 'TeamA',
#         'game_date': '2024-08-18',
#         'delete_yn': 'N',
#         'create_user': 'user1',
#         'gold': 3000,
#         'ccing': 10,
#         'time_played': 35,
#         'total_damage_champions': 20000,
#         'total_damage_taken': 10000,
#         'vision_score': 15,
#         'vision_bought': 5
#     },
# ]
# db.insertLeague(params)
# sub_name = 'example_sub_name'
# main_name = 'example_main_name'
# db.insertMappingName(sub_name, main_name)
print(db.deleteMappingSubName('example_sub_name'))
# print(db.)
db.close()