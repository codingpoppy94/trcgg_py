from database import Database

class LeagueService:
    def __init__(self):
        self.db = Database()
        self.db.connect()

# !전적

    # 전체전적조회
    def get_record(self, riot_name, guild_id):
        return self.db.findRecord(riot_name, guild_id)
    
    # 최근한달조회
    def get_record_month(self, riot_name, guild_id):
        return self.db.findRecordMonth(riot_name, guild_id)
    
    # 모스트픽
    def get_most_pick(self, riot_name, guild_id):
        return self.db.findMostPick(riot_name, guild_id)
    
    # 최근 두달간 같은 팀 시너지
    def get_record_with_team(self, riot_name, guild_id):
        return self.db.findRecordWithTeam(riot_name, guild_id)
    
    # 나와 인간상성 찾기
    def get_record_other_team(self, riot_name, guild_id):
        return self.db.findRecordOtherTeam(riot_name, guild_id)
    
# !장인

    # 장인
    def get_champ_master(self, champ_name, guild_id):
        return self.db.findChampMaster(champ_name, guild_id)
    
# !통계(챔프,게임)

    # 챔프
    def get_champ_stats(self, year, month, guild_id):
        return self.db.findChampStats(year,month, guild_id)
    
    # 게임
    def get_game_stats(self, year, month, guild_id):
        return self.db.findGameStats(year, month, guild_id)

# !라인

    # 라인별 승률 조회
    def get_record_line(self, position, guild_id):
        return self.db.findRecordLine(position, guild_id)
    
# !결과

    # 게임 결과
    def get_record_game_id(self, game_id, guild_id):
        return self.db.findRecordByGameId(game_id, guild_id)
    
# 기타

    # 최근 Top 10 게임 조회
    def get_top_ten(self, riot_name, guild_id):
        return self.db.findTopTen(riot_name, guild_id)
    
    # 리플 데이터 저장
    def save_league(self, params):
        return self.db.insertLeague(params)
    
    # 부캐닉 조회 
    def get_mapping_name(self, guild_id):
        return self.db.findMappingName(guild_id)
    
    # 중복 리플 파일 조회
    def count_by_replay_name(self, game_id, guild_id):
        return self.db.countReplay(game_id, guild_id)
    
# 관리

    # !부캐 저장
    def save_mapping_name(self, sub_name, main_name, guild_id):
        return self.db.insertMappingName(sub_name, main_name, guild_id)

    # !탈퇴 - 리그 정보
    def update_delete_yn(self, delete_yn, riot_name, guild_id):
        return self.db.changeDeleteYN(delete_yn, riot_name, guild_id)
    
    # !탈퇴 - 부캐 닉네임
    def update_mapping_delete_yn(self, delete_yn, riot_name, guild_id):
        return self.db.changeMappingDeleteYN(delete_yn, riot_name, guild_id)
    
    # !닉변 - 리그 정보
    def update_riot_name(self, new_name, old_name, guild_id):
        return self.db.changeRiotName(new_name, old_name, guild_id)
    
    # !닉변 - 부캐 닉네임 
    def update_mapping_riot_name(self, new_name, old_name, guild_id):
        return self.db.changeMappingRiotName(new_name, old_name, guild_id)
    
    # !drop - 리플 삭제
    def delete_league_by_game_id(self, game_id, guild_id):
        return self.db.deleteLeagueByGameId(game_id, guild_id)
    
    # !부캐삭제
    def delete_mapping_sub_name(self, riot_name, guild_id):
        return self.db.deleteMappingSubName(riot_name, guild_id)
    
# 길드 관리

    # 길드 조회
    def get_guild(self, guild_id):
        return self.db.findGuild(guild_id)
    
    # 길드 추가
    def save_guild(self, guild_id, guild_name):
        return self.db.insertGuild(guild_id, guild_name)
    
    