from path_utils import find_route, find_route_with_stops, infer_direction
from timetable_query import get_available_departures
from data_loader import clean_station_name, load_line_station_map
from datetime import timedelta, datetime
import pandas as pd

def find_best_route(start: str, end: str, via_stations=None, mode='distance', start_time=None):
    """
    최소 거리/최소 시간 기반 경로 탐색 + 출발 시각 보조 기능

    Args:
        start (str): 출발역
        end (str): 도착역
        via_stations (list[str] | None): 경유역 리스트
        mode (str): 'distance' 또는 'time'
        start_time (str | None): 출발 시각 (예: '07:35')

    Returns:
        tuple: (총 비용, 경로 리스트)
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

    if start_time:
        try:
            # 출발역이 포함된 노선 중 가장 관련성 높은 노선 선택
            target_line = None
            for line, dir in direction_info.items():
                if start in load_line_station_map()[line]:  # 출발역 포함되는 노선이면 우선 사용
                    target_line = line
                    direction = dir
                    break

            if target_line and direction:
                nearest = get_available_departures(
                    start, start_time,
                    line=target_line,
                    direction=direction,
                    limit=5
                )

                print(f"\n'{start}'역 기준 {start_time} 이후 가장 빠른 열차 목록 (상위 5개):")
                for i, row in enumerate(nearest, 1):
                    depart_time = row['출발시각']

                    if mode == 'time':
                        # 총 소요 시간은 초 단위이므로 timedelta 사용
                        arrival_time = depart_time + timedelta(seconds=total_cost)
                        print(f"{i:02d}. 열차번호: {row['열차번호']} | 시각: {depart_time.time()} → 도착 예정: {arrival_time.time()} | 방향: {row['방향']} | 파일: {row['파일명']}")
                    else:
                        print(f"{i:02d}. 열차번호: {row['열차번호']} | 시각: {depart_time.time()} | 방향: {row['방향']} | 파일: {row['파일명']}")
            else:
                print("방향 정보가 불충분하여 추천 열차 필터링을 건너뜁니다.")

        except Exception as e:
            print(f"출발 시각 추천 기능 실패: {e}")

    return total_cost, path

def recommend_trains_by_segments(segments, start_time_str="07:00:00"):
    print("\n🚇 구간별 열차 추천:")
    current_time = datetime.strptime(start_time_str, "%H:%M:%S")

    for segment in segments:
        line = segment['line']
        direction = segment['direction']
        stations = segment['stations']

        if len(stations) < 2:
            continue  # 역이 하나뿐이면 생략

        start_station = stations[0]
        end_station = stations[-1]

        # 열차 정보 조회
        departures = get_available_departures(
            station=start_station,
            time_str=current_time.strftime("%H:%M:%S"),
            line=line,
            direction=direction,
            limit=1
        )

        if not departures:
            print(f"[{line}] {start_station} → {end_station} | 🚫 열차 없음")
            continue

        train = departures[0]
        departure_time = train['출발시각']

        if isinstance(departure_time, pd.Timestamp):
            departure_time = departure_time.to_pydatetime()

        # 소요 시간 추정 (향후 실제 계산으로 교체 가능)
        travel_minutes = segment.get('duration', 0) or 20
        arrival_time = departure_time + timedelta(minutes=travel_minutes)

        print(
            f"[{line}] {start_station} → {end_station} | 열차번호: {train['열차번호']} "
            f"| 출발: {departure_time.strftime('%H:%M:%S')} → 도착: {arrival_time.strftime('%H:%M:%S')} "
            f"| 방향: {direction}"
        )

        current_time = arrival_time + timedelta(minutes=2)  # 환승 대기시간 고려