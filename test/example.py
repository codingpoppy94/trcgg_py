import psycopg2
import psycopg2.extras
import simplejson as sjson
import json


class Model:
    def __init__(self):
        self.db = None
        self.cursor = None

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def connect(self, host, dbname, user, password):
        self.db = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=5432)
        self.cursor = self.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def close(self):
        self.cursor.close()
        self.db.close()

    def getBuildingOnwerInfo(self, ppk):
        self.cursor.execute(f"""
        select ppk, jpk, pnu, road_name_address_management_number, land_address, road_name_address, dong, ho, danji_lng,
               danji_lat, complex_key, dong_key, ho_key, purpose_name, owner_name, owner_age_category, share_rate
          from data_api.tb_building_owner_info_v2
         where ppk = '{ppk}'""")

        rows = self.cursor.fetchall()
        return json.loads(sjson.dumps(rows))
