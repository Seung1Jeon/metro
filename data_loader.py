import pandas as pd
# 데이터 가공을 위한 pandas 모듈 사용
from collections import defaultdict
# 파이썬의 자료형(list, tuple, set, dict)에 대한 대안을 제공하는 collections 모듈 사용
# defaultdict(): 누락된 값을 제공하기 위해 팩토리 함수를 호출
import re
# 정규 표현식을 사용하기 위한 파이썬 내장 모듈인 re 모듈 사용
import os
# 파일 생성, 수정, 삭제, 디렉토리 작업을 수행하기 위한 os 모듈

# 정제 함수
# csv 파일 내의 환승역 명칭(환승역+번호)을 통일하고 부역명(괄호 부기)을 제거하기 위한 함수
def clean_station_name(name: str) -> str:
    name = re.sub(r'\d+$', '', name) # 숫자 제거 (ex. 반월당1 → 반월당, 반월당2 → 반월당)
    name = re.sub(r'\(.*?\)', '', name) # 괄호 제거 (ex. 용산(달서구) → 용산)
    return name.strip()

# 거리 기반 그래프
# 전체 노선을 통합하는 그래프를 생성하는 함수
def load_distance_graph():
    # 공공데이터포털 대구지하철 구간정보
    files = [
        'data/대구교통공사_1호선 역 구간정보_20241231.csv',
        'data/대구교통공사_2호선 역 구간정보_20241231.csv',
        'data/대구교통공사_3호선 역 구간정보_20241231.csv'
    ]
    graph = defaultdict(dict)

    for file_path in files:
        df = pd.read_csv(file_path, encoding='cp949')
        stations = df['역명'].dropna().astype(str).apply(clean_station_name).tolist()
        distances = df['하행키로'].tolist()
        for i in range(len(stations) - 1):
            curr, next_ = stations[i], stations[i + 1]
            distance = distances[i + 1]
            if pd.notna(distance):
                graph[curr][next_] = distance
                graph[next_][curr] = distance
    return dict(graph)

# 시각표 처리 및 그래프 생성
def load_timetable_long_format(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, encoding="cp949")
    df['역명'] = df['역명'].astype(str).apply(clean_station_name)
    df[['요일', '방향']] = df['요일별'].str.extract(r'(\w+)\((\w)\)')

    df_long = pd.melt(
        df,
        id_vars=["요일별", "역명", "구분", "요일", "방향"],
        var_name="열차번호",
        value_name="시각"
    )
    df_long.dropna(subset=['시각'], inplace=True)
    df_long['시각'] = pd.to_datetime(df_long['시각'], format="%H:%M:%S", errors='coerce')
    df_long.dropna(subset=['시각'], inplace=True)

    df_long.sort_values(by=['열차번호', '요일', '방향', '시각'], inplace=True)
    return df_long

def calculate_segment_travel_time(df_long: pd.DataFrame, include_stop_time: bool = False) -> pd.DataFrame:
    df = df_long.copy()

    # 이동 시간 계산용 정보
    df['다음_역명'] = df['역명'].shift(-1)
    df['다음_구분'] = df['구분'].shift(-1)
    df['다음_시각'] = df['시각'].shift(-1)
    df['다음_열차번호'] = df['열차번호'].shift(-1)
    df['다음_요일'] = df['요일'].shift(-1)
    df['다음_방향'] = df['방향'].shift(-1)

    # 정차 시간 계산용 정보
    df['이전_역명'] = df['역명'].shift(1)
    df['이전_구분'] = df['구분'].shift(1)
    df['이전_시각'] = df['시각'].shift(1)
    df['이전_열차번호'] = df['열차번호'].shift(1)
    df['이전_요일'] = df['요일'].shift(1)
    df['이전_방향'] = df['방향'].shift(1)

    # 이동 시간 조건
    move_cond = (
        (df['구분'] == '출발') &
        (df['다음_구분'] == '도착') &
        (df['열차번호'] == df['다음_열차번호']) &
        (df['요일'] == df['다음_요일']) &
        (df['방향'] == df['다음_방향']) &
        (df['역명'] != df['다음_역명'])
    )

    # 이동 시간: 다음 역의 도착 시간에서 이전 역의 출발 시각을 뺸 값
    df['이동_시간'] = (df['다음_시각'] - df['시각']).dt.total_seconds()

    if include_stop_time:
        # 정차 시간 조건
        stop_cond = (
            (df['구분'] == '출발') &
            (df['이전_구분'] == '도착') &
            (df['열차번호'] == df['이전_열차번호']) &
            (df['요일'] == df['이전_요일']) &
            (df['방향'] == df['이전_방향']) &
            (df['역명'] == df['이전_역명'])
        )
        # 정차 시간: 동일 역명의 도착 시각에서 동일 역명의 출발 시각 사이의 값
        df['정차_시간'] = (df['시각'] - df['이전_시각']).dt.total_seconds()
        # 총 소요 시간 = 이동 + 정차
        df['소요시간(초)'] = df['이동_시간'] + df['정차_시간']
        final_cond = move_cond & stop_cond
    else:
        # 정차 시간 없이 이동 시간만 반영하기
        df['소요시간(초)'] = df['이동_시간']
        final_cond = move_cond

    df_result = df.loc[final_cond, ['역명', '다음_역명', '소요시간(초)']].copy()
    df_result.rename(columns={'역명': '출발역', '다음_역명': '도착역'}, inplace=True)
    return df_result

# 모든 CSV 파일 통합 → 평균 소요시간 계산
def build_travel_time_graph(include_stop_time: bool = False):
    files = [
        "data/대구교통공사_1호선 열차시각표(상선)_20241007.csv",
        "data/대구교통공사_1호선 열차시각표(하선)_20241007.csv",
        "data/대구교통공사_2호선 열차시각표(상선)_20241010.csv",
        "data/대구교통공사_2호선 열차시각표(하선)_20241010.csv",
        "data/대구교통공사_3호선 열차시각표(상선)_20241007.csv",
        "data/대구교통공사_3호선 열차시각표(하선)_20241007.csv"
    ]
    all_segments = []
    for f in files:
        if os.path.exists(f):
            df_long = load_timetable_long_format(f)
            df_seg = calculate_segment_travel_time(df_long, include_stop_time)
            all_segments.append(df_seg)
    df_all = pd.concat(all_segments)
    df_avg = df_all.groupby(['출발역', '도착역'])['소요시간(초)'].mean().reset_index()

    graph = defaultdict(dict)
    for _, row in df_avg.iterrows():
        s, e, t = row['출발역'], row['도착역'], row['소요시간(초)']
        graph[s][e] = t
        graph[e][s] = t
    return dict(graph)

# 환승역
TRANSFER_STATIONS = {
    '반월당': ['1호선', '2호선'],
    '명덕': ['1호선', '3호선'],
    '청라언덕': ['2호선', '3호선']
}

# 역이 환승역인지 확인하는 함수
def is_transfer_station(station_name):
    return clean_station_name(station_name) in TRANSFER_STATIONS

# 역 구간정보 csv 파일에서 역 정보만 추출하여 리스트에 저장
def load_line_station_map() -> dict:
    files = [
        'data/대구교통공사_1호선 역 구간정보_20241231.csv',
        'data/대구교통공사_2호선 역 구간정보_20241231.csv',
        'data/대구교통공사_3호선 역 구간정보_20241231.csv'
    ]
    line_map = {}
    for file in files:
        match = re.search(r'(\d호선)', file)
        if match:
            line_name = match.group(1)
            df = pd.read_csv(file, encoding='cp949')
            stations = df['역명'].dropna().astype(str).apply(clean_station_name).tolist()
            line_map[line_name] = stations
    return line_map

def prepare_timetable_long_format_dict():
    """
    전체 노선별 시각표를 long format으로 가공하여 (노선, 방향) -> DataFrame 구조로 반환
    """
    timetable_files = {
        ('1호선', '상'): "대구교통공사_1호선 열차시각표(상선)_20241007.csv",
        ('1호선', '하'): "대구교통공사_1호선 열차시각표(하선)_20241007.csv",
        ('2호선', '상'): "대구교통공사_2호선 열차시각표(상선)_20241010.csv",
        ('2호선', '하'): "대구교통공사_2호선 열차시각표(하선)_20241010.csv",
        ('3호선', '상'): "대구교통공사_3호선 열차시각표(상선)_20241007.csv",
        ('3호선', '하'): "대구교통공사_3호선 열차시각표(하선)_20241007.csv",
    }

    base_dir = "./data"
    result = {}

    for (line, direction), fname in timetable_files.items():
        full_path = os.path.join(base_dir, fname)
        if os.path.exists(full_path):
            df_long = load_timetable_long_format(full_path)
            result[(line, direction)] = df_long
        else:
            print(f"[경고] 누락된 시각표 파일: {full_path}")

    return result
