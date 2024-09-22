from database import Database

class LeagueService:
    def __init__(self):
        self.db = Database()
        self.db.connect()

# !전적

    # 전체전적조회
    def get_record(self, riot_name):
        return self.db.findRecord(riot_name)
    
    # 최근한달조회
    def get_record_month(self, riot_name):
        return self.db.findRecordMonth(riot_name)
    
    # 모스트픽
    def get_most_pick(self, riot_name):
        return self.db.findMostPick(riot_name)
    
    # 최근 두달간 같은 팀 시너지
    def get_record_with_team(self, riot_name):
        return self.db.findRecordWithTeam(riot_name)
    
    # 나와 인간상성 찾기
    def get_record_other_team(self, riot_name):
        return self.db.findRecordOtherTeam(riot_name)
    
# !장인

    # 장인
    def get_champ_master(self, champ_name):
        return self.db.findChampMaster(champ_name)
    
# !통계(챔프,게임)

    # 챔프
    def get_champ_stats(self, year, month):
        return self.db.findChampStats(year,month)
    
    # 게임
    def get_game_stats(self, year, month):
        return self.db.findGameStats(year,month)

# !라인

    # 라인별 승률 조회
    def get_record_line(self, position):
        return self.db.findRecordLine(position)
    
# !결과

    # 게임 결과
    def get_record_game_id(self, game_id):
        return self.db.findRecordByGameId(game_id)
    
# 기타

    # 최근 Top 10 게임 조회
    def get_top_ten(self, riot_name):
        return self.db.findTopTen(riot_name)
    
    