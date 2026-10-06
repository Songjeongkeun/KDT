"""
OpenCV(Opne Source Vision Library)
OpenCV는 이미지(영상)을 처리하기 위한 대표적인 오픈소스 컴퓨터 비전 라이브러리

- 이미지(영상) 읽기와 저장
- 색상 공간 변환
- 크기 변경, 회전, 자르기
- 필터링과 경계선 검출
- 이진화와 객체 분할
- 특징점 검출
- 머신러닝/딥러닝 모델과의 이동

> OpenCV에서 읽은 이미지는 기본적으로 Numpy 배열로 다루기 때문에 Numpy 인덱싱, 슬라이싱, 배열 연산을 그대로 활용할 수 있음

pip install opencv-python
"""
# import sys
# print(sys.executable)
import cv2

print('현재 OpenCV 버전: ', cv2.__version__)