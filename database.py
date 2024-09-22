import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
import simplejson as sjson
import json
from datetime import datetime

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 데이터베이스 접속 정보 가져오기
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

class Database:
    def __init__(self):
        self.db= None
        self.cursor= None
        
    def __del__(self):
        self.cursor.close()
        self.db.close()    
    
    def connect(self, host=DB_HOST, dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, port=DB_PORT):
        self.db = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
        self.cursor = self.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)    

    def close(self):
        self.cursor.close()
        self.db.close()
        
    def execute_query(self, query, params):
        if params is None:
            params = ()
        
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return json.loads(sjson.dumps(rows))
 
    # 예시
    def findLeague(self):
        self.cursor.execute("select game_id,riot_name from league limit 10")
        rows = self.cursor.fetchall()
        return json.loads(sjson.dumps(rows))
    
    ## SELECT ====================================================

    # 전체 전적 조회
    def findRecord(self, riot_name):
        query = """
            SELECT 
                POSITION,
                COUNT(*) AS TOTAL_COUNT,
                COUNT(CASE WHEN GAME_RESULT = '승' THEN 1 END) AS WIN,
                COUNT(CASE WHEN GAME_RESULT = '패' THEN 1 END) AS LOSE,
                CASE 
                    WHEN COUNT(*) = 0 THEN 0
                    ELSE ROUND(COUNT(CASE WHEN GAME_RESULT = '승' THEN 1 END)::NUMERIC / NULLIF(COUNT(*), 0) * 100 ,2)
                END AS WIN_RATE,
                CASE
                    WHEN SUM(DEATH) = 0 THEN 9999
                    ELSE ROUND((SUM(KILL) + SUM(ASSIST))::NUMERIC / NULLIF(SUM(DEATH), 0), 2) 
                END AS KDA
            FROM LEAGUE
            WHERE LOWER(RIOT_NAME) = LOWER(%s)
            AND DELETE_YN = 'N'
            GROUP BY POSITION
            ORDER BY 
                CASE POSITION
                WHEN 'TOP' THEN 1
                WHEN 'JUG' THEN 2
                WHEN 'MID' THEN 3
                WHEN 'ADC' THEN 4
                WHEN 'SUP' THEN 5
            END
        """
        return self.execute_query(query, (riot_name,))
    
    # 최근 한달 전적
    def findRecordMonth(self, riot_name):
        query = """
            SELECT 
                COUNT(*) AS TOTAL_COUNT,
                COUNT(CASE WHEN GAME_RESULT = '승' THEN 1 END) AS WIN,
                COUNT(CASE WHEN GAME_RESULT = '패' THEN 1 END) AS LOSE,
                CASE 
                    WHEN COUNT(*) = 0 THEN 0
                    ELSE ROUND(COUNT(CASE WHEN GAME_RESULT = '승' THEN 1 END)::NUMERIC / NULLIF(COUNT(*), 0) * 100 ,2)
                END AS WIN_RATE,
                CASE
                    WHEN SUM(DEATH) = 0 THEN 9999
                    ELSE ROUND((SUM(KILL) + SUM(ASSIST))::NUMERIC / NULLIF(SUM(DEATH), 0), 2) 
                END AS KDA
            FROM LEAGUE
            WHERE LOWER(RIOT_NAME) = LOWER(%s)
            AND DELETE_YN = 'N'
            AND GAME_DATE >= DATE_TRUNC('month', CURRENT_TIMESTAMP)
            AND GAME_DATE < DATE_TRUNC('month', CURRENT_TIMESTAMP) + INTERVAL '1 month'
            
        """
        return self.execute_query(query, (riot_name,))
    
    # 모스트픽
    def findMostPick(self, riot_name):
        query = """
            SELECT 
                CHAMP_NAME,
                COUNT(CHAMP_NAME) AS TOTAL_COUNT,
                COUNT(CASE WHEN GAME_RESULT = '승' THEN 1 END) AS WIN,
                COUNT(CASE WHEN GAME_RESULT = '패' THEN 1 END) AS LOSE,
                ROUND(COUNT(CASE WHEN GAME_RESULT = '승' THEN 1 END)::numeric / COUNT(*) * 100 ,2) AS WIN_RATE
            FROM LEAGUE
            WHERE LOWER(RIOT_NAME) = LOWER(%s)
            AND DELETE_YN = 'N'
            GROUP BY CHAMP_NAME
            ORDER BY TOTAL_COUNT DESC 
            LIMIT 10
        """
        return self.execute_query(query, (riot_name,))
    
    # 장인
    def findChampMaster(self, champ_name):
        query = """
            SELECT 
                RIOT_NAME, 
                COUNT(RIOT_NAME) AS TOTAL_COUNT,
                COUNT(CASE WHEN GAME_RESULT = '승' THEN 1 END) AS WIN,
                COUNT(CASE WHEN GAME_RESULT = '패' THEN 1 END) AS LOSE,
                ROUND(COUNT(CASE WHEN GAME_RESULT = '승' THEN 1 END)::NUMERIC / COUNT(*) * 100 ,2) AS WIN_RATE
            FROM LEAGUE 
            WHERE CHAMP_NAME = %s
            AND DELETE_YN = 'N'
            GROUP BY RIOT_NAME 
            HAVING COUNT(RIOT_NAME) >= 10
            ORDER BY TOTAL_COUNT DESC
        """
        return self.execute_query(query, (champ_name,))
        
    # 통계 챔피언    
    def findChampStats(self, year, month):
        query = """
            SELECT 
                CHAMP_NAME,
                COUNT(CHAMP_NAME) AS TOTAL_COUNT,
                COUNT(CASE WHEN game_result = '승' THEN 1 END) AS win,
                COUNT(CASE WHEN game_result = '패' THEN 1 END) AS lose,
                ROUND(COUNT(CASE WHEN game_result = '승' THEN 1 END)::numeric / COUNT(*)*100,2) AS win_rate
            FROM LEAGUE 
            WHERE DELETE_YN = 'N'
                AND EXTRACT(YEAR FROM GAME_DATE) = %s
                AND EXTRACT(MONTH FROM GAME_DATE) = %s
            GROUP BY CHAMP_NAME
            HAVING COUNT(CHAMP_NAME) >= 20
        """
        return self.execute_query(query, (year, month))    
        
    # 통계 게임
    def findGameStats(self, year, month):
        query = """
            SELECT 
                RIOT_NAME,
                COUNT(RIOT_NAME) AS TOTAL_COUNT,
                COUNT(CASE WHEN game_result = '승' THEN 1 END) AS win,
                COUNT(CASE WHEN game_result = '패' THEN 1 END) AS lose,
                ROUND(COUNT(CASE WHEN game_result = '승' THEN 1 END)::numeric / COUNT(*)*100,2) AS win_rate,
            CASE
                WHEN SUM(DEATH) = 0 THEN 9999
                ELSE ROUND((SUM(KILL) + SUM(ASSIST))::NUMERIC / NULLIF(SUM(DEATH), 0), 2) 
                END AS KDA
            FROM LEAGUE 
            WHERE DELETE_YN = 'N'
                AND EXTRACT(YEAR FROM GAME_DATE) = %s
                AND EXTRACT(MONTH FROM GAME_DATE) = %s
            GROUP BY RIOT_NAME
            ORDER BY TOTAL_COUNT DESC
        """
        return self.execute_query(query, (year, month))
        
    # 최근 두달간 같은 팀 시너지
    def findRecordWithTeam(self, riot_name):
        query = """
            SELECT 
                A.RIOT_NAME,
                COUNT(A.RIOT_NAME) AS TOTAL_COUNT,
                COUNT(CASE WHEN B.GAME_RESULT = '승' THEN 1 END) AS WIN,
                COUNT(CASE WHEN B.GAME_RESULT = '패' THEN 1 END) AS LOSE,
                ROUND(COUNT(CASE WHEN B.GAME_RESULT = '승' THEN 1 END)::NUMERIC / COUNT(*)*100,2) AS WIN_RATE
            FROM LEAGUE A 
            INNER JOIN  
            (
                SELECT * FROM LEAGUE 
                WHERE LOWER(RIOT_NAME) = LOWER(%s)
                AND (
                    (EXTRACT(YEAR FROM GAME_DATE) = EXTRACT(YEAR FROM CURRENT_DATE)
                    AND EXTRACT(MONTH FROM GAME_DATE) = EXTRACT(MONTH FROM CURRENT_DATE))
                    OR
                    (EXTRACT(YEAR FROM GAME_DATE) = EXTRACT(YEAR FROM CURRENT_DATE - INTERVAL '1 month')
                    AND EXTRACT(MONTH FROM GAME_DATE) = EXTRACT(MONTH FROM CURRENT_DATE - INTERVAL '1 month'))
                    )
            ) B
            ON A.GAME_TEAM = B.GAME_TEAM 
            AND A.GAME_ID = B.GAME_ID 
            AND LOWER(A.RIOT_NAME) != LOWER(%s)
            AND A.DELETE_YN = 'N'
            GROUP BY A.RIOT_NAME
            HAVING  COUNT(A.RIOT_NAME) >= 5
            ORDER BY WIN_RATE DESC
        """
        return self.execute_query(query, (riot_name, riot_name))
        
    # 나와 인간상성 찾기
    def findRecordOtherTeam(self, riot_name):
        query = """
            SELECT 
                A.RIOT_NAME,
                COUNT(A.RIOT_NAME) AS TOTAL_COUNT,
                COUNT(CASE WHEN B.GAME_RESULT = '승' THEN 1 END) AS WIN,
                COUNT(CASE WHEN B.GAME_RESULT = '패' THEN 1 END) AS LOSE,
                ROUND(COUNT(CASE WHEN B.GAME_RESULT = '승' THEN 1 END)::NUMERIC / COUNT(*)*100,2) AS WIN_RATE
            FROM LEAGUE A 
            INNER JOIN  
            (
                SELECT * FROM LEAGUE 
                WHERE LOWER(RIOT_NAME) = LOWER(%s)
                AND (
                    (EXTRACT(YEAR FROM GAME_DATE) = EXTRACT(YEAR FROM CURRENT_DATE)
                    AND EXTRACT(MONTH FROM GAME_DATE) = EXTRACT(MONTH FROM CURRENT_DATE))
                    OR
                    (EXTRACT(YEAR FROM GAME_DATE) = EXTRACT(YEAR FROM CURRENT_DATE - INTERVAL '1 month')
                    AND EXTRACT(MONTH FROM GAME_DATE) = EXTRACT(MONTH FROM CURRENT_DATE - INTERVAL '1 month'))
                )
            ) B
            ON A.GAME_TEAM != B.GAME_TEAM 
            AND A.GAME_ID = B.GAME_ID 
            AND LOWER(A.RIOT_NAME) != LOWER(%s)
            AND A.DELETE_YN = 'N'
            AND A.POSITION = B.POSITION
            GROUP BY A.RIOT_NAME
            HAVING  COUNT(A.RIOT_NAME) >= 5
            ORDER BY WIN_RATE DESC
        """
        return self.execute_query(query, (riot_name, riot_name))
        
    # 라인별 승률 조회
    def findRecordLine(self, position):
        query = """
            SELECT 	
                POSITION,
                RIOT_NAME,
                COUNT(RIOT_NAME) AS TOTAL_COUNT,
                COUNT(CASE WHEN GAME_RESULT = '승' THEN 1 END) AS WIN,
                COUNT(CASE WHEN GAME_RESULT = '패' THEN 1 END) AS LOSE,
                ROUND(COUNT(CASE WHEN GAME_RESULT = '승' THEN 1 END)::NUMERIC / COUNT(*)*100,2) AS WIN_RATE,
                CASE
                    WHEN SUM(DEATH) = 0 THEN 9999
                    ELSE ROUND((SUM(KILL) + SUM(ASSIST))::NUMERIC / NULLIF(SUM(DEATH), 0), 2) 
                END AS KDA
            FROM LEAGUE  
            WHERE POSITION = %s
            AND DELETE_YN = 'N'
            GROUP BY POSITION, RIOT_NAME 
            HAVING COUNT(RIOT_NAME) >= 50
            ORDER BY WIN_RATE DESC
            LIMIT 15   
        """
        return self.execute_query(query, (position, ))
    
    
    # 게임 결과
    def findRecordByGameId(self, game_id):
        query = """
            SELECT 
                GAME_ID, 
                RIOT_NAME, 
                CHAMP_NAME, 
                POSITION, 
                KILL, 
                DEATH, 
                ASSIST, 
                GAME_RESULT, 
                GAME_TEAM,
                TOTAL_DAMAGE_CHAMPIONS,
                VISION_BOUGHT
            FROM LEAGUE
            WHERE LOWER(GAME_ID) = LOWER(%s)
            AND DELETE_YN = 'N'
            ORDER BY GAME_TEAM,
                CASE POSITION
                WHEN 'TOP' THEN 1
                WHEN 'JUG' THEN 2
                WHEN 'MID' THEN 3
                WHEN 'ADC' THEN 4
                WHEN 'SUP' THEN 5
            END
        """
        return self.execute_query(query, (game_id, ))
    
    # 최근 Top 10 게임 조회
    def findTopTen(self, riot_name):
        query = """
            SELECT 
                GAME_ID, 
                RIOT_NAME, 
                CHAMP_NAME, 
                POSITION, 
                KILL, 
                DEATH, 
                ASSIST, 
                GAME_RESULT, 
                GAME_TEAM,
                TOTAL_DAMAGE_CHAMPIONS,
                VISION_BOUGHT
            FROM LEAGUE
            WHERE LOWER(RIOT_NAME) = LOWER(%s)
            AND DELETE_YN = 'N'
            ORDER BY GAME_DATE DESC
            LIMIT 10
        """
        return self.execute_query(query, (riot_name, ))
        
    # 부캐 닉네임 조회
    def findMappingName(self):
        query = """
            SELECT 
                SUB_NAME,
                MAIN_NAME
            FROM
                MAPPING_NAME
            WHERE 
                DELETE_YN = 'N'
        """
        return self.execute_query(query,None)
    
    # 중복 리플 파일명 조회
    def findReplayName(self, game_id):
        query = """
            SELECT
                COUNT(*)
            FROM
                LEAGUE
            WHERE
                GAME_ID = %s
        """
        return self.execute_query(query, (game_id, ))
        
    ## INSERT ====================================================
    
    # 리플 데이터 저장 ver1 row
    def insertLeague(self, params):
        query = """
            INSERT INTO LEAGUE
            (
                game_id,
                riot_name,
                champ_name,
                position,
                kill, 
                death, 
                assist,
                game_result,
                game_team,
                game_date,
                create_date,
                update_date,
                delete_yn,
                create_user,
                gold,
                ccing,
                time_played,
                total_damage_champions,
                total_damage_taken,
                vision_score,
                vision_bought,
                puuid
            )
            VALUES %s
        """

        # Create a list of tuples where each tuple represents a row to insert
        values = [
            (
                item['game_id'],
                item['riot_name'],
                item['champ_name'],
                item['position'],
                item['kill'],
                item['death'],
                item['assist'],
                item['game_result'],
                item['game_team'],
                item['game_date'],
                datetime.now(),  # CURRENT_TIMESTAMP
                datetime.now(),  # CURRENT_TIMESTAMP
                item['delete_yn'],
                item['create_user'],
                item['gold'],
                item['ccing'],
                item['time_played'],
                item['total_damage_champions'],
                item['total_damage_taken'],
                item['vision_score'],
                item['vision_bought'],
                item['puuid']
            ) for item in params
        ]
        
        psycopg2.extras.execute_values(
            self.cursor, query, values
        )
        self.db.commit()
    
    # 리플 데이터 저장 ver2 all one
    
    # 부캐닉 저장
    def insertMappingName(self, sub_name, main_name):
        query = """
            INSERT INTO MAPPING_NAME
            (
                SUB_NAME,
                MAIN_NAME,
                CREATE_DATE,
                UPDATE_DATE,
                DELETE_YN
            )
            VALUES 
            (
                %s,
                %s,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP,
                'N'
            )
        """

        params = (sub_name, main_name)
        self.cursor.execute(query, params)
        self.db.commit()
        
    
    ## UPDATE ====================================================
    
    # 탈퇴 및 복구 회원처리 - 리그정보
    def changeDeleteYN(self, delete_yn, riot_name):
        query = """
            UPDATE LEAGUE
                SET DELETE_YN = %s,
                UPDATE_DATE = CURRENT_TIMESTAMP
            WHERE 
                RIOT_NAME = %s
        """
        
        params = (delete_yn, riot_name)
        self.cursor.execute(query, params)
        self.db.commit()
        return self.cursor.rowcount
        
    # 탈퇴 및 복구 회원처리 - 부캐닉
    def changeMappingDeleteYN(self, delete_yn, riot_name):
        query = """
            UPDATE MAPPING_NAME
                SET DELETE_YN = %s,
                UPDATE_DATE = CURRENT_TIMESTAMP
            WHERE 
                MAIN_NAME = %s
        """
        
        params = (delete_yn, riot_name)
        self.cursor.execute(query, params)
        self.db.commit()
        return self.cursor.rowcount
    
    # 닉네임 변경 - 리그정보
    def changeRiotName(self, new_name, old_name):
        query = """
            UPDATE LEAGUE
                SET RIOT_NAME = %s,
                UPDATE_DATE = CURRENT_TIMESTAMP
            WHERE RIOT_NAME = %s
        """
        
        params = (new_name, old_name)
        self.cursor.execute(query, params)
        self.db.commit()
        return self.cursor.rowcount
    
    # 닉네임 변경 - 부캐닉    
    def changeMappingRiotName(self, new_name, old_name):
        query = """
            UPDATE MAPPING_NAME
                SET MAIN_NAME = %s,
                UPDATE_DATE = CURRENT_TIMESTAMP
            WHERE MAIN_NAME = %s
        """
        
        params = (new_name, old_name)
        self.cursor.execute(query, params)
        self.db.commit()
        return self.cursor.rowcount
    
    ## DELETE ====================================================
    
    # !drop 리플 삭제
    def deleteLeagueByGameId(self, game_id):
        query = """
            DELETE FROM LEAGUE
                WHERE GAME_ID = %s
        """
        
        params = (game_id,)
        self.cursor.execute(query, params)
        self.db.commit()
        return self.cursor.rowcount
    
    # 부캐삭제
    def deleteMappingSubName(self, riot_name):
        query = """
            DELETE FROM MAPPING_NAME
                WHERE SUB_NAME = %s
        """
        
        params = (riot_name,)
        self.cursor.execute(query, params)
        self.db.commit()
        return self.cursor.rowcount