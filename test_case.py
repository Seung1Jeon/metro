from route_finder import find_best_route, recommend_trains_by_segments
from path_utils import split_path_by_line
from timetable_query import get_available_departures
from datetime import datetime

def test_segment_ordered_recommendation():
    cost, path = find_best_route("설화명곡", "칠곡경대병원", mode='time')
    segments = split_path_by_line(path)

    # 열차 추천 결과가 시간 순으로 출력되는지 확인
    print("\n📍 전체 경로:", " → ".join(path))
    print("총 소요 시간:", cost / 60, "분")  # 초 단위를 분으로 변환

    recommend_trains_by_segments(segments, start_time_str="07:00:00")

def test_departures_for_line1_upward():
    departures = get_available_departures(
        line='1호선',
        direction='상',
        station='설화명곡',
        after_time=datetime.strptime("07:00:00", "%H:%M:%S").time()
    )

    if not departures:
        print("❌ 07:00 이후 설화명곡역 출발 1호선 상행 열차가 없습니다.")
    else:
        print(f"✅ 총 {len(departures)}개의 열차가 검색되었습니다. 상위 5개:")
        for train in departures[:5]:
            print(train)

def debug_station_entries():
    import pandas as pd
    df = pd.read_csv("data/대구교통공사_1호선 열차시각표(상선)_20241007.csv", encoding="cp949")
    설화 = df[df['역명'] == '설화명곡']
    print("설화명곡 상행 데이터 중 '구분' 분포:\n", 설화['구분'].value_counts())
    print(설화.head())  # 시각표 직접 확인

if __name__ == "__main__":
    debug_station_entries()
    test_departures_for_line1_upward()
    test_segment_ordered_recommendation()

