# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 Thomas Dye
#
# SPDX-License-Identifier: MIT
"""
`sampler`
================================================================================

A CircuitPython Library to help with sampling and averaging


* Author(s): Thomas Dye

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""

# imports
import analogio

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/ThomasPDye/CircuitPython_Sampler.git"


class Sampler:
    """Base class for a Sampler

    :param int max_samples: the maximum number of samples to store
                            (before discarding the oldest samples, one at a time)
    """

    def __init__(self, max_samples: int = 256):
        self.__max_samples = max_samples
        self.__samples = []

    def get(self):
        """get value function, requires redefinition in subclasses"""

    def len(self):
        """return number of samples currently stored"""
        return len(self.__samples)

    def update(self):
        """update the array of samples"""
        while self.len() >= self.__max_samples:
            self.__samples.pop(0)
        self.__samples.append(self.get())

    def average(self, lastn: int = 128):
        """return average of the lastn samples"""
        if self.len() == 0:
            self.update()
        length = self.len()
        startn = 0
        if 0 < lastn <= length:
            startn = length - lastn
        sample_sum = 0.0
        for n in range(startn, length):
            sample_sum += self.__samples[n]
        return sample_sum / (length - startn)

    def reset(self):
        """clear the list of stored samples"""
        self.__samples.clear()


class VoltageSampler(Sampler):
    """class for sampling optionally scaled voltages using on board analog inputs
    :param ~analogio.AnalogIn ain: The analog input to get data from
    :param float ratio: value to multiply ain voltage by
                        (e.g. the divider ratio of an external resistive potential divider)
    :param int max_samples: the maximum number of samples to store
    """

    def __init__(
        self, ain: analogio.AnalogIn, ratio: float = 1.0, max_samples: int = 1024
    ):
        super().__init__(max_samples)
        self.__ain = ain
        self.__ratio = ratio

    def get(self):
        """get and scale the voltage on the analog input using instantiated parameters"""
        return self.__ratio * (self.__ain.value * self.__ain.reference_voltage) / 65536
