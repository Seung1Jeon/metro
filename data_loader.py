import pandas as pd
from collections import defaultdict

def build_graph_from_csv(file_path, encoding='cp949'):
    df = pd.read_csv(file_path, encoding=encoding)
    graph = {}
    stations = df['역명'].tolist()
    distances = df['하행키로'].tolist()

    for i in range(len(stations) - 1):
        curr, next_ = stations[i], stations[i + 1]
        distance = distances[i + 1]

        graph.setdefault(curr, {})[next_] = distance
        graph.setdefault(next_, {})[curr] = distance

    return graph

def load_total_graph():
    files = [
        '대구교통공사_1호선 역 구간정보_20241231.csv',
        '대구교통공사_2호선 역 구간정보_20241231.csv',
        '대구교통공사_3호선 역 구간정보_20241231.csv'
    ]

    total_graph = defaultdict(dict)

    for file in files:
        g = build_graph_from_csv(file)
        for station, neighbors in g.items():
            total_graph[station].update(neighbors)

    return dict(total_graph)

