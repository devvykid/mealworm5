# 급식봇 API 서버 버전 5
![Try it out on Facebook Messenger](https://img.shields.io/badge/Messenger-Try%20it%20out-%230078FF?style=for-the-badge&logo=Messenger)
![GitHub](https://img.shields.io/github/license/hassium-io/mealworm5?style=flat-square)
  
<img src="https://user-images.githubusercontent.com/30792695/74304041-2f7bc200-4d9f-11ea-93d8-d6bfee983176.png" alt="급식봇 배너" width="70%">

### Disclaimer
당신 (그니까 너님) 이 급식봇을 사용했는데 급식이 맛없어서 토했다는가 또는 굶어 죽었다는가 등에 대해서는 급식봇에서는 일절 책임지지 않습니다. 당신의 어머니께서 말씀하셨듯이, 그런 거는 좀 알아서 해결하세요. (뭐 이슈를 넣는 거는 괜찮습니다만)

#### 잠깐! 코드를 보기 전에
코드가 더러울 수 있습니다.
썩은 눈은 사지 않습니다. 죄송합니다.

## 개요
급식이 급식을 위해 개발한 급식스러운 페이스북 메신저 봇, 급식봇의 서버 코드 리포지토리입니다.

급식봇으로는 전국 초/중/고등학교의 급식, 알러지 정보 등을 빠르고 쉽게 조회하실 수 있습니다.

급식봇은 python의 Flask 프레임워크와 Jinja2 템플릿 엔진을 사용해 만들어졌습니다. 뭐, 그렇다고요...

## 사용법
`급식봇 내일 서울과고 급식` --> 내일의 서울과학고 중식을 가져옵니다  
`세종과학고 3월 14일 저녁 알려줘라` --> 3월 14일의 세종과학고 석식을 가져옵니다  
`내일은?` --> 앞서 요청했던 학교의 내일 중식을 가져옵니다.

날짜를 생략할 경우 기본값은 오늘, 학교 이름을 생략할 경우 기본값은 마지막에 요청했던 학교, 
밥타임(?)을 생략할 경우 기본은 중식을 가져옵니다.

## 급식 가져오기
급식봇은 파이썬의 requests 모듈을 이용해 NEIS를 크롤링해 급식을 가져옵니다.  
학교 코드, 주소 정보를 가져올 때에는 schoolinfo.go.kr 의 API를 사용합니다.

## 자연어 처리
급식봇은 자연어 처리 기술을 이용해 정형된 방식으로 말하지 않아도 요청을 잘 처리할 수 있습니다.  
자연어 처리로는 [LUIS.ai](https://luis.ai) 를 이용하였고, LUIS.ai 코드는 어디 있냐 하면, 그건 비밀입니다. ㅋㅋㅋ

## 데이터베이스와 유저 관리
급식봇은 아주 멋지고 빠른 [Redis](https://redis.io/) 라는 NOSQL을 이용해 사용자 데이터를 관리합니다. 개꿀~!  
유저 관리에 대해서는 더 이상은 알려고 하지 마세요. ~~코드를 보면 됩니다~~

## 추후 개발 예정인 기능

- [ ] 급식 구독하기
- [ ] ~~너의 가상 여친~~

## 라이선스
mealworm5 코드는 [WTFPL](http://www.wtfpl.net/) (Do What The Fuck You Want To Public License) 로 배포됩니다. 왜냐고요? 재미있잖습니까... 허허허

###### Made with ♥️ by <img src="https://user-images.githubusercontent.com/30792695/74304401-3c4ce580-4da0-11ea-9631-42f303e8c1a9.png" alt="Hassium" height="20rem">
