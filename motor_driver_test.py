import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

# Right Motor (DRV8871 1번 모듈)
in1 = 17  # Right motor IN1 (정방향 PWM)
in2 = 27  # Right motor IN2 (역방향 PWM)

# Left Motor (DRV8871 2번 모듈)
in3 = 5   # Left motor IN1 (정방향 PWM)
in4 = 6   # Left motor IN2 (역방향 PWM)

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

# PWM 설정
pwm_right_forward = GPIO.PWM(in1, 100)  # Right motor 정방향 PWM (100Hz)
pwm_right_backward = GPIO.PWM(in2, 100)  # Right motor 역방향 PWM (100Hz)

pwm_left_forward = GPIO.PWM(in3, 100)   # Left motor 정방향 PWM (100Hz)
pwm_left_backward = GPIO.PWM(in4, 100)  # Left motor 역방향 PWM (100Hz)

# PWM 시작 (초기 속도 0%)
pwm_right_forward.start(0)
pwm_right_backward.start(0)
pwm_left_forward.start(0)
pwm_left_backward.start(0)

try:
    speed = 100

    while True:
        user_input = input()

        if user_input == "w":  # Forward
            # 정방향 활성화
            pwm_right_forward.ChangeDutyCycle(speed)
            pwm_left_forward.ChangeDutyCycle(speed)
            # 역방향 비활성화
            pwm_right_backward.ChangeDutyCycle(0)
            pwm_left_backward.ChangeDutyCycle(0)
            print("Forward")

        elif user_input == "s":  # Backward
            # 역방향 활성화
            pwm_right_backward.ChangeDutyCycle(speed)
            pwm_left_backward.ChangeDutyCycle(speed)
            # 정방향 비활성화
            pwm_right_forward.ChangeDutyCycle(0)
            pwm_left_forward.ChangeDutyCycle(0)
            print("Backward")

        elif user_input == "d":  # Right Turn
            # Right motor 역방향, Left motor 정방향
            pwm_right_forward.ChangeDutyCycle(0)
            pwm_right_backward.ChangeDutyCycle(speed)

            pwm_left_forward.ChangeDutyCycle(speed)
            pwm_left_backward.ChangeDutyCycle(0)
            print("Right")

        elif user_input == "a":  # Left Turn
            # Right motor 정방향, Left motor 역방향
            pwm_right_forward.ChangeDutyCycle(speed)
            pwm_right_backward.ChangeDutyCycle(0)

            pwm_left_forward.ChangeDutyCycle(0)
            pwm_left_backward.ChangeDutyCycle(speed)
            print("Left")

        elif user_input == "c":  # Stop
            # 모든 PWM 비활성화
            pwm_right_forward.ChangeDutyCycle(0)
            pwm_right_backward.ChangeDutyCycle(0)
            pwm_left_forward.ChangeDutyCycle(0)
            pwm_left_backward.ChangeDutyCycle(0)
            print("Stop")
        
        elif user_input == "f":
            speed = min(100, speed + 10)
        elif user_input == "g":
            speed = max(20, speed - 10)

except KeyboardInterrupt:
    pwm_right_forward.stop()
    pwm_right_backward.stop()
    pwm_left_forward.stop()
    pwm_left_backward.stop()
    GPIO.cleanup()
    print("GPIO Clean up")
