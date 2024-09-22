# from datetime import datetime
# import json
# import parse
# import database as du

# def set_data(stats_array, file_name, create_user):
#     # print('set 시작')
#     current_year = datetime.now().year
#     date_time = file_name.split("_")

#     month = int(date_time[1][:2])   
#     day = int(date_time[1][2:])
#     hour = int(date_time[2][:2])
#     if hour == 24:
#         hour = 0
#     minute = int(date_time[2][2:])
    
#     # 현재 년도와 추출한 월, 일로 datetime 생성
#     game_date = datetime(current_year, month, day, hour, minute)
    
#     # 부캐 닉네임 처리
    
#     # mapping_maps = find_mapping_name()
#     res_list = list()
    
#     # return json 으로 해줘야댐 
#     stats_array = json.loads(stats_array)
#     print(stats_array)
#     for d in stats_array:
#         try:
#             res_list.append(
#                 {'assist':d['ASSISTS'],
#                  'death':d['NUM_DEATHS'],
#                  'kill':d['CHAMPIONS_KILLED'],
#                  'position':d['TEAM_POSITION'].replace('JUNGLE', 'JUG').replace('BOTTOM', 'ADC').replace('UTILITY', 'SUP').replace('MIDDLE', 'MID'),
#                  'riot_name':d['NAME'].replace('\\s','').replace('й','n').strip(),
#                 #  mapping_names 추가 변경
#                  'game_result':d['WIN'].replace('Win','승').replace('Fail','패'),
#                  'champ_name':d['SKIN'].lower().strip(),
#                 #  챔프이름 한글화
#                  'game_team':d['TEAM'].replace('100','blue').replace('200','red'),
#                  'gold':d['GOLD_EARNED'],
#                  'ccing':d['TIME_CCING_OTHERS'],
#                  'time_played':d['TIME_PLAYED'],
#                  'total_damage_champions':d['TOTAL_DAMAGE_DEALT_TO_CHAMPIONS'],
#                  'total_damage_taken':d['TOTAL_DAMAGE_TAKEN'],
#                  'vision_score':d['VISION_SCORE'],
#                  'vision_bought':d['VISION_WARDS_BOUGHT_IN_GAME'],
#                  'puuid':d['PUUID'],
#                  'game_date':game_date,
#                  'create_user':create_user,
#                  'game_id':file_name.lower(),
#                  'delete_yn':'N'
#                  }
#             )
#         except Exception as e:
#             print(e.__traceback__())
#             pass
    
#     # print(res_list)
        
#     db=du.Database()
#     db.connect()
#     db.insertLeague(res_list)
#     db.close()
    
# def save(byte, file_name, create_user):
#     stats_array = parse.parse_replay_data(byte)
#     set_data(stats_array,file_name, create_user)
    
    
# # if __name__ == "__main__":
# #     print(f'실행')
# #     file=open('test/1T_0922_0550.rofl','rb')
# #     file_byte = file.readlines()
# #     byte = None
# #     for byte in file_byte:
# #         continue
    
# #     save(byte,'1T_0922_0550','test_user')
    
    

    
    
