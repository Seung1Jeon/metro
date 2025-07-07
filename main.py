from data_loader import load_total_graph
from dijkstra import dijkstra

graph = load_total_graph()

start_station = '설화명곡'
end_station = '안심'

distance, path = dijkstra(graph, start_station, end_station)

print(f'최단 거리: {distance:.2f} km')
print('경로:', ' → '.join(path))