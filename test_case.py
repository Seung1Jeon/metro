from route_finder import find_best_route, recommend_trains_by_segments
from path_utils import split_path_by_line

def test_segment_ordered_recommendation():
    cost, path = find_best_route("설화명곡", "칠곡경대병원", mode='time')
    segments = split_path_by_line(path)

    # 열차 추천 결과가 시간 순으로 출력되는지 확인
    print("\n📍 전체 경로:", " → ".join(path))
    print("총 소요 시간:", cost / 60, "분")  # 초 단위를 분으로 변환

    recommend_trains_by_segments(segments, start_time_str="07:00:00")

if __name__ == "__main__":
    test_segment_ordered_recommendation()

# from path_utils import find_route

# def test_simple_time_route():
#     start = "문양"
#     end = "영남대"
#     mode = "time"

#     try:
#         cost, path = find_route(start, end, mode)
#         print("✅ 최소 시간 경로 테스트 통과")
#         print(f"경로: {' → '.join(path)}")
#         print(f"총 소요 시간: {cost:.1f}초")
#     except Exception as e:
#         print("❌ 테스트 실패:", e)

# if __name__ == "__main__":
#     test_simple_time_route()


