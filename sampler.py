# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 Thomas Dye
#
# SPDX-License-Identifier: MIT
"""
`sampler`
================================================================================

A CircuitPython Library to help with sampling and averagin


* Author(s): Thomas Dye

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/ThomasPDye/CircuitPython_Sampler.git"

class Sampler:
    def __init__(self, max_samples: int = 256):
        self.__max_samples = max_samples
        self.__samples = []

    def __get(self):
        pass

    def len(self):
        return len(self.__samples)

    def update(self):
        while self.len() >= self.__max_samples:
            self.__samples.pop(0)
        self.__samples.append(self.__get())

    def average(self, lastn: int = 128):
        if self.len() == 0:
            self.update()
        N = self.len()
        startn = 0
        if 0 < lastn and lastn <= N:
            startn = N - lastn
        sum = 0
        for n in range(startn,N):
            sum += self.__samples[n]
        return sum / (N - startn)

    def reset(self):
        self.__samples.clear()

from analogio import AnalogIn

class VoltageSampler(Sampler):
    def __init__(self, ain: AnalogIn, ratio: float = 1.0, max_samples:int = 1024):
        super().__init__(max_samples)
        self.__ain = ain
        self.__ratio = ratio

    def __get(self):
        return self.__ratio * (self.__ain.value * self.__ain.reference_voltage) / 65536
