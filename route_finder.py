from path_utils import find_route, find_route_with_stops, infer_direction
from timetable_query import get_available_departures
from data_loader import clean_station_name, load_line_station_map, prepare_timetable_long_format_dict
from datetime import timedelta, datetime
import pandas as pd

def find_best_route(start: str, end: str, via_stations=None, mode='distance', start_time=None):
    """
    최소 거리/최소 시간 기반 경로 탐색 + 출발 시각 보조 기능
    """
    start = clean_station_name(start)
    end = clean_station_name(end)
    via_stations = [clean_station_name(st) for st in via_stations] if via_stations else []

    # 경유역 여부에 따라 분기
    if via_stations:
        total_cost, path = find_route_with_stops(start, via_stations + [end], mode)
    else:
        total_cost, path = find_route(start, end, mode)

    # 방향 추론
    direction_info = infer_direction(path)

    # 출발 시각 기반 추천 기능
    if start_time:
        try:
            target_line = None
            direction = None
            for line, dir in direction_info.items():
                if start in load_line_station_map()[line]:
                    target_line = line
                    direction = dir
                    break

            if target_line and direction:
                timetable_dict = prepare_timetable_long_format_dict()
                after_time = datetime.strptime(start_time, "%H:%M:%S").time()

                nearest = get_available_departures(
                    timetable_dict,
                    target_line,
                    direction,
                    start,
                    after_time
                )

                print(f"\n'{start}'역 기준 {start_time} 이후 가장 빠른 열차 목록 (상위 5개):")
                for i, row in enumerate(nearest[:5], 1):
                    depart_time = row['departure_time']
                    if mode == 'time':
                        arrival_time = datetime.combine(datetime.today(), depart_time) + timedelta(seconds=total_cost)
                        print(f"{i:02d}. 열차번호: {row['train_number']} | 시각: {depart_time} → 도착 예정: {arrival_time.time()} | 방향: {direction}")
                    else:
                        print(f"{i:02d}. 열차번호: {row['train_number']} | 시각: {depart_time} | 방향: {direction}")
            else:
                print("방향 정보가 불충분하여 추천 열차 필터링을 건너뜁니다.")
        except Exception as e:
            print(f"출발 시각 추천 기능 실패: {e}")

    return total_cost, path


def recommend_trains_by_segments(segments, start_time_str="07:00:00"):
    """
    각 구간(segment)별로 다음 열차를 추천
    """
    print("\n🚇 구간별 열차 추천:")
    current_time = datetime.strptime(start_time_str, "%H:%M:%S")
    timetable_dict = prepare_timetable_long_format_dict()

    for segment in segments:
        line = segment['line']
        direction = segment['direction']
        stations = segment['stations']

        if len(stations) < 2:
            continue

        start_station = stations[0]
        end_station = stations[-1]

        departures = get_available_departures(
            timetable_dict,
            line,
            direction,
            start_station,
            current_time.time()
        )

        if departures.empty:
            print(f"[{line}] {start_station} → {end_station} | 🚫 열차 없음")
            continue

        train = departures.iloc[0]
        departure_time = datetime.combine(datetime.today(), train['시각'].time())

        travel_minutes = segment.get('duration', 0) or 20
        arrival_time = departure_time + timedelta(minutes=travel_minutes)

        print(
            f"[{line}] {start_station} → {end_station} | 열차번호: {train['열차번호']} "
            f"| 출발: {departure_time.strftime('%H:%M:%S')} → 도착: {arrival_time.strftime('%H:%M:%S')} "
            f"| 방향: {direction}"
        )

        current_time = arrival_time + timedelta(minutes=2)  # 환승 시간 고려