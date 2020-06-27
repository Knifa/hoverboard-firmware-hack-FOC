import serial
import struct
import time
import math
import ctypes

def main():
    ser = serial.Serial("/dev/ttyS10", baudrate=38400)

    while ser.is_open:
        rest = ser.read_until(b"\xcd\xab")

        fb_b = ser.read(10)
        print(rest)
        print(fb_b)

        (
            fb_roll,
            fb_pitch,
            fb_yaw,
            fb_sensors,
            fb_cs
        ) = struct.unpack("<3h2H", fb_b)

        print(f"roll:     {fb_roll / 100} deg")
        print(f"pitch:    {fb_pitch / 100} deg")
        print(f"yaw:      {fb_yaw / 100} deg")
        print(f"sensors:  {fb_sensors}")
        print(f"cs:       {fb_cs}")
        print()


if __name__ == "__main__":
    main()
