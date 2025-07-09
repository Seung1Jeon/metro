from route_finder import find_best_route

def test_direct_route_distance():
    cost, path = find_best_route("반월당", "영남대", mode='distance')
    assert cost > 0
    assert len(path) > 1
    print("✅ 테스트 통과: 단일 경로 (distance)")

def test_direct_route_time():
    cost, path = find_best_route("반월당", "영남대", mode='time')
    assert cost > 0
    assert len(path) > 1
    print("✅ 테스트 통과: 단일 경로 (time)")

def test_route_with_stops():
    cost, path = find_best_route("반월당", "영남대", via_stations=["신매", "사월"], mode='distance')
    assert cost > 0
    assert "신매" in path and "사월" in path
    print("✅ 테스트 통과: 경유역 포함 경로")

def test_route_with_time_filter():
    cost, path = find_best_route("반월당", "영남대", mode='time', start_time="07:35:00")
    assert cost > 0
    assert len(path) > 1
    print("✅ 테스트 통과: 출발 시각 기준 필터")

if __name__ == "__main__":
    test_direct_route_distance()
    test_direct_route_time()
    test_route_with_stops()
    test_route_with_time_filter()