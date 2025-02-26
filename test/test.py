# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    #testing the cases 
    test_cases = [
        (20, 30, 50),  # Basic case
        (255, 0, 255),  # Max value of ui_in
        (0, 255, 255),  # Max value of uio_in
        (255, 255, 254),  # Overflow case (255 + 255 = 510, but 8-bit output wraps around to 254)
        (0, 0, 0),  # Zero case
    ]
    for ui, uio, expected in test_cases:
        dut.ui_in.value = ui
        dut.uio_in.value = uio
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == expected, f"Summation failed: {ui} + {uio} != {expected}"

    dut._log.info("Test priority encoder logic")

    # Test priority encoder logic
    dut.en.value = 1  # Enable the priority encoder

    # Test all bits of In
    for i in range(16):
        dut.In.value = 1 << i  # Set only the ith bit to 1
        await ClockCycles(dut.clk, 1)
        assert dut.C.value == i, f"Priority encoder failed: Expected {i}, got {dut.C.value}"

    # Test special case where all bits are 0
    dut.In.value = 0
    await ClockCycles(dut.clk, 1)
    assert dut.C.value == 0b11110000, f"Priority encoder failed: Expected 0b11110000, got {dut.C.value}"

    # Test when en is low
    dut.en.value = 0
    dut.In.value = 0b00000001  # Set the least significant bit
    await ClockCycles(dut.clk, 1)
    assert dut.C.value == 0, f"Priority encoder failed: Expected 0 when en is low, got {dut.C.value}"

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.ui_in.value = 20
    dut.uio_in.value = 30

    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 1)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    assert dut.uo_out.value == 50

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
