import pigpio
import time

from encoder import Encoder
from pid import PID

class MotorController:
    def __init__(self, encoder_a_pin, encoder_b_pin, pwm_a_pin, pwm_b_pin, pid_params):
        self.encoder = Encoder(encoder_a_pin, encoder_b_pin)
        self.pid = PID(*pid_params)
        
        self.pi = pigpio.pi()
        self.pwm_a_pin = pwm_a_pin
        self.pwm_b_pin = pwm_b_pin
        self.pi.set_mode(self.pwm_a_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.pwm_b_pin, pigpio.OUTPUT)

        self.pi.set_PWM_frequency(self.pwm_a_pin, 1000)
        self.pi.set_PWM_frequency(self.pwm_b_pin, 1000)
        self.pi.set_PWM_dutycycle(self.pwm_a_pin, 0)
        self.pi.set_PWM_dutycycle(self.pwm_b_pin, 0)

        self.current_speed = 0
        self.target_speed = 0
        self.last_time = time.time()

    def set_target_speed(self, target_speed):
        self.target_speed = target_speed

    def update(self):
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time

        position = self.encoder.get_position()
        self.current_speed = position / delta_time
        print(f"current_speed : {self.current_speed}")

        pid_output = self.pid.compute(self.target_speed, self.current_speed, delta_time)
        print(f"pid_output : {pid_output}")
        pwm_value = min(abs(int(pid_output)), 255)
        if pid_output > 0:
            self.pi.set_PWM_dutycycle(self.pwm_a_pin, pwm_value)
            self.pi.set_PWM_dutycycle(self.pwm_b_pin, 0)
        else:
            self.pi.set_PWM_dutycycle(self.pwm_a_pin, 0)
            self.pi.set_PWM_dutycycle(self.pwm_b_pin, pwm_value)

    def stop(self):
        self.pi.set_PWM_dutycycle(self.pwm_a_pin, 0)
        self.pi.set_PWM_dutycycle(self.pwm_b_pin, 0)
        self.pi.stop()


if __name__ == "__main__":
    encoder_a_pin = 19
    encoder_b_pin = 13
    pwm_pin_1 = 6
    pwm_pin_2 = 5
    
    pid_params = (1.0, 0.1, 0.01)
    
    motor_controller = MotorController(encoder_a_pin, encoder_b_pin, pwm_pin_1, pwm_pin_2, pid_params)
    
    try:
        target_speed = int(input())
        motor_controller.set_target_speed(target_speed)
        
        while True:
            motor_controller.update()
            time.sleep(1)
        
    except KeyboardInterrupt:
        motor_controller.stop()
        print("모터 제어 종료")