import serial
import struct
import time
import math
import ctypes
import threading

import matplotlib.pyplot as plt
import matplotlib.animation as anim

x_data = []
fb_a_data = []
fb_e_data = []
fb_p_data = []
fb_i_data = []
fb_d_data = []
fb_o_data = []
data_lock = threading.Lock()

def graph_thread():
    fig, ax = plt.subplots()

    fb_a_line, = ax.plot([], [], label="angle")
    fb_e_line, = ax.plot([], [], label="error")
    fb_p_line, = ax.plot([], [], label="p")
    fb_i_line, = ax.plot([], [], label="i")
    fb_d_line, = ax.plot([], [], label="d")
    fb_o_line, = ax.plot([], [], label="output")

    ax.legend()
    ax.set_ylim(-50, 50)

    def update(frame):
        ax.autoscale_view()
        ax.relim()

        with data_lock:
            fb_a_line.set_data(x_data[-500:], fb_a_data[-500:])
            fb_e_line.set_data(x_data[-500:], fb_e_data[-500:])
            fb_p_line.set_data(x_data[-500:], fb_p_data[-500:])
            #fb_i_line.set_data(x_data[-500:], fb_i_data[-500:])
            fb_d_line.set_data(x_data[-500:], fb_d_data[-500:])
            fb_o_line.set_data(x_data[-500:], fb_o_data[-500:])

        return (
            fb_a_line,
            fb_e_line,
            fb_p_line,
            fb_i_line,
            fb_d_line,
            fb_o_line,
        )

    a = anim.FuncAnimation(fig, update, interval=100)
    plt.show()

graph_t = threading.Thread(target=graph_thread)
graph_t.start()

def main():
    ser = serial.Serial("/dev/ttyS10", baudrate=921600)

    x = 0
    while ser.is_open:
        ser.read_until(b"\xcd\xab")
        ser.read(2)

        fb_b = ser.read(24)
        (
            fb_a,
            fb_e,
            fb_p,
            fb_i,
            fb_d,
            fb_o
        ) = struct.unpack("<6f", fb_b)

        # print(f"angle:{fb_a}")
        # print(f"err:  {fb_e}")
        # print(f"p:    {fb_p}")
        # print(f"i:    {fb_i}")
        # print(f"d:    {fb_d}")
        # print(f"o:    {fb_o}")
        # print()
        # print()

        x = x + 1
        with data_lock:
            x_data.append(x)
            fb_a_data.append(fb_a)
            fb_e_data.append(fb_e)
            fb_p_data.append(fb_p)
            fb_i_data.append(fb_i)
            fb_d_data.append(fb_d)
            fb_o_data.append(fb_o)

        # fb_b = ser.read(16)
        # (
        #     fb_cmd1,
        #     fb_cmd2,
        #     fb_speedr,
        #     fb_speedl,
        #     fb_bat,
        #     fb_temp,
        #     fb_cmdl,
        #     fb_checksum,
        # ) = struct.unpack("<6h 2H", fb_b)

        # print(f"cmd1:     {fb_cmd1}")
        # print(f"cmd2:     {fb_cmd2}")
        # print(f"speedr:   {fb_speedr}")
        # print(f"speedl:   {fb_speedl}")
        # print(f"bat:      {fb_bat}")
        # print(f"temp:     {fb_temp}")
        # print(f"cmdl:     {fb_cmdl}")
        # print(f"cs:       {fb_checksum}")
        # print()

        # c_start = 0xABCD
        # c_steer = 0
        # c_speed = int(math.sin((time.monotonic() * 2 * math.pi / 10)) * 2000)
        # c_cs = c_start ^ ctypes.c_ushort(c_steer).value ^ ctypes.c_ushort(c_speed).value

        # c_b = struct.pack("<H 2h H", c_start, c_steer, c_speed, c_cs)
        # ser.write(c_b)
        # ser.flush()
        # print(f"cmd:      {c_b}")
        # print()




if __name__ == "__main__":
    main()
