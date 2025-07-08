import pandas as pd
# 데이터 가공을 위한 pandas 모듈 사용
from collections import defaultdict
# 파이썬의 자료형(list, tuple, set, dict)에 대한 대안을 제공하는 collections 모듈 사용
# defaultdict(): 누락된 값을 제공하기 위해 팩토리 함수를 호출
import re
# 정규 표현식을 사용하기 위한 파이썬 내장 모듈인 re 모듈 사용

# csv 파일 내의 환승역 명칭(환승역+번호)을 통일하기 위한 함수
def clean_station_name(name: str) -> str:
    return re.sub(r'\d+$', '', name).strip()

# csv 파일을 읽어 그래프를 생성하는 함수
def build_graph_from_csv(file_path, encoding='cp949'):
    df = pd.read_csv(file_path, encoding=encoding)
    graph = {}
    stations = df['역명'].dropna().tolist()
    distances = df['하행키로'].tolist()

    for i in range(len(stations) - 1):
        curr = clean_station_name(stations[i])
        next_ = clean_station_name(stations[i + 1])
        distance = distances[i + 1]

        graph.setdefault(curr, {})[next_] = distance
        graph.setdefault(next_, {})[curr] = distance

    return graph

# 전체 노선을 통합하는 그래프를 생성하는 함수
def load_total_graph():
    # 공공데이터포털 대구지하철 구간정보
    files = [
        'data/대구교통공사_1호선 역 구간정보_20241231.csv',
        'data/대구교통공사_2호선 역 구간정보_20241231.csv',
        'data/대구교통공사_3호선 역 구간정보_20241231.csv'
    ]

    total_graph = defaultdict(dict)

    for file in files:
        g = build_graph_from_csv(file)
        for station, neighbors in g.items():
            total_graph[station].update(neighbors)

    return dict(total_graph)

# 환승역
TRANSFER_STATIONS = {
    '반월당': ['1호선', '2호선'],
    '명덕': ['1호선', '3호선'],
    '청라언덕': ['2호선', '3호선']
}

# 역이 환승역인지 확인하는 함수
def is_transfer_station(station_name):
    return clean_station_name(station_name) in TRANSFER_STATIONS

