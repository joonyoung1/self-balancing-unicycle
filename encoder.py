import pigpio
import time
from collections import deque

class Encoder:
    def __init__(self, encoder_a_pin, encoder_b_pin):
        self.encoder_a_pin = encoder_a_pin
        self.encoder_b_pin = encoder_b_pin
        
        self.pi = pigpio.pi()
        self.encoder_position = 0
        
        self.DEBOUNCE_TIME = 100
        self.last_tick = 0
        
        self.A_values = deque(maxlen=5)
        self.B_values = deque(maxlen=5)
        
        self.last_A = 0
        self.last_B = 0
        
        self.pi.set_pull_up_down(self.encoder_a_pin, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.encoder_b_pin, pigpio.PUD_UP)
        
        self.pi.callback(self.encoder_a_pin, pigpio.EITHER_EDGE, self.encoder_callback)

    def encoder_callback(self, gpio, level, tick):
        if (tick - self.last_tick) < self.DEBOUNCE_TIME:
            return

        A = self.pi.read(self.encoder_a_pin)
        B = self.pi.read(self.encoder_b_pin)

        if A == self.last_A and B == self.last_B:
            return

        self.A_values.append(A)
        self.B_values.append(B)

        A_avg = round(sum(self.A_values) / len(self.A_values))
        B_avg = round(sum(self.B_values) / len(self.B_values))

        if A_avg == B_avg:
            self.encoder_position += 1
        else:
            self.encoder_position -= 1

        self.last_tick = tick
        self.last_A = A
        self.last_B = B

    def get_position(self):
        current_position = self.encoder_position
        self.encoder_position = 0  # 위치를 리셋
        return current_position


if __name__ == "__main__":
    ENCODER_A = 19
    ENCODER_B = 13

    encoder = Encoder(ENCODER_A, ENCODER_B)
    try:
        while True:
            print(f"Encoder 1 Position: {encoder.get_position()}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        encoder.pi.stop()
