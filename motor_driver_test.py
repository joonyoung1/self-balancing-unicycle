import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

# Right Motor (DRV8871 1번 모듈)
in1 = 17  # Right motor IN1 (PWM 사용)
in2 = 27  # Right motor IN2

# Left Motor (DRV8871 2번 모듈)
in3 = 5   # Left motor IN1 (PWM 사용)
in4 = 6   # Left motor IN2

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

# PWM 설정 (IN1, IN3 핀에서 PWM 제어)
pwm_right = GPIO.PWM(in1, 100)  # Right motor PWM (100Hz)
pwm_left = GPIO.PWM(in3, 100)   # Left motor PWM (100Hz)
pwm_right.start(0)  # 초기 속도 0%
pwm_left.start(0)   # 초기 속도 0%

GPIO.output(in2, GPIO.LOW)  # Right motor 초기 방향
GPIO.output(in4, GPIO.LOW)  # Left motor 초기 방향

try:
    speed = 100
    # Create Infinite loop to read user input
    while True:
        # Get user Input
        user_input = input()

        if user_input == "w":
            # Forward
            GPIO.output(in2, GPIO.LOW)  # Right motor 정방향
            GPIO.output(in4, GPIO.LOW)  # Left motor 정방향
            pwm_right.ChangeDutyCycle(speed)  # 속도 75%
            pwm_left.ChangeDutyCycle(speed)   # 속도 75%
            print("Forward")

        elif user_input == "s":
            # Backward
            GPIO.output(in2, GPIO.HIGH)  # Right motor 역방향
            GPIO.output(in4, GPIO.HIGH)  # Left motor 역방향
            pwm_right.ChangeDutyCycle(speed)  # 속도 75%
            pwm_left.ChangeDutyCycle(speed)   # 속도 75%
            print("Back")

        elif user_input == "d":
            # Right Turn
            GPIO.output(in2, GPIO.LOW)  # Right motor 정방향
            GPIO.output(in4, GPIO.LOW)  # Left motor 정지
            pwm_right.ChangeDutyCycle(speed)  # Right motor 속도 75%
            pwm_left.ChangeDutyCycle(0)    # Left motor 속도 0%
            print("Right")

        elif user_input == "a":
            # Left Turn
            GPIO.output(in2, GPIO.LOW)  # Right motor 정지
            GPIO.output(in4, GPIO.LOW)  # Left motor 정방향
            pwm_right.ChangeDutyCycle(0)    # Right motor 속도 0%
            pwm_left.ChangeDutyCycle(speed)    # Left motor 속도 75%
            print("Left")

        elif user_input == "c":
            # Stop
            pwm_right.ChangeDutyCycle(0)  # Right motor 정지
            pwm_left.ChangeDutyCycle(0)   # Left motor 정지
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)
            print("Stop")
        
        elif user_input == "f":
            speed = min(100, speed + 10)
        elif user_input == "g":
            speed = max(20, speed - 10)

except KeyboardInterrupt:
    pwm_right.stop()
    pwm_left.stop()
    GPIO.cleanup()
    print("GPIO Clean up")
