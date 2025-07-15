#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
시각표 데이터 구조 디버깅 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import prepare_timetable_long_format_dict, clean_station_name
from timetable_query import get_available_departures
from datetime import datetime

def debug_timetable_structure():
    """시각표 데이터 구조를 디버깅"""
    print("🔍 시각표 데이터 구조 디버깅 시작...")
    
    try:
        # 시각표 데이터 로드
        timetable_dict = prepare_timetable_long_format_dict()
        
        print(f"\n📊 시각표 데이터 키: {list(timetable_dict.keys())}")
        
        # 첫 번째 노선 데이터 확인
        first_key = list(timetable_dict.keys())[0]
        first_df = timetable_dict[first_key]
        
        print(f"\n📋 첫 번째 노선 ({first_key}) 데이터 구조:")
        print(f"Shape: {first_df.shape}")
        print(f"Columns: {list(first_df.columns)}")
        print(f"Data types: {first_df.dtypes}")
        
        print(f"\n📝 첫 5행 데이터:")
        print(first_df.head())
        
        # 특정 역의 출발 정보 확인
        test_station = "설화명곡"
        test_line = "1호선"
        test_direction = "상"
        
        print(f"\n🚇 {test_station}역 출발 정보 테스트:")
        
        if (test_line, test_direction) in timetable_dict:
            departures = get_available_departures(
                timetable_dict,
                test_line,
                test_direction,
                test_station,
                datetime.now().time()
            )
            
            print(f"출발 정보 개수: {len(departures)}")
            
            if not departures.empty:
                print(f"첫 번째 출발 정보:")
                first_row = departures.iloc[0]
                print(f"  Type: {type(first_row)}")
                print(f"  Index: {first_row.index}")
                print(f"  Values: {first_row.values}")
                print(f"  시각: {first_row['시각']}")
                print(f"  열차번호: {first_row['열차번호']}")
                
                # 실제 접근 테스트
                try:
                    print(f"  시각 접근 테스트: {first_row['시각']}")
                    print(f"  열차번호 접근 테스트: {first_row['열차번호']}")
                except Exception as e:
                    print(f"  ❌ 접근 오류: {e}")
                    print(f"  사용 가능한 키: {list(first_row.keys()) if hasattr(first_row, 'keys') else 'No keys'}")
            else:
                print("출발 정보가 없습니다.")
        else:
            print(f"노선 ({test_line}, {test_direction}) 데이터가 없습니다.")
            
    except Exception as e:
        print(f"❌ 디버깅 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_timetable_structure() 