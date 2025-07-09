from data_loader import load_distance_graph, load_time_graph, clean_station_name, load_line_station_map
from shortest_path import dijkstra_distance, dijkstra_time


# 경유역 미포함
def find_route(start_station: str, end_station: str, mode='distance'):
    start_station = clean_station_name(start_station) # 시작역
    end_station = clean_station_name(end_station) # 종착역

    # 최소 시간/최소 거리 조건 분기
    if mode == 'time':
        graph = load_time_graph()
        dijkstra_func = dijkstra_time
    else:    
        graph = load_distance_graph()
        dijkstra_func = dijkstra_distance
    
    # 역명 존재 여부 판별
    if start_station not in graph:
        raise ValueError(f"출발역 '{start_station}' 이(가) 존재하지 않습니다.")
    if end_station not in graph:
        raise ValueError(f"도착역 '{end_station}' 이(가) 존재하지 않습니다.")

    cost, path = dijkstra_func(graph, start_station, end_station)
    return cost, path

# 경유역 포함
def find_route_with_stops(start: str, stops: list[str], mode='distance'):
    # 최소 시간/최소 거리 조건 분기
    if mode == 'time':
        graph = load_time_graph()
        dijkstra_func = dijkstra_time
    else:
        graph = load_distance_graph()
        dijkstra_func = dijkstra_distance

    all_stations = [clean_station_name(st) for st in [start] + stops]
    total_cost = 0
    total_path = []

    for i in range(len(all_stations) - 1):
        s = all_stations[i]
        e = all_stations[i + 1]

        if s not in graph:
            raise ValueError(f"경유 출발역 '{s}' 이(가) 존재하지 않습니다.")
        if e not in graph:
            raise ValueError(f"경유 도착역 '{e}' 이(가) 존재하지 않습니다.")

        cost, path = dijkstra_func(graph, s, e)
        total_cost += cost

        # 첫 경로는 전체를 넣고 다음 경로는 시작역 중복을 제거하고 이음
        if i == 0:
            total_path.extend(path)
        else:
            total_path.extend(path[1:])

    return total_cost, total_path

def infer_direction(path: list[str]) -> dict[str, str]:
    """
    path에 기반하여 노선별 상/하행 판단

    Returns:
        {'2호선': '상', '1호선': '하', ...}
    """
    direction_info = {}
    line_station_map = load_line_station_map()

    for line, stations in line_station_map.items():
        # 해당 노선에 포함된 path 내 역들만 추출
        on_line = [station for station in path if station in stations]

        if len(on_line) >= 2:
            start_idx = stations.index(on_line[0])
            end_idx = stations.index(on_line[-1])
            direction_info[line] = '상' if end_idx > start_idx else '하'

    return direction_info