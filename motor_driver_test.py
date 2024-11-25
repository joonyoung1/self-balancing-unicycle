import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

# Right Motor
in1 = 17
in2 = 27
en_a = 4
# Left Motor
in3 = 5
in4 = 6
en_b = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en_a, GPIO.OUT)

GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en_b, GPIO.OUT)

q = GPIO.PWM(en_a, 100)
p = GPIO.PWM(en_b, 100)
p.start(0)  # 시작 PWM은 0
q.start(0)  # 시작 PWM은 0

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)

# PWM 값을 점진적으로 증가/감소하는 함수
def gradual_change(pwm, target, step=5, delay=0.1):
    """
    :param pwm: PWM 객체
    :param target: 목표 Duty Cycle 값
    :param step: 증가/감소 단위 (기본값: 5)
    :param delay: 단계 사이의 지연 시간 (기본값: 0.1초)
    """
    current = pwm.duty_cycle if hasattr(pwm, 'duty_cycle') else 0  # 현재 Duty Cycle 가져오기
    if target > current:  # 증가
        for value in range(current, target + step, step):
            pwm.ChangeDutyCycle(min(value, target))
            sleep(delay)
    elif target < current:  # 감소
        for value in range(current, target - step, -step):
            pwm.ChangeDutyCycle(max(value, target))
            sleep(delay)

try:
    while True:
        user_input = input()

        if user_input == "w":  # Forward
            gradual_change(q, 0)  # PWM 점진적 감소
            gradual_change(p, 0)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            GPIO.output(in3, GPIO.LOW)
            print("Forward")
            gradual_change(q, 75)  # 오른쪽 모터 점진적 증가
            gradual_change(p, 75)  # 왼쪽 모터 점진적 증가

        elif user_input == "s":  # Backward
            gradual_change(q, 0)
            gradual_change(p, 0)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)
            GPIO.output(in3, GPIO.HIGH)
            print("Back")
            gradual_change(q, 75)
            gradual_change(p, 75)

        elif user_input == "d":  # Right
            gradual_change(q, 0)
            gradual_change(p, 0)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            print("Right")
            gradual_change(q, 50)  # 오른쪽 모터 낮은 PWM
            gradual_change(p, 75)  # 왼쪽 모터 높은 PWM

        elif user_input == "a":  # Left
            gradual_change(q, 0)
            gradual_change(p, 0)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            print("Left")
            gradual_change(q, 75)  # 오른쪽 모터 높은 PWM
            gradual_change(p, 50)  # 왼쪽 모터 낮은 PWM

        elif user_input == "c":  # Stop
            print("Stop")
            gradual_change(q, 0)  # PWM 점진적 감소
            gradual_change(p, 0)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO Clean up")
