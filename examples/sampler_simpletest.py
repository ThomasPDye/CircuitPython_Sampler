# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 Thomas Dye
#
# SPDX-License-Identifier: Unlicense
import time
from math import ceil
import board
from analogio import AnalogIn

from sampler import VoltageSampler

sample_period = 0.1  # minimum time between samples
print_period = 10  # minimum time between prints
sleep_period = 0.01  # target time to sleep between time comparisons
# (approximately equivalent to timing precision)

num_samples = ceil(print_period / sample_period)

battery_voltage_sampler = VoltageSampler(
    AnalogIn(board.VOLTAGE_MONITOR), ratio=2.0, max_samples=num_samples
)

last_print_time = last_sample_time = time.monotonic()
battery_voltage_sampler.update()
print(battery_voltage_sampler.average())

while True:
    t = time.monotonic()
    if t - last_sample_time >= sample_period:
        battery_voltage_sampler.update()
        last_sample_time = t
    if t - last_print_time >= print_period:
        print("{:.2f} V".format(battery_voltage_sampler.average(num_samples)))
        last_print_time = t
    time.sleep(sleep_period)
