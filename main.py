from data_loader import load_total_graph, clean_station_name
from shortest_path import dijkstra

# 경유역 미포함
def find_route(start_station: str, end_station: str):
    graph = load_total_graph()
    start_station = clean_station_name(start_station) # 시작역
    end_station = clean_station_name(end_station) # 종착역

    if start_station not in graph:
        raise ValueError(f"출발역 '{start_station}' 이(가) 존재하지 않습니다.")
    if end_station not in graph:
        raise ValueError(f"도착역 '{end_station}' 이(가) 존재하지 않습니다.")

    distance, path = dijkstra(graph, start_station, end_station)
    return distance, path

# 경유역 포함
def find_route_with_stops(start: str, stops: list[str]):
    graph = load_total_graph()
    all_stations = [start] + stops

    all_stations = [clean_station_name(st) for st in all_stations]

    total_distance = 0
    total_path = []

    for i in range(len(all_stations) - 1):
        s = all_stations[i]
        e = all_stations[i + 1]

        if s not in graph:
            raise ValueError(f"경유 출발역 '{s}' 이(가) 존재하지 않습니다.")
        if e not in graph:
            raise ValueError(f"경유 도착역 '{e}' 이(가) 존재하지 않습니다.")

        distance, path = dijkstra(graph, s, e)
        total_distance += distance

        # 첫 경로는 전체를 넣고 다음 경로는 시작역 중복을 제거하고 이음
        if i == 0:
            total_path.extend(path)
        else:
            total_path.extend(path[1:])

    return total_distance, total_path
