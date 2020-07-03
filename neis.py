class NEIS:
    def __init__(self, config):
        # Read Keys from config.ini
        self.key = config['NEIS_OPENAPI_KEY']

        return

    def search_school(self, query):
        """
        Neis OpenAPI 를 사용해 학교를 검색하고, NEIS.School 객체의 배열을 반환합니다.
        :param query: 학교 문자열
        :return: 검색된 학교 School Object 배열 (없으면 [] 리턴)
        """
        return []

    def school_from_code(self, code):
        """
        학교 코드를 받아 해당 학교의 NEIS.School 객체를 반환합니다.
        :param code: 나이스 학교코드:str
        :return: NEIS.School
        """
        pass

    class School:
        class _Menu:
            def __init__(self, menu, allergy):
                self.name = menu
                self.allergy = allergy

        def __init__(self, name, code, region_code, region_hangul, address):
            self.name = name
            self.code = code
            self.region_code = region_code
            self.region_hangul = region_hangul
            self.address = address
            return

        def get_meal(self, date, time):
            """
            급식을 가져온다.
            :param date: datetime.date 객체. 급식을 가져올 날짜
            :param time: int. 1: 조식, 2: 중식, 3: 석식
            :return: Array (School._Menu)
            """
            menus = [], allergies = []
            ######

            result = []
            for i in range(len(menus)):
                m = self._Menu(menus[i], allergies[i])
                result.append(m)

            return result
