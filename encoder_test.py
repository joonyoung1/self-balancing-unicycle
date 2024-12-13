import pigpio
import time
from collections import deque

# 핀 번호 설정
ENCODER_A = 19
ENCODER_B = 13

# 초기화
pi = pigpio.pi()
encoder_position = 0

# 디바운싱 시간 (1ms)
DEBOUNCE_TIME = 1000  
last_tick = 0

# 신호 평균화를 위한 큐 설정
A_values = deque(maxlen=5)
B_values = deque(maxlen=5)

# 마지막 신호 상태 저장
last_A = 0
last_B = 0

# 풀업/풀다운 설정 (노이즈 감소)
pi.set_pull_up_down(ENCODER_A, pigpio.PUD_UP)  # 풀업 설정
pi.set_pull_up_down(ENCODER_B, pigpio.PUD_UP)  # 풀업 설정

# 콜백 함수
def encoder_callback(gpio, level, tick):
    global encoder_position, last_tick, last_A, last_B

    # 디바운싱: 신호 간격이 너무 짧으면 무시
    if (tick - last_tick) < DEBOUNCE_TIME:
        return

    # 현재 신호 읽기
    A = pi.read(ENCODER_A)
    B = pi.read(ENCODER_B)

    # 신호 안정화: 직전 값과 동일한 경우 무시
    if A == last_A and B == last_B:
        return

    # 신호를 큐에 저장하여 평균화
    A_values.append(A)
    B_values.append(B)

    # 평균 계산
    A_avg = round(sum(A_values) / len(A_values))
    B_avg = round(sum(B_values) / len(B_values))

    # 인코더 값 변경
    if A_avg == B_avg:
        encoder_position += 1
    else:
        encoder_position -= 1

    # 출력
    print(f"Position: {encoder_position}")

    # 마지막 값 및 시간 갱신
    last_tick = tick
    last_A = A
    last_B = B

# GPIO 핀 감지 설정
pi.callback(ENCODER_A, pigpio.EITHER_EDGE, encoder_callback)

try:
    print("Encoder is running. Press Ctrl+C to stop.")
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    pi.stop()
