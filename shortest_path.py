import heapq
# 파이썬 표준 라이브러리 중 하나인 heapq 모듈을 사용하여 다익스트라 최단 경로 알고리즘 구현

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}
    distances[start] = 0 # 시작 노드 0으로 설정
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # 경로 추적
    path = []
    current = end
    while current:
        path.insert(0, current)
        current = previous_nodes[current]

    return distances[end], path