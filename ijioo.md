# 커밋 메세지 
## 규칙

1. 제목과 본문 두 줄 띄어 구분
2. 제목 subject
	50자 이내
	첫 글자는 영어로 할 시 대문자
	끝 마침표 X
	명령문O, 과거형X
3. 본문 body
	각 행은 72자 이내(넘어가면 줄바꿈)
	무엇을, 왜에 대하여 설명

## 구조
<type>(<scope>): <subject> #제목
<BLANK LINE>
<body> #본문
<BLANK LINE>
<footer>
제목은 필수

## 제목
Type : 제목
ex - feat : Add login api #로그인 API 추가

### Type
feat : 새로운 기능 추가, 기존 기능 요구사항에 맞춰 수정
fix : 기능에 대한 버그 수정
build : 빌드 관련 수정
chore : 패키지 매니저 수정, 기타
ci : CI 관련
docs : 문서, 주석 수정
style : 코드 스타일, 포맷팅에 대한 수정
refactor : 코드 리팩터링, 기능 변화 X(ex-변수 이름 변경 등)
test : 테스트 코드 추가/ 수정
release : 버전 릴리즈

## 본문
제목으로 표현 가능하면 생략 가능
아닌 경우 자세한 내용 작성

## 꼬리말
어떤 이슈에 대한 commit인지 작성, issue number 포함(#1)
이슈가 끝날 때 close #1

- 전처리과정
    데이터 전처리
        텍스트 전처리 (Text preprocessing)
        형태소 분석
        제외할 단어 코드 작성
        수정 사항
        벡터화 (Vectorization)
            CountVectorizer
            TF-IDF Vectorizer

- 분석 모델링