# 급식봇 API 서버 버전 5
<a href="https://m.me/mealworm05">![Try it out on Facebook Messenger](https://img.shields.io/badge/Messenger-Try%20it%20out-%230078FF?style=for-the-badge&logo=Messenger&logoColor=%23ffffff)</a>
![GitHub](https://img.shields.io/badge/LICENSE-WTFPL-blueviolet?style=for-the-badge)
  
<img src="https://user-images.githubusercontent.com/30792695/82785254-2f5e8880-9e9d-11ea-8f34-dd2e7542bde7.png" alt="급식봇 로고" width="30%">

## Support me on Patreon
<a href="https://www.patreon.com/devvykid"><img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" alt="Become a Patron!" width="200px"></a>  

페이트리온에서 저를 후원해 주세요! 훌륭한 서비스로 보답하겠습니다.  

## 개요
### ~~병맛~~ Disclaimer
사용자 (고로 너님) 가 급식봇을 사용했는데, 급식이 맛없어서 토했다는가 또는 굶어 죽었다는가 등의 사소한 문제에 대해서는 개발자/기여자는 책임지지 않습니다.
당신의 어머니께서 말씀하셨듯이, 그런 거는 좀 알아서 해결하세요. (뭐 이슈를 넣는 거는 괜찮습니다만)

#### 잠깐! 코드를 보기 전에
코드가 더러울 수 있습니다.
썩은 눈은 사지 않습니다. 죄송합니다.

### 진짜 개요
급식이 급식을 위해 개발한 급식스러운 페이스북 메신저 봇, 급식봇(의 5번째 버전) 서버 코드 리포지토리입니다.
여기를 방문할 사람은 아무도 없다는 것을 알기에, (그리고 방문하더라도 아무도 이 길고 긴 리드미를 읽지 않는다는 걸 알기에...) 아무말 대잔치를 벌이고 있는 중입니다.

급식봇으로는 전국의 초/중/고등학교의 급식, 알러지 정보 등을 페이스북 메신저 플랫폼을 통해 빠르고 쉽게 조회하실 수 있습니다.

급식봇은 비단뱀이라는 아주 아름다운 언어와 Flask 프레임워크/Jinja2 템플릿 엔진, 그리고 Dialogflow를 이용해 만들어졌습니다. 어절씨구 옹헤야!

### 사용법
`급식봇 내일 서울과고 급식` --> 내일의 서울과학고 중식을 가져옵니다  
`세종과학고 3월 14일 저녁 알려줘라` --> 3월 14일의 세종과학고 석식을 가져옵니다  
`내일은?` --> 앞서 요청했던 학교의 내일 중식을 가져옵니다

날짜를 생략할 경우 기본값은 오늘, 학교 이름을 생략할 경우 기본값은 마지막에 요청했던 학교, 
밥타임(?)을 생략할 경우 기본은 중식을 가져옵니다.

## 구현

### 급식 가져오기
급식봇은 파이썬의 requests 모듈을 이용해 NEIS를 크롤링해 급식을 가져옵니다.  
학교 코드, 주소 정보를 가져올 때에는 schoolinfo.go.kr 의 API를 사용합니다.

### 자연어 처리
급식봇은 자연어 처리 기술을 이용해 정형화된 방식으로 말하지 않아도 요청을 잘 처리할 수 있습니다.  
자연어 처리로는 [Dialogflow](https://dialogflow.com/) 엔진을 이용하였고, Dialogflow 훈련 자료는 공개되어있지 않습니다.

### 데이터베이스와 유저 관리
급식봇은 아주 멋지고 빠른~~느려터진~~ [Firestore](https://cloud.google.com/firestore)를 이용해 사용자 데이터를 관리합니다. 개꿀~!  
유저 관리에 대해서는 더 이상은 알려고 하면 다칩니다. ~~코드를 보면 됩니다~~

## 서버(클라우드) 인프라 구성
급식봇의 모든 처리는 (외부 API 제외) [Google Cloud Platform](https://cloud.google.com/)에서 처리됩니다. 공짜 오예!

## 추후 개발 예정인 기능

- [ ] 급식 구독하기
- [ ] ~~너의 가상 여친~~

## 라이선스
mealworm5 코드는 [WTFPL](http://www.wtfpl.net/) (Do What The Fuck You Want To Public License) 로 배포됩니다. 왜냐고요? 읍읍 읍읍읍읍!!!!!
  
  
-------------------------------------------------------------------
###### Made with ♥️ by <img src="https://user-images.githubusercontent.com/30792695/82785153-fc1bf980-9e9c-11ea-84fd-0d331efdd985.png" alt="devvykid" height="30rem">
