from path_utils import find_route, find_route_with_stops
from timetable_query import get_available_departures
from data_loader import clean_station_name

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

    # 출발 시각 기반 보조 기능
    if start_time:
        try:
            nearest = get_available_departures(start, start_time, limit=5)
            print(f"\n'{start}'역 기준 {start_time} 이후 가장 빠른 열차 목록 (상위 5개):")
            for i, row in enumerate(nearest, 1):
                print(f"{i:02d}. 열차번호: {row['열차번호']} | 시각: {row['출발시각'].time()} | 방향: {row['방향']} | 파일: {row['파일명']}")
        except Exception as e:
            print(f"출발 시각 추천 기능 실패: {e}")

    # 경유역 여부에 따라 분기
    if via_stations:
        return find_route_with_stops(start, via_stations + [end], mode)
    else:
        return find_route(start, end, mode)