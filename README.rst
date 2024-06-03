Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-sampler/badge/?version=latest
    :target: https://circuitpython-sampler.readthedocs.io/
    :alt: Documentation Status



.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/ThomasPDye/CircuitPython_Sampler/workflows/Build%20CI/badge.svg
    :target: https://github.com/ThomasPDye/CircuitPython_Sampler/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

A CircuitPython Library to help with sampling and averaging


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-sampler/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-sampler

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-sampler

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install circuitpython-sampler

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install sampler

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

    import time
    from math import ceil
    import board
    from analogio import AnalogIn

    from sampler import VoltageSampler

    sample_period = 0.1  # minimum time between samples
    print_period = 10  # minimum time between prints
    sleep_period = 0.01  # target time to sleep between time comparisons

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


Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-sampler.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/ThomasPDye/CircuitPython_Sampler/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
