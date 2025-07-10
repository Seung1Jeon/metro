import pandas as pd
from data_loader import clean_station_name

def get_available_departures(timetable_dict, line, direction, station, after_time):
    """
    주어진 노선, 방향, 역명, 시각 이후 출발 가능한 열차 정보 반환
    
    Parameters:
        timetable_dict (dict): {(line, direction): pd.DataFrame}
        line (str): 노선명 (예: '1호선')
        direction (str): '상' 또는 '하'
        station (str): 역명
        after_time (datetime.time): 기준 시간

    Returns:
        List[dict]: 출발 가능한 열차 정보 리스트
    """
    station = clean_station_name(station)

    key = (line, direction)
    if key not in timetable_dict:
        print(f"[경고] 해당 노선/방향의 데이터가 없습니다: {key}")
        return []

    df = timetable_dict[key]
    df = df[df['역명'] == station]

    if df.empty:
        print(f"[경고] 해당 역({station})의 데이터가 없습니다.")
        return []

    df = df[df['구분'] == '출발']
    if df.empty:
        print(f"[정보] {station}역에는 '출발' 정보가 없습니다.")
        return []

    time_data = []
    for col in df.columns:
        if col.isdigit():
            try:
                departure_time = pd.to_datetime(df.iloc[0][col], format="%H:%M:%S", errors='coerce')
                if pd.notna(departure_time) and departure_time.time() >= after_time:
                    time_data.append({
                        'train_number': col,
                        'departure_time': departure_time.time()
                    })
            except Exception:
                continue

    return sorted(time_data, key=lambda x: x['departure_time'])

