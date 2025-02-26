/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_max (
    parameter n = 8,
    int i = 0,
    input  wire [n-1:0] ui_in,    // Dedicated inputs
    output wire [n-1:0] uo_out,   // Dedicated outputs
    input  wire [n-1:0] uio_in,   // IOs: Input path
    output wire [n-1:0] uio_out,  // IOs: Output path
    output wire [n-1:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n,    // reset_n - low to reset
    wire [0:1] C
);

  // All output pins must be assigned. If not used, assign to 0.
    always @(ui_in, uio_in)
    begin
        i = n - 1;
        C = 0;
        while (i >= 0 & C[0] == 1)
        begin
            C[0] == ui_in[i] ^ uio_in[i];
            C[1] == ~ui_in[i];
            i--;
        end
        
        if (C[0] == 1) uo_out = C[1] ? uio_in : ui_in;
        else uo_out = 0;
    end
    
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
