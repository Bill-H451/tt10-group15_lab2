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
   test_values = [
    0b0000000000000000,  
    0b0000000000000001,  
    0b0000000000000010,  
    0b0000000000000100,  
    0b0000000000001000,  
    0b0000000000010000,  
    0b0000000000100000,  
    0b0000000001000000,  
    0b0000000010000000,  
    0b0000000100000000,  
    0b0000001000000000,  
    0b0000010000000000,  
    0b0000100000000000,  
    0b0001000000000000,  
    0b0010000000000000,  
    0b0100000000000000,  
    0b1000000000000000,  
    0b1111111111111111,  
    0b0000000000000011,  
    0b0000000000000101,  
    0b0000000000001001,  
]
for In_value in test_values:
    dut.In.value = In_value
    await ClockCycles(dut.clk, 1)

    # Calculate the expected value of C directly
    expected_C = 0b11110000  # Default value for the special case (all bits 0)
    for i in range(15, -1, -1):  # Iterate from bit 15 (MSB) to bit 0 (LSB)
        if In_value & (1 << i):  # Check if the ith bit is set
            expected_C = i  # Set expected_C to the index of the first '1'
            break  # Exit the loop once the first '1' is found

    # Compare the actual output with the expected value
    assert dut.C.value == expected_C, (
        f"Priority encoder failed for In = {In_value:016b}: "
        f"Expected C = {expected_C}, got {dut.C.value}"
    )

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
