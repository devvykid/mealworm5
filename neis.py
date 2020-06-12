class NEIS:
    def __init__(self, config):
        # Read Keys from config.ini
        self.project_id = config['NEIS_OPENAPI_KEY']

        pass

    def search_school(self, query):
        """
        Neis OpenAPI 를 사용해 학교를 검색하고, NEIS.School 객체의 배열을 반환합니다.
        :param query: 학교 문자열
        :return: 검색된 학교 School Object 배열
        """
        pass

    class School:
        class _Meal:
            def __init__(self, menus, allergies):
                self.menus = menus
                self.allergies = allergies

        def __init__(self):
            pass

        def get_meal(self, date, time):
            """

            :param date: datetime.date 객체. 급식을 가져올 날짜
            :param time: 1: 조식, 2: 중식, 3: 석식
            :return: _Meal 객체
            """
            meal = self._Meal(menus=[], allergies=[])
            return meal
