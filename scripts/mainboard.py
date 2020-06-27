import serial
import struct
import time
import math
import ctypes

def main():
    ser = serial.Serial("/dev/ttyS10", baudrate=38400)

    while ser.is_open:
        ser.read_until(b"\xcd\xab")

        fb_b = ser.read(16)
        (
            fb_cmd1,
            fb_cmd2,
            fb_speedr,
            fb_speedl,
            fb_bat,
            fb_temp,
            fb_cmdl,
            fb_checksum,
        ) = struct.unpack("<6h 2H", fb_b)

        print(f"cmd1:     {fb_cmd1}")
        print(f"cmd2:     {fb_cmd2}")
        print(f"speedr:   {fb_speedr}")
        print(f"speedl:   {fb_speedl}")
        print(f"bat:      {fb_bat}")
        print(f"temp:     {fb_temp}")
        print(f"cmdl:     {fb_cmdl}")
        print(f"cs:       {fb_checksum}")
        print()

        c_start = 0xABCD
        c_steer = 0
        c_speed = int(math.sin((time.monotonic() * 2 * math.pi / 10)) * 2000)
        c_cs = c_start ^ ctypes.c_ushort(c_steer).value ^ ctypes.c_ushort(c_speed).value

        c_b = struct.pack("<H 2h H", c_start, c_steer, c_speed, c_cs)
        ser.write(c_b)
        ser.flush()
        print(f"cmd:      {c_b}")
        print()




if __name__ == "__main__":
    main()
