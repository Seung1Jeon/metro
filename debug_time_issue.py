#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
시간 변환 문제 디버깅 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from data_loader import prepare_timetable_long_format_dict
from timetable_query import get_available_departures

def debug_time_conversion():
    """시간 변환 문제 디버깅"""
    print("🔍 시간 변환 문제 디버깅 시작...")
    
    try:
        # 테스트 시간 설정
        test_time = datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)
        print(f"테스트 시간: {test_time}")
        print(f"테스트 시간 (time 객체): {test_time.time()}")
        
        # 시각표 데이터 로드
        timetable_dict = prepare_timetable_long_format_dict()
        
        # 설화명곡역 테스트
        station = "설화명곡"
        line = "1호선"
        direction = "상"
        
        print(f"\n🚇 {station}역 {test_time.time()} 이후 열차 조회:")
        
        if (line, direction) in timetable_dict:
            departures = get_available_departures(
                timetable_dict,
                line,
                direction,
                station,
                test_time.time()
            )
            
            print(f"조회된 열차 수: {len(departures)}")
            
            if not departures.empty:
                print("\n첫 5개 열차:")
                for i, (_, row) in enumerate(departures.head().iterrows(), 1):
                    train_time = row['시각']
                    print(f"{i:02d}. 열차번호: {row['열차번호']} | 시각: {train_time}")
                    
                    # 시간 변환 테스트
                    if hasattr(train_time, 'time'):
                        time_obj = train_time.time()
                        print(f"   → time 객체: {time_obj}")
                        
                        # 오늘 날짜로 변환
                        today = datetime.now().date()
                        combined_time = datetime.combine(today, time_obj)
                        print(f"   → 오늘 날짜로 변환: {combined_time}")
                    else:
                        print(f"   → time() 메서드 없음: {type(train_time)}")
            else:
                print("열차 정보가 없습니다.")
        else:
            print(f"노선 ({line}, {direction}) 데이터가 없습니다.")
            
    except Exception as e:
        print(f"❌ 디버깅 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_time_conversion() 