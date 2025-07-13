import pandas as pd
from data_loader import clean_station_name

def get_available_departures(
    timetable_dict,
    line,
    direction,
    station,
    next_station=None,
    prev_station=None,
    time_str=None
):
    """
    특정 역에서 주어진 시각 이후의 열차 출발 정보를 반환합니다.
    기점/종점 예외를 포함해 '도착' 시각을 출발 시각으로 간주하거나,
    이전 역의 도착 시각을 대신 사용하는 처리를 포함합니다.
    """
    import pandas as pd

    try:
        timetable_df = timetable_dict[(line, direction)]
    except KeyError:
        print(f"[오류] 노선({line}) 방향({direction})의 시각표 데이터가 없습니다.")
        return pd.DataFrame()

    # 출발 시각은 기본적으로 해당 역의 '출발' 구분만 필터링
    departures = timetable_df[
        (timetable_df['역명'] == station) & 
        (timetable_df['구분'] == '출발')
    ].copy()

    # 출발 시각이 없고 '도착'만 있는 경우 → csv 파일 기준 기점역
    if departures.empty:
        possible_departure = timetable_df[
            (timetable_df['역명'] == station) & 
            (timetable_df['구분'] == '도착')
        ].copy()
        if not possible_departure.empty:
            print(f"[⚠️ 기점역 처리] '{station}'역은 도착 시각만 존재 → 출발 시각으로 간주합니다.")
            departures = possible_departure.copy()

    # 종점역의 경우 출발 시각이 없고 이전역 도착 시각으로 대체
    if departures.empty and prev_station:
        arrivals_at_prev = timetable_df[
            (timetable_df['역명'] == prev_station) & 
            (timetable_df['구분'] == '도착')
        ].copy()
        if not arrivals_at_prev.empty:
            print(f"[⚠️ 종점역 처리] '{station}'역의 출발 시각이 없어서 이전역('{prev_station}') 도착 시각을 대체합니다.")
            departures = arrivals_at_prev.copy()

    # 주어진 시각 이후 열차만 필터링
    if time_str:
        departures = departures[departures['시각'] >= time_str]

    # 시각 기준 정렬
    return departures.sort_values(by='시각')
