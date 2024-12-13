import mpu6050
import time
import math

class BalanceSensor:
    def __init__(self, address=0x68, alpha=0.99):
        self.mpu = mpu6050.mpu6050(address)
        self.alpha = alpha
        self.last_time = time.time()
        self.pitch = 0
        self.roll = 0

    def calculate_tilt(self, accel_data):
        ax = accel_data['x']
        ay = accel_data['y']
        az = accel_data['z']

        pitch = math.atan2(az, math.sqrt(ax**2 + (-ay)**2)) * (180 / math.pi)
        roll = math.atan2(ax, math.sqrt(az**2 + (-ay)**2)) * (180 / math.pi)

        return pitch, roll

    def complementary_filter(self, accel_pitch, accel_roll, gyro_pitch, gyro_roll, dt):
        pitch = self.alpha * (gyro_pitch * dt + accel_pitch) + (1 - self.alpha) * accel_pitch
        roll = self.alpha * (gyro_roll * dt + accel_roll) + (1 - self.alpha) * accel_roll

        return pitch, roll

    def read_sensor_data(self):
        accelerometer_data = self.mpu.get_accel_data()
        gyro_data = self.mpu.get_gyro_data()

        accel_pitch, accel_roll = self.calculate_tilt(accelerometer_data)
        gyro_pitch = gyro_data['x'] / 131.0
        gyro_roll = gyro_data['y'] / 131.0

        return accel_pitch, accel_roll, gyro_pitch, gyro_roll

    def get_pitch_roll(self):
        accel_pitch, accel_roll, gyro_pitch, gyro_roll = self.read_sensor_data()

        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        return self.complementary_filter(accel_pitch, accel_roll, gyro_pitch, gyro_roll, dt)


if __name__ == "__main__":
    sensor = BalanceSensor()
    while True:
        pitch, roll = sensor.get_pitch_roll()

        print(f"Pitch: {pitch}°")
        print(f"Roll: {roll}°")
        
        time.sleep(0.05)