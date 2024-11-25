import mpu6050
import time
import math

# MPU6050 인스턴스 생성 (I2C 주소: 0x68)
mpu = mpu6050.mpu6050(0x68)

# 기울기 각도 (Pitch, Roll) 계산 함수
def calculate_tilt(accel_data):
    # 가속도계 데이터에서 x, y, z 값 추출
    ax = accel_data['x']
    ay = accel_data['y']
    az = accel_data['z']
    
    # pitch (앞뒤 기울기) 계산
    pitch = math.atan2(ay, math.sqrt(ax**2 + az**2)) * (180 / math.pi)
    
    # roll (좌우 기울기) 계산
    roll = math.atan2(ax, math.sqrt(ay**2 + az**2)) * (180 / math.pi)

    return pitch, roll

# 센서 데이터 읽기 함수
def read_sensor_data():
    accelerometer_data = mpu.get_accel_data()
    gyroscope_data = mpu.get_gyro_data()
    temperature = mpu.get_temp()

    # 기울기 계산 (Pitch, Roll)
    pitch, roll = calculate_tilt(accelerometer_data)

    return accelerometer_data, gyroscope_data, temperature, pitch, roll

# 메인 루프: 센서 데이터 읽기 및 출력
while True:
    accelerometer_data, gyroscope_data, temperature, pitch, roll = read_sensor_data()

    # 결과 출력
    print(f"Accelerometer data: {accelerometer_data}")
    print(f"Gyroscope data: {gyroscope_data}")
    print(f"Temp: {temperature}°C")
    print(f"Pitch: {pitch}°")  # 기울기 (앞뒤)
    print(f"Roll: {roll}°")    # 기울기 (좌우)
    
    # 각속도 출력 (Gyroscope 데이터)
    print(f"Gyroscope X: {gyroscope_data['x']}°/s")
    print(f"Gyroscope Y: {gyroscope_data['y']}°/s")
    print(f"Gyroscope Z: {gyroscope_data['z']}°/s")

    # 0.1초 대기
    time.sleep(0.1)
