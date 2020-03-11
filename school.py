import datetime
import pytz
import requests
from urllib import parse
import time


class School:
    def __init__(self, school_name, school_code, school_region, school_address, school_region_hangul):
        self.name = school_name
        self.code = school_code
        self.region = school_region
        self.address = school_address
        self.region_hangul = school_region_hangul

        return

    def get_meal(self, date, mealtime):
        # TODO: 경고: mealtime은 '텍스트' 입니다 (아님 None 이던가)
        pass


class Neis:
    def __init__(self):
        pass

    def search_school(self, q):
        # 과고 -> 과학고 등 처리다
        if q.endswith('과고'):
            q = q.replace('과고', '과학고')

        # 학교 이름 짧을경우 ValueError
        if len(q) < 2:
            raise ValueError

        # 본격적 수색작업 시작
        url = "https://www.schoolinfo.go.kr/ei/ss/Pneiss_a01_l0.do"

        payload = "HG_CD=" \
                  "&SEARCH_KIND=" \
                  "&HG_JONGRYU_GB=" \
                  "&GS_HANGMOK_CD=" \
                  "&GS_HANGMOK_NM=" \
                  "&GU_GUN_CODE=" \
                  "&SIDO_CODE="  \
                  "&GUGUN_CODE=" \
                  "&SRC_HG_NM=" + parse.quote(q)

        headers = {
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        result = response.json()
        final_result = []

        for category in result:
            for sch in result[category]:
                s = School(
                    sch['SCHUL_NM'],    # 풀네임
                    sch['SCHUL_CODE'],  # 나이스 코드
                    self.school_code_kor_to_eng(sch['LCTN_NM']),  # 나이스 리전 코드
                    sch['SCHUL_RDNMA'],  # 주소
                    sch['LCTN_NM']      # 한글지역명
                )
                final_result.append(s)

        return final_result  # 리스트 리턴

    @staticmethod
    def school_code_kor_to_eng(kor):
        school_codes = [
            ('서울', 'sen'),
            ('부산', 'pen'),
            ('대구', 'dge'),
            ('인천', 'ice'),
            ('광주', 'gen'),
            ('대전', 'dje'),
            ('울산', 'use'),
            ('세종', 'sje'),
            ('경기', 'goe'),
            ('강원', 'kwe'),
            ('충북', 'cbe'),
            ('충남', 'cne'),
            ('전북', 'jbe'),
            ('전남', 'jne'),
            ('경북', 'gbe'),
            ('경남', 'gne'),
            ('제주', 'jje')
        ]

        # 한글 -> 영어 변환
        for i in school_codes:
            if kor.strip() == i[0]:
                return i[1]
        return None


class Meal:
    def __init__(self, menus, allergies, mealtime):
        self.menus = menus
        self.allergies = allergies
        self.mealtime = mealtime

    def text(self):
        # 급식이 없으면 None 을 리턴합니다.
        return ''
