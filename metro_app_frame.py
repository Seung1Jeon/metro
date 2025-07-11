import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
from pathlib import Path

IMG_FONT_PATH = "C:\\Windows\\Fonts\\malgun.ttf"

class MetroAppFrame(tk.Frame):
    """
    MetroApp을 프레임으로 변환한 클래스
    다른 프레임들과 동일한 폰트와 색상 스타일을 적용
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#FFFFFF")
        
        # 기존 MetroApp의 속성들을 controller로 이동
        self.departure_station = None
        self.arrival_station = None
        self.is_selecting_departure = False
        self.is_selecting_arrival = False
        self.favorites = []  # 즐겨찾기 역 리스트
        self.frames = {}
        
        # 프레임들을 초기화
        self.init_frames()
        
    def init_frames(self):
        """프레임들을 초기화하고 등록"""
        # MainPage, SecondPage, ThirdPage 프레임들을 생성
        # 실제 구현에서는 이 부분을 controller에서 처리하도록 수정
        pass
        
    def show_frame(self, name):
        """프레임 전환 메서드"""
        print("show_frame:", name)
        if name in self.frames:
            self.frames[name].tkraise()
            if name == "MainPage":
                self.frames["MainPage"].reset_popup_state()
            if name == "SecondPage":
                self.frames["SecondPage"].close_fav_popup()
                self.frames["SecondPage"].render_favorites()
            if name == "ThirdPage":
                self.frames["ThirdPage"].close_fav_popup()
                self.frames["ThirdPage"].render_favorites()
                
    def set_departure_station(self, station_name):
        """출발역 설정"""
        self.departure_station = station_name
        if "SecondPage" in self.frames:
            self.frames["SecondPage"].update_departure_text()
        if "ThirdPage" in self.frames:
            self.frames["ThirdPage"].update_departure_text()
            
    def set_arrival_station(self, station_name):
        """도착역 설정"""
        self.arrival_station = station_name
        if "SecondPage" in self.frames:
            self.frames["SecondPage"].update_arrival_text()
        if "ThirdPage" in self.frames:
            self.frames["ThirdPage"].update_arrival_text()


class MetroAppController:
    """
    MetroApp의 컨트롤러 역할을 하는 클래스
    프레임들 간의 데이터 공유와 상태 관리를 담당
    """
    def __init__(self):
        self.departure_station = None
        self.arrival_station = None
        self.is_selecting_departure = False
        self.is_selecting_arrival = False
        self.favorites = []
        self.frames = {}
        
    def show_frame(self, name):
        """프레임 전환"""
        print("show_frame:", name)
        if name in self.frames:
            self.frames[name].tkraise()
            if name == "MainPage":
                self.frames["MainPage"].reset_popup_state()
            if name == "SecondPage":
                self.frames["SecondPage"].close_fav_popup()
                self.frames["SecondPage"].render_favorites()
            if name == "ThirdPage":
                self.frames["ThirdPage"].close_fav_popup()
                self.frames["ThirdPage"].render_favorites()
                
    def set_departure_station(self, station_name):
        """출발역 설정"""
        self.departure_station = station_name
        if "SecondPage" in self.frames:
            self.frames["SecondPage"].update_departure_text()
        if "ThirdPage" in self.frames:
            self.frames["ThirdPage"].update_departure_text()
            
    def set_arrival_station(self, station_name):
        """도착역 설정"""
        self.arrival_station = station_name
        if "SecondPage" in self.frames:
            self.frames["SecondPage"].update_arrival_text()
        if "ThirdPage" in self.frames:
            self.frames["ThirdPage"].update_arrival_text()


def create_metro_app():
    """
    MetroApp을 생성하는 함수
    프레임 기반 구조로 변경
    """
    root = tk.Tk()
    root.title("대구지하철노선도")
    root.geometry("540x960")
    
    # 컨트롤러 생성
    controller = MetroAppController()
    
    # 메인 프레임 생성
    main_frame = MetroAppFrame(root, controller)
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)
    
    # 여기서 MainPage, SecondPage, ThirdPage 프레임들을 생성하고 등록
    # 실제 구현에서는 기존 프레임 클래스들을 import하여 사용
    
    return root, controller


if __name__ == "__main__":
    root, controller = create_metro_app()
    root.mainloop() 