---
marp: true
theme: default
paginate: true
---
# 전기 환경차 등록 현황 및 현대 FAQ 조회 시스템

---

# 팀소개

---

### 1-1. 팀원 소개

| 팀원1  | 팀원2  | 팀원3  | 팀원4  | 팀원5  | 팀원6  |
| ------ | ------ | ------ | ------ | ------ | ------ |
|        |        |        |        |        |        |
| 김한솔 | 김주영 | 김재묵 | 김필주 | 박준희 | 이혜림 |

# 2. 프로젝트 개요

---

## 2-1. 프로젝트 명

---

#### 한국 전기차 보급과 탄소배출과 기온의 분석과 인프라 격차 & 보조금 정책 분석과 현대 FAQ

## 2-2. 프로젝트 소개

---

#### "6도의 멸종"을 아시나요?

<img src="https://contents.kyobobook.co.kr/sih/fit-in/458x0/pdt/9788984074491.jpg" width="300px" align="right">

- 2024년 평균기온 10년 대비 1.28℃ 상승
- 수송 부문 CO₂ 배출 감소하지 않음
- 자동차 등록 대수 지속 증가
- 친환경차 비율은 여전히 낮은 수준

## 2-2. 프로젝트 소개

---

## 2-3. 프로젝트 배경

---

## 2-4. 프로젝트 목표.

---


## 2-5. 기대 효과

---





# 3. 기술 스택

---





# 4. WBS (작업 분할 구조)

---





# 5. 데이터 분석 및 전처리 (EDA)

---



## 5-1. 활용 데이터

---





## 5-2. 주요 전처리 내용

---




# 6. 수행 결과 (Streamlit 대시보드)

---



## 주요 기능

---





# 7. 개발 중 주요 이슈 및 해결

---





# 8. 한계점 및 향후 과제
한계점 및 향후 과제

1. 실시간 연동의 부재 → 실시간 데이터 처리 구조 개선 필요
현재 시스템은 정적 데이터 기반으로 동작하여 데이터가 즉각적으로 반영되지 않는 한계가 있습니다. 향후에는 API 연동 또는 주기적 크롤링 및 자동 갱신 로직을 적용하여 데이터가 실시간으로 업데이트될 수 있도록 개선할 계획입니다. 이를 통해 서비스의 신뢰성과 활용도를 높이고자 합니다.

2. UI 구성의 단순 나열 구조 → 사용자 중심 인터페이스 개선 필요
그래프가 화면 하단으로 단순 나열되어 가독성이 떨어지는 문제가 있습니다. 향후에는 상단 메뉴바 또는 사이드바를 활용하여 사용자가 원하는 그래프만 선택적으로 확인할 수 있도록 구조를 개선할 예정입니다. 이는 사용자 경험을 향상시키는 중요한 개선 요소입니다.

3. 목적 설계의 구체성 부족 → 명확한 타겟 및 목표 설정 필요
프로젝트의 목표와 타겟이 다소 포괄적으로 설정되어 있어 기능 설계의 방향성이 분산되는 경향이 있습니다. 향후에는 구체적인 사용자 타겟과 핵심 목표를 명확히 정의하여, 그에 맞는 기능 중심으로 발전시킬 계획입니다. 이는 서비스 완성도를 높이기 위한 중요한 과제입니다.

---




# 9. 한 줄 회고

이혜림 - 이번 프로젝트를 통해 순서와 절차의 중요성, 그리고 그것을 미리 계획하는 일이 더욱 중요하다는 것을 깨달았습니다. 미래를 알 수는 없지만, 대비하고 방향을 설정해두면 이후 과정에서 발생하는 문제도 무리 없이 해결할 수 있다는 점을 배웠습니다. 또한 협업에서는 내가 무엇을 할지보다, 내가 어떤 방향으로 가고 있는지를 아는 것이 더 중요하다는 것을 다시 한 번 느끼게 되었습니다.

---




# 프로젝트 목적 및 해결 방향

## 목적

- 기온 · CO₂ · 자동차 등록 · 충전 인프라 · 보조금 데이터를 통합 분석하는 대시보드 구축

## 해결 방법

- 공공데이터 통합
- 시각화 기반 비교 분석
- 정책 효과 및 지역 격차 검증

---

# 프로젝트 분석 대상 및 대상 사용자

## 사용자 대상

- 전기차 구매를 고려하는 일반 소비자→ 지역 인프라·보조금 비교 제공
- 정책 및 시장 흐름에 관심 있는 사용자→ 전기차 보급과 탄소배출, 정책 효과 분석 가능

  ##분석기업
- 현대

---

# ERD

<img width="2800" height="500" alt="005" src="https://postfiles.pstatic.net/MjAyNjAyMjZfMjgz/MDAxNzcyMDgwMzkyMTk1.NMEMIofpgO0WqU11OU0sxgRWUpKJeNwJ3aS-4l6JKQcg.UTPaQ89fqKkvQN8fc2e0_zRVM739MqWzxAYf17cRl6Eg.PNG/erd.png?type=w966">

---

hydrogen_regional 테이블# 2025년 12월 기준 시도별 수소차 등록대수
https://h2hub.or.kr/main/yard/domestic-hydrogen-vehicle-registration-status-yearly.do
수소경제 종합 정보 포털

ev_registration 테이블# 시도별 연도별 전기차 등록대수, 핵심 중심 테이블
https://chargeinfo.ksga.org/front/statistics/evCar/
차지인포

charger_yearly 테이블# 연도별 권역별 전기차 충전소 수
https://chargeinfo.ksga.org/front/statistics/charger
차지인포

temperature_yearly 테이블# 연도별 전국 평균기온
https://data.kma.go.kr/climate/RankState/selectRankStatisticsDivisionList.do
기상청 기상자료개방포털

---

total_vehicle_yearly 테이블 # 연도별 전체 자동차 등록 대수
https://stat.molit.go.kr/portal/cate/statView.do?hRsId=58&hFormId=1244&hSelectId=5559&hPoint=00&hAppr=1&hDivEng=&oFileName=&rFileName=&midpath=&sFormId=1244&sStyleNum=1&settingRadio=xlsx
국토교통 통계누리

subsidy 테이블 #2026 지자체별 전기차 + 수소차 보조금
https://ev.or.kr/nportal/buySupprt/initPsLocalCarPirceAction.do
무공해차 통합누리집

transport_co2 테이블 # 시도별 연도별 수송 CO2 배출량
https://www.gir.go.kr/home/index.do?menuId=36
기후에너지환경부 온실가스 종합정보센터
