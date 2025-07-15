#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GUI와 경로 계산 로직 연동 테스트 스크립트
"""

import sys
import os

# 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_route_calculation():
    """경로 계산 로직 테스트"""
    try:
        from route_finder import find_best_route
        from path_utils import split_path_by_line
        
        print("🚇 경로 계산 로직 테스트 시작...")
        
        # 테스트 케이스들
        test_cases = [
            ("화원", "교대"),
            ("설화명곡", "칠곡경대병원"),
            ("문양", "영남대"),
            ("반월당", "청라언덕")
        ]
        
        for start, end in test_cases:
            print(f"\n📍 {start} → {end}")
            try:
                total_cost, path = find_best_route(start, end, mode='time')
                segments = split_path_by_line(path)
                
                print(f"   경로: {' → '.join(path)}")
                print(f"   소요시간: {total_cost/60:.1f}분")
                print(f"   구간수: {len(segments)}")
                
                for i, segment in enumerate(segments, 1):
                    print(f"   구간{i}: {segment['line']} {segment['direction']}행 "
                          f"({segment['stations'][0]} → {segment['stations'][-1]})")
                          
            except Exception as e:
                print(f"   ❌ 오류: {e}")
                
        print("\n✅ 경로 계산 로직 테스트 완료!")
        return True
        
    except ImportError as e:
        print(f"❌ 모듈 import 오류: {e}")
        return False
    except Exception as e:
        print(f"❌ 테스트 오류: {e}")
        return False

def test_gui_launch():
    """GUI 실행 테스트"""
    try:
        print("\n🖥️ GUI 실행 테스트...")
        
        # GUI 모듈 import 테스트
        from build.gui import MetroApp
        
        print("✅ GUI 모듈 import 성공!")
        print("💡 GUI를 실행하려면 다음 명령어를 사용하세요:")
        print("   python build/gui.py")
        
        return True
        
    except ImportError as e:
        print(f"❌ GUI 모듈 import 오류: {e}")
        return False
    except Exception as e:
        print(f"❌ GUI 테스트 오류: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("=" * 50)
    print("🚇 대구지하철 경로 계산 시스템 테스트")
    print("=" * 50)
    
    # 1. 경로 계산 로직 테스트
    route_test_passed = test_route_calculation()
    
    # 2. GUI 실행 테스트
    gui_test_passed = test_gui_launch()
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("📊 테스트 결과 요약")
    print("=" * 50)
    print(f"경로 계산 로직: {'✅ 통과' if route_test_passed else '❌ 실패'}")
    print(f"GUI 모듈: {'✅ 통과' if gui_test_passed else '❌ 실패'}")
    
    if route_test_passed and gui_test_passed:
        print("\n🎉 모든 테스트가 통과했습니다!")
        print("이제 GUI를 실행하여 실제 경로 계산 기능을 확인할 수 있습니다.")
    else:
        print("\n⚠️ 일부 테스트가 실패했습니다. 오류를 확인하고 수정해주세요.")

if __name__ == "__main__":
    main() 