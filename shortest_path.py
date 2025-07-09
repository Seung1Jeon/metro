import heapq
# 파이썬 표준 라이브러리 중 하나인 heapq 모듈을 사용하여 다익스트라 최단 경로 알고리즘 구현

import heapq

def dijkstra(graph: dict, start: str, end: str) -> tuple[float, list[str]]:
    """
    다익스트라 알고리즘 (거리 기반 또는 시간 기반 공통)

    Parameters:
    - graph: 인접 리스트 형태의 그래프 (dict[str, dict[str, float]])
    - start: 출발역 이름
    - end: 도착역 이름

    Returns:
    - total_cost: 총 거리 또는 시간 (float)
    - path: 최단 경로에 해당하는 역 이름 리스트
    """
    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)

        if node in visited:
            continue
        visited.add(node)
        path = path + [node]

        if node == end:
            return cost, path

        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))

    return float('inf'), []


# 거리 기반 경로 탐색 함수
def dijkstra_distance(graph, start, end):
    """
    거리 기반 다익스트라: 거리 단위는 km
    """
    return dijkstra(graph, start, end)


# 시간 기반 경로 탐색 함수
def dijkstra_time(graph_time, start, end):
    """
    시간 기반 다익스트라: 시간 단위는 초
    """
    return dijkstra(graph_time, start, end)
