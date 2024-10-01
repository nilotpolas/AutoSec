`timescale 1 ns / 1 ns

module present_tb;
	reg clk;
	parameter latency = 5;
    parameter N = 181;
	parameter total_record = 3*N;
	reg x0_0, x1_0, x2_0, x3_0,x0_1, x1_1, x2_1, x3_1,r;

	wire Y0_0, Y1_0, Y2_0, Y3_0, Y0_1, Y1_1, Y2_1, Y3_1;

	integer i, count;
	reg [3:0] out0Comb[0:total_record-1];
	reg [3:0] out1Comb[0:total_record-1];
	initial $readmemb("out0Comb.txt",out0Comb);
	initial $readmemb("out1Comb.txt",out1Comb);
	initial clk = 1'b0;

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
		.Y3_1(Y3_1)
	);
	always begin
	#5 clk = ~clk;
	end
	initial begin
		$dumpfile("sbox_vcd.vcd");
		$dumpvars();
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
	
		if (count==0) begin		
		
			if(i>0) begin
				$display("Test Case: %0d:  \tTime: %0t",i,$time);
				$display("Input %c%c: %b%b%b%b  %b%b%b%b \txor= %b%b%b%b",32,32,x0_0, x1_0, x2_0, x3_0, x0_1, x1_1, x2_1, x3_1,x0_0^x0_1,x1_0^x1_1,x2_0^x2_1,x3_0^x3_1);
				$display("Output: %b%b%b%b  %b%b%b%b \txor= %b%b%b%b",Y3_0, Y2_0, Y1_0, Y0_0, Y3_1, Y2_1, Y1_1, Y0_1,Y3_0^Y3_1,Y2_0^Y2_1,Y1_0^Y1_1,Y0_0^Y0_1);
				$display("---------------------------------------------------------------");
			end	
					
			//exit condition
			if (i >= total_record) begin
				$finish;
			end

			//input				
			x0_0 = out0Comb[i][3];
			x1_0 = out0Comb[i][2];
			x2_0 = out0Comb[i][1];
			x3_0 = out0Comb[i][0];

			x0_1 = out1Comb[i][3];
			x1_1 = out1Comb[i][2];
			x2_1 = out1Comb[i][1];
			x3_1 = out1Comb[i][0];
			r = $random;
			i = i+1;
		end
		count = (count+1)%(latency);	
	end
endmodule
