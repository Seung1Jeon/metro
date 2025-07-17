# 대구지하철 노선도 앱 (Metro App)

대구교통공사 1선, 2호선, 3선의 실시간 열차 정보와 최적 경로를 제공하는 GUI 애플리케이션입니다.

## 🚇 주요 기능

- **실시간 노선도**: 대구지하철 전체 노선을 시각적으로 표시
- **역 검색**: 역명으로 빠른 검색 및 즐겨찾기 기능
- **최적 경로 탐색**: 출발역과 도착역 간의 최단 경로 및 시간 계산
- **열차 시간표**: 구간별 추천 열차 정보 제공
- **즐겨찾기**: 자주 이용하는 역을 즐겨찾기로 등록
- **최근 검색**: 최근 검색한 역 기록 관리

## 📁 프로젝트 구조

```
metro/
├── build/                          # GUI 애플리케이션
│   ├── gui.py                     # 메인 GUI 애플리케이션
│   └── images/                    # GUI 이미지 파일들
├── data/                          # 대구교통공사 데이터
│   ├── 대구교통공사_1호선 역 구간정보_20241231.csv
│   ├── 대구교통공사_1호선 열차시각표(상선)_20241007.csv
│   ├── 대구교통공사_1호선 열차시각표(하선)_20241007.csv
│   ├── 대구교통공사_2호선 역 구간정보_20241231.csv
│   ├── 대구교통공사_2호선 열차시각표(상선)_20241010.csv
│   ├── 대구교통공사_2호선 열차시각표(하선)_20241010.csv
│   ├── 대구교통공사_3호선 역 구간정보_20241231.csv
│   ├── 대구교통공사_3호선 열차시각표(상선)_20241007.csv
│   └── 대구교통공사_3호선 열차시각표(하선)_20241007                   # 핵심 기능 모듈
│   ├── data_loader.py             # 데이터 로딩 및 전처리
│   ├── route_finder.py            # 경로 탐색 알고리즘
│   ├── path_utils.py              # 경로 유틸리티 함수
│   ├── shortest_path.py           # 최단 경로 알고리즘 (Dijkstra)
│   └── timetable_query.py         # 시간표 조회 기능
├── tests/                         # 테스트 파일들
│   ├── test_case.py               # 기본 테스트 케이스
│   ├── test_gui_integration.py    # GUI 통합 테스트
│   ├── debug_time_issue.py        # 시간 관련 디버깅
│   └── debug_timetable.py         # 시간표 디버깅
├── main.py                        # CLI 버전 메인 실행 파일
├── metro_app_frame.py             # GUI 프레임워크 구조
└── README.md                      # 프로젝트 문서
```

## 🛠️ 기술 스택

- **Python 3.x**: 메인 프로그래밍 언어
- **Tkinter**: GUI 프레임워크
- **PIL (Pillow)**: 이미지 처리
- **Pandas**: 데이터 처리 및 분석
- **NumPy**: 수치 계산

## 📦 설치 및 실행

### 1. 의존성 설치

```bash
pip install pandas pillow numpy
```

### 2. GUI 애플리케이션 실행

```bash
python build/gui.py
```

### 3. CLI 버전 실행

```bash
python main.py
```

## 🎯 사용 방법

### GUI 버전1. **메인 화면**: 노선도에서 역을 클릭하여 출발역/도착역 설정
2. **검색 기능**: 상단 검색창에서 역명 검색
3 **경로 탐색**: 출발역과 도착역 설정 후 최적 경로 확인
4 **즐겨찾기**: 자주 이용하는 역을 즐겨찾기로 등록

### CLI 버전
1. 출발역 입력2. 도착역 입력  
3. 출발 시각 입력 (예: 7:35:00)
4 선택 (distance/time)
5. 최적 경로 및 열차 정보 확인

## 🔧 개발 환경

- **OS**: Windows 10/11 macOS, Linux
- **Python**:37- **IDE**: VS Code, PyCharm 등

## 📊 데이터 출처 및 저작권

본 프로젝트는 [공공데이터포털](https://www.data.go.kr)에서 제공한  
**「대구교통공사\_1호선/2/3호선 역 구간정보」**와 **「대구교통공사\_1호선/2호선/3호선 열차시각표(상행/하행)」** 데이터를 기반으로 제작되었습니다.

- ⓒ 공공데이터포털, 제공기관: **대구교통공사**
- 데이터 라이선스: **공공누리 제1형**
  [공공누리 이용약관 보기](https://www.data.go.kr/ugs/selectPortalPolicyView.do)

해당 프로젝트에 사용된 대구교통공사 CI 이미지는 [대구광역시 공식 홈페이지](https://www.daegu.go.kr/index.do?menu_id=0050251)를 통해 제공된 자료이며,「저작권법 제24조의2」에 따라 자유 이용이 가능한 공공저작물입니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -mAdd some AmazingFeature`)
4.Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 문의사항이나 버그 리포트는 Issues 탭을 이용해 주세요.
