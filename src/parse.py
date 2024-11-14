from datetime import datetime
from champion_dictionary import champion_dic
from service import LeagueService

import requests
import json
import io

ls = LeagueService()

# 리플레이 저장
def save(file_url, file_name, create_user, guild_id):  
        
    # test
    # file=open('test/1t_0927_0038.rofl','rb')
    # file_byte = file.readlines()
    # bytes_data = None
    # for bytes_data in file_byte:
    #     continue
    
    if check_duplicate(file_name, guild_id) : 
        bytes_data = get_input_stream_discord_file(file_url)
        
        if bytes_data:
            stats_array = parse_replay_data(bytes_data)
            save_data(stats_array, file_name, create_user, guild_id)
            return f":green_circle:등록완료: {file_name} 반영 완료"
        else:
            raise Exception("파일 데이터 저장 중 에러.")
    else :
        return f":red_circle:등록실패: {file_name} 중복된 리플 파일 등록"
   
# 데이터 파싱 로직
def parse_replay_data(byte):
    
    start_index = byte.find(b'{"gameLength":')
    end_index = byte.rfind(b'\\"}]"}')
    
    if not byte or len(byte) == 0:
        raise Exception("파싱 데이터가 없습니다")

    try:
        byte = byte[start_index:end_index+6].replace(b'\\', b'').replace(b'"[', b'[').replace(b']"', b']')
        data = byte.decode('utf-8')

        # JSON 데이터 파싱
        root_node = json.loads(data)
        stats_array = root_node.get("statsJson")

        return json.dumps(stats_array)

    except Exception as e:
        print(f"파싱 에러: {e}")
        raise

# 디스코드에 올린 파일 데이터 가져오기
def get_input_stream_discord_file(file_url):
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()

        # 응답 데이터를 byte로 변환
        return change_byte_array(response.raw)
    except requests.exceptions.RequestException as e:
        print(f"파일 가져오기 에러: {e}")
        return None

# byte[] 변환
def change_byte_array(raw_stream):
    try:
        buffer = io.BytesIO()
        for chunk in raw_stream:
            if chunk:
                buffer.write(chunk)
        return buffer.getvalue()
    except Exception as e:
        print(f"Byte 변환 에러: {e}")
        return None
    
# 파싱한 데이터 save
def save_data(stats_array, file_name, create_user, guild_id):
    # print('set 시작')
    current_year = datetime.now().year
    date_time = file_name.split("_")

    month = int(date_time[1][:2])   
    day = int(date_time[1][2:])
    hour = int(date_time[2][:2])
    if hour == 24:
        hour = 0
    minute = int(date_time[2][2:])
    
    # 현재 년도와 추출한 월, 일로 datetime 생성
    game_date = datetime(current_year, month, day, hour, minute)
    
    res_list = list()
    # return json 으로 해줘야댐 
    stats_array = json.loads(stats_array)
    # print(stats_array)
    for d in stats_array:
        try:
            res_list.append(
                {'assist':d['ASSISTS'],
                 'death':d['NUM_DEATHS'],
                 'kill':d['CHAMPIONS_KILLED'],
                 'position':d['TEAM_POSITION'].replace('JUNGLE', 'JUG').replace('BOTTOM', 'ADC').replace('UTILITY', 'SUP').replace('MIDDLE', 'MID'),
                 'riot_name':set_mapping_name(d['NAME'].replace(' ','').replace('й','n').strip(), guild_id),
                 'game_result':d['WIN'].replace('Win','승').replace('Fail','패'),
                 'champ_name': champion_dic.dic.get(d['SKIN'].lower().strip(), d['SKIN'].lower().strip()),
                 'game_team':d['TEAM'].replace('100','blue').replace('200','red'),
                 'gold':d['GOLD_EARNED'],
                 'ccing':d['TIME_CCING_OTHERS'],
                 'time_played':d['TIME_PLAYED'],
                 'total_damage_champions':d['TOTAL_DAMAGE_DEALT_TO_CHAMPIONS'],
                 'total_damage_taken':d['TOTAL_DAMAGE_TAKEN'],
                 'vision_score':d['VISION_SCORE'],
                 'vision_bought':d['VISION_WARDS_BOUGHT_IN_GAME'],
                 'puuid':d['PUUID'],
                 'game_date':game_date,
                 'create_user':create_user,
                 'game_id':file_name.lower(),
                 'delete_yn':'N',
                 'guild_id':guild_id
                 }
            )
        except Exception as e:
            print(e.__traceback__())
            pass
    
    # print(res_list)
    ls.save_league(res_list)
    
# 매핑 이름 처리
def set_mapping_name(name, guild_id):
    mappings = ls.get_mapping_name(guild_id)
    
    for mapping in mappings:
        if name == mapping['sub_name']:            
            return mapping['main_name']
    return name

# 리플 파일명 중복 확인
def check_duplicate(file_name, guild_id):
    result = ls.count_by_replay_name(file_name, guild_id)
    if result[0]['count'] > 0 :
        return False
    else :
        return True
   
# 예시 사용
# file_url = 'https://example.com/discordfile'
# try:
#     result = parse_replay(file_url)
#     print(result)
# except Exception as e:
#     print(f"Error: {e}")
    
# if __name__ == "__main__":
#     file=open('1T_0922_0550.rofl','rb')
#     file_byte = file.readlines()
#     byte = None
#     for byte in file_byte:
#         continue
    
#     file2=open('test.text','w')
#     file2.write(parse_replay_data(byte))
#     file2.close()
#     # print(parse_replay_data(byte))
        
# if __name__ == "__main__":
#     print(f'실행')
#     file=open('test/1T_0922_0550.rofl','rb')
#     file_byte = file.readlines()
#     byte = None
#     for byte in file_byte:
#         continue
    
#     save(byte,'1T_0922_0550','test_user')        