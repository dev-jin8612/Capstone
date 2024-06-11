from capstone.YDLidarX2 import LidarX2
import serial
import time
import map

in_port = '/dev/ttyACM0'
baud_rate = 9600
ser2 = serial.Serial(in_port, baud_rate)

com_port = '/dev/ttyUSB1'
baud_rate = 115200
ser = serial.Serial(com_port, baud_rate)

Lidar = LidarX2()
flag1 = 0
flag2 = 0
ampCheck = []

def check_lidar():
    result = Lidar.getPolarResults()
    filtered_result = {key: value for key, value in result.items() if
                       int(key) in range(0, 30) or int(key) in range(330, 360)}

    for value in filtered_result.values():
        if 10 < value < 3000:
            print("abovid")
            ser.write(b'A 0')
            time.sleep(13)
            return True
    return False

def move_forward(duration, check_interval=0.1):
    start_time = time.time()
    while time.time() - start_time < duration:
        check_lidar()
        ser.write(b'F 1\n')
        time.sleep(check_interval)

def handle_direction(direction, distance_str):
    if int(direction) >= 90:
        time.sleep_duration = 2.4
    elif int(direction) > 75:
        time.sleep_duration = 2.4
    elif int(direction) > 60:
        time.sleep_duration = 1.2
    elif int(direction) > 45:
        time.sleep_duration = 1.0
    elif int(direction) > 35:
        time.sleep_duration = 0.7
    elif int(direction) > 25:
        time.sleep_duration = 0.5
    elif int(direction) > 15:
        time.sleep_duration = 0.3
    else:
        time.sleep_duration = 0

    if time.sleep_duration > 0:
        command = f"{distance_str} 1\n"
        ser.write(command.encode())
        time.sleep(time.sleep_duration)

def main_function():
    global flag1, flag2, mapCheck

    with Lidar as lidar:
        while True:
            if len(mapCheck) - 1 > flag1:
                road = int(mapCheck[flag1][3])
                print(road)

                if road > 50:
                    le = int(road / 4)
                    move_forward(le)
                else:
                    move_forward(road * 0.1)
            else:
                t1 = mapCheck[-2][0]
                t2 = mapCheck[-1]
                t = map.calculate_distance(t1, t2)
                ti = int(t)
                move_forward(ti/2)
                ser.write(b'S 0')

            direction = float(mapCheck[flag1][1])
            distance_str = mapCheck[flag1][2]
            handle_direction(direction, distance_str)

            print(f"{distance_str} turn")
            flag1 += 1
            print("________")

def move_function():
    while True:
        user_input = input("Enter 'start' to begin or 's' to end: ")
        if user_input.lower() == 'start':
            main_function()
        elif user_input.lower() == 's':
            print("Stopping...")
            break
        else:
            print("Invalid input. Please enter 'start' or 's'.")

if __name__ == "__main__":
    move_function()
