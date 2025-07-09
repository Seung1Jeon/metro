import pandas as pd
from datetime import datetime, timedelta
import os
import re

DATA_DIR = "data"
DATA_FILES = [
    "대구교통공사_1호선 열차시각표(상선)_20241007.csv",
    "대구교통공사_1호선 열차시각표(하선)_20241007.csv",
    "대구교통공사_2호선 열차시각표(상선)_20241010.csv",
    "대구교통공사_2호선 열차시각표(하선)_20241010.csv",
    "대구교통공사_3호선 열차시각표(상선)_20241007.csv",
    "대구교통공사_3호선 열차시각표(하선)_20241007.csv"
]

# 역명에서 환승역(숫자), 부역명(괄호) 제거
def clean_station_name(name: str) -> str:
    name = re.sub(r'\d+$', '', name)
    name = re.sub(r'\(.*?\)', '', name)
    return name.strip()

# 지정한 역에서 특정 시간 이후에 출발하는 열차 번호의 출발 시각 반환
def get_available_departures(station: str, time_str: str, margin_min=0, limit=None):
    station = clean_station_name(station)
    target_time = datetime.strptime(time_str, "%H:%M:%S") + timedelta(minutes=margin_min)
    result = []

    for file in DATA_FILES:
        path = os.path.join(DATA_DIR, file)
        if not os.path.exists(path):
            continue

        df = pd.read_csv(path, encoding="cp949")
        df['역명'] = df['역명'].astype(str).apply(clean_station_name)

        if station not in df['역명'].values:
            continue

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

        # 지정한 역, 출발 정보, 발차 시각 필터링
        df_filtered = df_long[
            (df_long['역명'] == station) &
            (df_long['구분'] == '출발') &
            (df_long['시각'].dt.time >= target_time.time())
        ][['열차번호', '시각', '방향']]

        for _, row in df_filtered.iterrows():
            result.append({
            '열차번호': row['열차번호'],
            '출발시각': row['시각'],
            '방향': row['방향'],
            '파일명': file
            })

    # 시각 기준 정렬
    result.sort(key=lambda x: x['출발시각'])

    if limit:
        result = result[:limit]

    return result
