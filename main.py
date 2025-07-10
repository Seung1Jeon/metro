from route_finder import find_best_route, recommend_trains_by_segments
from path_utils import split_path_by_line
from datetime import datetime, timedelta

def run_full_routine():
    start = input("출발역을 입력하세요: ").strip()
    end = input("도착역을 입력하세요: ").strip()
    start_time = input("출발 시각을 입력하세요 (예: 07:35:00): ").strip()
    mode = input("모드 선택 (distance / time): ").strip().lower()

    print("\n경로 탐색 중...\n")
    
    total_cost, path = find_best_route(start, end, mode=mode)
    print(f"전체 경로: {' → '.join(path)}")
    print(f"총 소요 {('시간' if mode=='time' else '거리')}: {round(total_cost/60, 1)}분\n")

    segments = split_path_by_line(path)
    train_recommendations = recommend_trains_by_segments(segments, start_time)

    print("구간별 열차 추천:")
    for rec in train_recommendations:
        print(f"[{rec['line']}] {rec['from']} → {rec['to']} | 열차번호: {rec['train_number']} | 출발: {rec['depart_time']} | 방향: {rec['direction']}")

if __name__ == "__main__":
    run_full_routine()
