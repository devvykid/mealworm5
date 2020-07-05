# 급식봇 API 서버 버전 5
<a href="https://m.me/mealworm05">![Try it out on Facebook Messenger](https://img.shields.io/badge/Messenger-Try%20it%20out-%230078FF?style=for-the-badge&logo=Messenger&logoColor=%23ffffff)</a>
![GitHub](https://img.shields.io/badge/LICENSE-WTFPL-blueviolet?style=for-the-badge)
  
<img src="https://user-images.githubusercontent.com/30792695/82785254-2f5e8880-9e9d-11ea-8f34-dd2e7542bde7.png" alt="급식봇 로고" width="30%">

## Support me on Patreon
<a href="https://www.patreon.com/devvykid"><img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" alt="Become a Patron!" width="200px"></a>  

페이트리온에서 저를 후원해 주세요! 훌륭한 서비스로 보답하겠습니다.  

## 개요
### ~~병맛~~ Disclaimer
사용자가 급식봇을 사용했는데, 급식이 맛없어서 토했다는가 또는 굶어 죽었다는가 등의 사소한 문제에 대해서는 개발자/기여자는 책임지지 않습니다. 그런 거는 좀 알아서 해결하세요. (뭐 이슈를 넣는 거는 괜찮습니다만)

#### 잠깐! 코드를 보기 전에
코드가 더러울 수 있습니다.
썩은 눈은 사지 않습니다. 죄송합니다.

### 진짜 개요
급식이 급식을 위해 개발한 급식스러운 페이스북 메신저 봇, 급식봇(의 5번째 버전) 서버 코드 리포지토리입니다.  
리드미에서는 아무 말 대잔치가 벌어지고 있습니다.

급식봇으로는 전국의 초/중/고등학교의 급식, 알러지 정보 등을 페이스북 메신저 플랫폼을 통해 빠르고 쉽게 조회하실 수 있습니다.

급식봇은 비단뱀이라는 아주 아름다운 언어와 Flask 프레임워크와 Jinja2 템플릿 엔진, 그리고 Dialogflow를 이용해 만들어졌습니다.  
2019년부터 [나이스 오픈API](https://open.neis.go.kr/portal/mainPage.do)가 개방하면서 pyneis/schoolinfo 대신 API를 사용합니다.

## 사용법
<a href="https://m.me/mealworm05">![Try it out on Facebook Messenger](https://img.shields.io/badge/Messenger-Try%20it%20out-%230078FF?style=for-the-badge&logo=Messenger&logoColor=%23ffffff)</a>  
위 버튼을 눌러 시작합니다. 페이스북 메신저를 이용하기 위해서는 페이스북 계정이 필요합니다. 
 
`급식봇 내일 서울과고 급식` --> 내일의 서울과학고 중식을 가져옵니다  
`세종과학고 3월 14일 저녁 알려줘라` --> 3월 14일의 세종과학고 석식을 가져옵니다  
`내일은?` --> 앞서 요청했던 학교의 내일 중식을 가져옵니다

날짜를 생략할 경우 기본값은 오늘, 학교 이름을 생략할 경우 기본값은 마지막에 요청했던 학교, 
밥타임(?)을 생략할 경우 기본은 중식을 가져옵니다.

## 로컬에서 실행하기
mealworm5 코드를 자신의 머신에서 직접 실행하고 싶으신가요? 좋습니다. 이 문단을 보고 따라하세요.
### 클론하기
이 리포지토리를 클론하세요. 
### config.ini 작성하기
리포지토리 루트에 있는 config.ini.sample 을 config.ini라는 이름으로 복사하세요. 여러 가지 API 키가 필요합니다.
#### API 키 발급받기
mw5는 여러 가지 API에 의존하기 때문에, API 키가 반드시 필요합니다.  
##### NEIS OpenApi
[나이스 오픈API 포털](https://open.neis.go.kr/portal/mainPage.do)에 접속하여 API 키를 발급받으세요.
##### Facebook Token
Webhook에서 사용하는 ```VERIFY_TOKEN```은 직접 생성해야 합니다. 적정한 길이의 랜덤 토큰을 생성하여 사용하세요.
ACCESS_TOKEN은 Page Access Token을 의미하며, 메세지를 보낼 때 사용됩니다. [문서](https://developers.facebook.com/docs/facebook-login/access-tokens/#pagetokens)를 참고하여 토큰을 발급받고, 권한을 설정하세요.  
##### Dialogflow API 설정하기
DialogFlow 에이전트가 이미 만들어졌다는 가정 하에 진행합니다. 여기까지는 알아서 만들어오세요.  
  
1. [DialogFlow Docs](https://dialogflow.com/docs/reference/v2-auth-setup)를 참고하여 'DialogFlow API Client' Role을 가진 Service Account를 생성합니다. 서비스 계정을 생성 후 인증 정보가 담긴 JSON 파일을 다운로드합니다.
2. Cloud SDK를 설치하고, 현재 프로젝트를 선택합니다. [참고](https://cloud.google.com/sdk/docs/)
3. [여기](https://cloud.google.com/docs/authentication/production?hl=ko#setting_the_environment_variable)를 참고하여 1번에서 다운로드한 JSON의 경로를 환경 변수로 설정합니다.
4. ```gcloud auth application-default print-access-token``` 명령어를 실행합니다. Access Token이 발급됩니다.  
  
API를 호출할 때 인증에 실패하는 경우 서비스 계정에 올바를 Role이 설정되어 있는지 확인하세요.

##### FireStore 인증 설정하기
mw5는 구글 클라이언트 라이브러리를 사용하며, Google Cloud 내의 App Engine에서 호스팅되기 때문에 자동으로 인증을 거칩니다.  
고로, 님이 이걸 돌릴려면  
a. 편하게 개발자랑 똑같은 환경(GAE) 에서 실행합니다.  
b. 홀로 쓸쓸하게 구글 Cloud Docs를 뒤지면서 인증 시스템을 코드에서 수정합니다.  
  
a. 는 당연히 개나 소나 ~~열심히 독스를 찾아서~~ 알아서 하실 수 있을 것이라 믿습니다.  
b. 는 제가 귀찮아서 설명하지 않겠습니다(히힛). 대신 예의상 [링크](https://firebase.google.com/docs/firestore/quickstart?hl=ko#python
) [몇](https://cloud.google.com/docs/authentication/getting-started#command-line) [개](https://cloud.google.com/docs/authentication?hl=ko)를 남겨 놓겠습니다.  
  
아, 왜 DialogFlow는 이런 방식으로 안 했냐고요? 귀찮아서요.  
  
###### 개발자가 빼먹은 경고
app 패키지의 firestore.py 위에 있는 project_id 값을 **변경하세요**. 성능상의 이유로 config.ini 에서 불러오지 않습니다.
### 파이썬 venv 설정하기
venv를 설정하고 ```pip install -r requirements.txt```를 실행하여 프로젝트의 의존성을 설치하세요. mw5는 python3.6 이상 환경만 지원합니다.

### 실행하기
app.py를 실행하세요. ```localhost```에서 서버가 런칭됩니다.  
경고: 프로덕션 환경에서는 반드시 uwsgi나 gunicorn 등의 '제대로 된 서버'를 사용해서 실행하세요. Flask 내장 wsgi 서버로 프로덕션에서 서비스하는 것은 [**매우 멍청한 짓입니다**](https://jhb.kr/358).

## 구현

### 급식 가져오기
~~급식봇은 파이썬의 requests 모듈을 이용해 NEIS를 크롤링해 급식을 가져옵니다.  
학교 코드, 주소 정보를 가져올 때에는 schoolinfo.go.kr 의 API를 사용합니다.~~  
업데이트: [나이스 오픈API](https://open.neis.go.kr/portal/mainPage.do)가 개방되면서 나이스에서 제공하는 API를 사용하도록 개편되었습니다.

### 자연어 처리
급식봇은 자연어 처리 기술을 이용해 정형화된 방식으로 말하지 않아도 요청을 잘 처리할 수 있습니다.  
자연어 처리 엔진으로는 기존에는 마이크로소프트의 [Language Understanding (LUIS)](https://luis.ai/)를 사용하였으나, 지금은 구글의 [Dialogflow](https://dialogflow.com/) 엔진을 이용하고 있습니다. Dialogflow 훈련 자료는 공개되어있지 않습니다.

### 데이터베이스와 유저 관리
급식봇은 아주 멋지고 빠른~~레이턴시가 느려터진~~ [Firestore](https://cloud.google.com/firestore)를 이용해 사용자 데이터를 관리합니다.  
유저 관리에 대해서는 더 이상은 알려고 하면 다칩니다. ~~사실 코드가 더러워서 그랬다 카더라~~  
'급식봇 지원' 기능을 통해 버그 신고, 의견 건의 등의 기능을 구현하였습니다.

## 서버(클라우드) 인프라 구성
급식봇의 모든 처리는 (외부 API 제외) [Google Cloud Platform](https://cloud.google.com/)에서 처리됩니다. 공짜 오예!

## 추후 개발 예정인 기능

- [ ] 급식 구독하기
- [ ] ~~너의 가상 여친~~

## 라이선스
mealworm5 코드는 [WTFPL](http://www.wtfpl.net/) (Do What The Fuck You Want To Public License) 로 배포됩니다. 왜냐고요? 그러게 말입니다...
  
  
-------------------------------------------------------------------
 Made with ♥️ by <img src="https://user-images.githubusercontent.com/30792695/82785153-fc1bf980-9e9c-11ea-84fd-0d331efdd985.png" alt="devvykid" height="20rem">
