`timescale 1ns/1ns
module present_tb;

	
	parameter total_record = 498;
    
    	reg clk, x0_0, x1_0, x2_0, x3_0, x0_1, x1_1, x2_1, x3_1, r;
	
	wire Y0_0, Y1_0, Y2_0, Y3_0, Y0_1, Y1_1, Y2_1, Y3_1;

	integer i, count;

	reg [3:0] out0Comb[0:total_record-1];
	reg [3:0] out1Comb[0:total_record-1];
	initial $readmemb("./InputPlaintext/out0Comb.txt",out0Comb);
	initial $readmemb("./InputPlaintext/out1Comb.txt",out1Comb);
//	initial clk = 1'b0;
 //   	initial ap_rst = 1'b1;
 //   	initial ap_start = 1'b1;
	sbox dut(
	.clk(clk),
	.x0_0(x0_0),
	.x1_0(x1_0),
	.x2_0(x2_0),
	.x3_0(x3_0),
	.x0_1(x0_1),
	.x1_1(x1_1),
	.x2_1(x2_1),
	.x3_1(x3_1),
        .r(r),
	.Y0_0(Y0_0),
	.Y1_0(Y1_0),
	.Y2_0(Y2_0),
	.Y3_0(Y3_0),
	
	.Y0_1(Y0_1),
	
	.Y1_1(Y1_1),
	
	.Y2_1(Y2_1),
	
	.Y3_1(Y3_1));
	
	always begin
	#5 clk = ~clk;
	end
	initial begin
		$dumpfile("sbox_vcd.vcd");
		$dumpvars();
		clk = 0;
		
		i = 0;
		count = 0;
		x0_0 = 0;
		x1_0 = 0;
		x2_0 = 0;
		x3_0 = 0;
		
		x0_1 = 0;
		x1_1 = 0;
		x2_1 = 0;
		x3_1 = 0;
		r = 0;
		
		
	end
	always @(negedge clk) begin
		if (i > total_record) begin
			$finish;
		end
		// else begin
		// 	if (count == 0) begin
			for (i = 0; i < total_record; i = i + 1) begin
				x0_0 = out0Comb[i][0];
				x1_0 = out0Comb[i][1];
				x2_0 = out0Comb[i][2];
				x3_0 = out0Comb[i][3];

				x0_1 = out1Comb[i][0];
				x1_1 = out1Comb[i][1];
				x2_1 = out1Comb[i][2];
				x3_1 = out1Comb[i][3];

				r = 0;
				#34
			
			 
				//$display("Test Case: %0d: %b%b%b%b  %b%b%b%b", i+1, x3_0, x2_0, x1_0, x0_0, x3_1, x2_1, x1_1, x0_1);
				//$display("Time     = %0t: %b%b%b%b  %b%b%b%b", $time,Y3_0, Y2_0, Y1_0, Y0_0, Y3_1, Y2_1, Y1_1, Y0_1);
				//$display("---------------------------------------------------------------");
				$display("%d  %b%b%b%b %b%b%b%b", i+1, x3_0 ^ x3_1, x2_0 ^ x2_1, x1_0 ^ x1_1, x0_0 ^ x0_1, Y0_0 ^ Y0_1, Y1_0 ^ Y1_1, Y2_0 ^ Y2_1, Y3_0 ^ Y3_1);

			end
			// end
			//$display("Test Case %0d: x3_0=%b, x2_0=%b, x1_0=%b, x0_0=%b, x3_1=%b, x2_1=%b, x1_1=%b, x0_1=%b,", i+1, x3_0, x2_0, x1_0, x0_0, x3_1, x2_1, x1_1, x0_1);
			//$display("Time=%0t: Outputs: Y0_0=%b, Y1_0=%b, Y2_0=%b, Y3_0=%b, Y0_1=%b, Y1_1=%b, Y2_1=%b, Y3_1=%b", $time, Y0_0, Y1_0, Y2_0, Y3_0, Y0_1, Y1_1, Y2_1, Y3_1);
			// count = (count + 1)%3;
		// end
		$finish;
	end
endmodule

