import pigpio
import time

class MotorController:
    def __init__(self, pwm_a_pin, pwm_b_pin, freq=10000):
        self.pi = pigpio.pi()
        self.pwm_a_pin = pwm_a_pin
        self.pwm_b_pin = pwm_b_pin
        self.pi.set_mode(self.pwm_a_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.pwm_b_pin, pigpio.OUTPUT)

        self.pi.set_PWM_frequency(self.pwm_a_pin, freq)
        self.pi.set_PWM_frequency(self.pwm_b_pin, freq)
        self.pi.set_PWM_dutycycle(self.pwm_a_pin, 0)
        self.pi.set_PWM_dutycycle(self.pwm_b_pin, 0)

    def set_pwm(self, pwm_value):
        pwm_value = max(min(pwm_value, 255), -255)  # -255 ~ 255 범위로 제한
        if pwm_value > 0:
            self.pi.set_PWM_dutycycle(self.pwm_a_pin, pwm_value)
            self.pi.set_PWM_dutycycle(self.pwm_b_pin, 0)
        elif pwm_value < 0:
            self.pi.set_PWM_dutycycle(self.pwm_a_pin, 0)
            self.pi.set_PWM_dutycycle(self.pwm_b_pin, -pwm_value)
        else:
            self.pi.set_PWM_dutycycle(self.pwm_a_pin, 0)
            self.pi.set_PWM_dutycycle(self.pwm_b_pin, 0)

    def stop(self):
        self.pi.set_PWM_dutycycle(self.pwm_a_pin, 0)
        self.pi.set_PWM_dutycycle(self.pwm_b_pin, 0)
        self.pi.stop()

if __name__ == "__main__":
    pwm_pin_1 = 17
    pwm_pin_2 = 27

    motor_controller = MotorController(pwm_pin_1, pwm_pin_2)
    
    try:
        while True:
            target_pwm = int(input("Enter PWM value (-255 to 255): "))
            motor_controller.set_pwm(target_pwm)
            time.sleep(1)
        
    except KeyboardInterrupt:
        motor_controller.stop()
        print("모터 제어 종료")
