from data_loader import load_total_graph
from shortest_path import dijkstra

graph = load_total_graph()

start_station = '설화명곡'
end_station = '안심'

if start_station not in graph:
    raise ValueError(f"출발역 '{start_station}' 이(가) 존재하지 않습니다.")

if end_station not in graph:
    raise ValueError(f"도착역 '{end_station}' 이(가) 존재하지 않습니다.")

distance, path = dijkstra(graph, start_station, end_station)

print(f'최단 거리: {distance:.2f} km')
print('경로:', ' → '.join(path))