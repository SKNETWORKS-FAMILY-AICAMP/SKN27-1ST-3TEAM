---
marp: true
theme: default
paginate: true
---
# 현대 친환경차 등록 현황 및 FAQ 조회 시스템

### SKN27-1ST-3TEAM

김한솔 · 이혜림 · 김재묵 · 김주영 · 김필주 · 박준희

---

# "6도의 멸종"을 아시나요?

<img src="https://contents.kyobobook.co.kr/sih/fit-in/458x0/pdt/9788984074491.jpg" width="300px" align="right">

- 2024년 평균기온 10년 대비 1.28℃ 상승
- 수송 부문 CO₂ 배출 감소하지 않음
- 자동차 등록 대수 지속 증가
- 친환경차 비율은 여전히 낮은 수준

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
  ## 분석기업
- 현대

---

# ERD

<img width="2800" height="500" alt="005" src="https://postfiles.pstatic.net/MjAyNjAyMjZfMjgz/MDAxNzcyMDgwMzkyMTk1.NMEMIofpgO0WqU11OU0sxgRWUpKJeNwJ3aS-4l6JKQcg.UTPaQ89fqKkvQN8fc2e0_zRVM739MqWzxAYf17cRl6Eg.PNG/erd.png?type=w966">



hydrogen_regional # 2025년 12월 기준 시도별 수소차 등록대수
https://h2hub.or.kr/main/yard/domestic-hydrogen-vehicle-registration-status-yearly.do
수소경제 종합 정보 포털

ev_registration # 시도별 연도별 전기차 등록대수, 핵심 중심 테이블
https://chargeinfo.ksga.org/front/statistics/evCar/
차지인포

charger_yearly # 연도별 권역별 전기차 충전소 수
https://chargeinfo.ksga.org/front/statistics/charger
차지인포

temperature_yearly # 연도별 전국 평균기온
https://data.kma.go.kr/climate/RankState/selectRankStatisticsDivisionList.do
기상청 기상자료개방포털

total_vehicle_yearly # 연도별 전체 자동차 등록 대수
https://stat.molit.go.kr/portal/cate/statView.do?hRsId=58&hFormId=1244&hSelectId=5559&hPoint=00&hAppr=1&hDivEng=&oFileName=&rFileName=&midpath=&sFormId=1244&sStyleNum=1&settingRadio=xlsx
국토교통 통계누리

subsidy #2026 지자체별 전기차 + 수소차 보조금
https://ev.or.kr/nportal/buySupprt/initPsLocalCarPirceAction.do
무공해차 통합누리집

transport_co2 # 시도별 연도별 수송 CO2 배출량
https://www.gir.go.kr/home/index.do?menuId=36
기후에너지환경부 온실가스 종합정보센터

---

# 마무리
