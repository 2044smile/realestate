# realestate

## Why did i make this? 

- 버팀목 전세대출, 보증보험 가능한지 여부는 `매물특징` 에 적혀 있다
- 그 말은 즉, 모든 부동산 매물을 들어가서 `매물특징`을 찾아야 한다는 이야기
- 그리고 저장 된 데이터 (eg. 주차가능 여부, 전세, 가격대, 투룸) 가 초기화 되는 이슈

## How should i make it?

- 추출한 데이터는 `Excel or CSV` 로 저장
- 크롤링으로 하루에 한번 `서초구 투룸 전세` 데이터가 나온다면 그 데이터만 가져온다
- 청년전용 버팀목 전세 자금 대출 3억 대출 한도, 보증보험

## options

- ~~tradTpCds = 전세 `&tradTpCd=B1`~~
- ~~rletTpCds = 단독/다가구, 빌라 `&rletTpCd=DDDGG,VL`~~
- ~~tag = `&tag=TWOROOM,PARKINGYN`~~
- ~~전세가~~
- ~~관리비~~
- ~~3억원 이하~~
- TODO: 주소지 & ~~네이버 맵 바로가기~~
- TODO: 매물 사진
- TODO: 반지하 제외
- TODO: description 에 설명이 없는 매물 제외
- TOOD: 관리비 정보가 없는 매물 제외

![alt text](image.png)

## real distance

- geopy (위도/경도)
- Google maps api

## i am curious

- 공시지가
- 청년전용 보증부월세 대출
- 해당 매물의 공시지가를 확인해서 126% 이하로 전세금이 되야지 보증보험이 가입이 가능하다
- 공동주택 공시가격은 국토교통부에서 운영하는 ['부동산공시가격 알리미'](https://marketer-jinny.tistory.com/entry/%EC%B2%AD%EB%85%84-%ED%97%88%EA%B7%B8-%EB%B2%84%ED%8C%80%EB%AA%A9-%EC%A0%84%EC%84%B8%EC%9E%90%EA%B8%88%EB%8C%80%EC%B6%9C-%EB%B3%B4%EC%A6%9D%EB%B3%B4%ED%97%98-%EA%B3%B5%EC%8B%9C%EC%A7%80%EA%B0%80126-%ED%99%95%EC%9D%B8-%ED%95%84%EC%88%98-I-%EC%A0%84%EC%84%B8%EC%82%AC%EA%B8%B0-%EC%98%88%EB%B0%A9) 라는 사이트에서 확인
