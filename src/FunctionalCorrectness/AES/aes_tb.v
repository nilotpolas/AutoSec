`timescale 1ns/1ns
module aes_tb;

	integer x0_0, x0_1;
	reg clk;
	reg [7:0] t0, t1, r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, 	r22, r23, r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35, dec_0, dec_1, dec_255, dec_169, dec_129, dec_9, dec_72, dec_242, dec_243, dec_152, dec_240, dec_4, dec_15, dec_12, dec_2, dec_3, dec_16, dec_36, dec_220, dec_11, dec_158, dec_45, dec_88, dec_99; 
	wire [7:0] Y0_0, Y0_1;
     sbox dut(
	.clk(clk),
	.t0(t0),
	.t1(t1),
	.r0(r0),
	.r1(r1),
	.r2(r2),
	.r3(r3),
	.r4(r4),
	.r5(r5),
	.r6(r6),
	.r7(r7),
	.r8(r8),
	.r9(r9),
	.r10(r10),
	.r11(r11),
	.r12(r12),
	.r13(r13),
	.r14(r14),
	.r15(r15),
	.r16(r16),
	.r17(r17),
	.r18(r18),
	.r19(r19),
	.r20(r20),
	.r21(r21),
	.r22(r22),
	.r23(r23),
	.r24(r24),
	.r25(r25),
	.r26(r26),
	.r27(r27),
	.r28(r28),
	.r29(r29),
	.r30(r30),
	.r31(r31),
	.r32(r32),
	.r33(r33),
	.r34(r34),
	.r35(r35),
	.dec_0(dec_0),
	.dec_1(dec_1),
	.dec_255(dec_255),
	.dec_169(dec_169),
	.dec_129(dec_129),
	.dec_9(dec_9),
	.dec_72(dec_72),
	.dec_242(dec_242),
	.dec_243(dec_243),
	.dec_152(dec_152),
	.dec_240(dec_240),
	.dec_4(dec_4),
	.dec_15(dec_15),
	.dec_12(dec_12),
	.dec_2(dec_2),
	.dec_3(dec_3),
	.dec_16(dec_16),
	.dec_36(dec_36),
	.dec_220(dec_220),
	.dec_11(dec_11),
	.dec_158(dec_158),
	.dec_45(dec_45),
	.dec_88(dec_88),
	.dec_99(dec_99),
	.y0(Y0_0),
	.y1(Y0_1));
	

	always begin
	#5 clk = ~clk;
	end
	initial begin
		$dumpfile("sbox_vcd.vcd");
		$dumpvars();
		clk = 0;
		x0_0 = 0;
		x0_1 = 0;
		
	end
	always @(posedge clk) begin
		for (x0_0 = 0; x0_0 <= 255; x0_0 = x0_0 + 1) begin
			for (x0_1 = 0; x0_1 <= 255; x0_1 = x0_1 + 1) begin
				t0 = x0_0;
				t1 = x0_1;
				r0 = 183;
				r1 = 183;
				r2 = 30;
				r3 = 196;
				r4 = 16;
				r5 = 36;
				r6 = 85;
				r7 = 54;
				r8 = 18;
				r9 = 238;
				r10 = 202;
				r11 = 134;
				r12 = 244;
				r13 = 252;
				r14 = 204;
				r15 = 111;
				r16 = 123;
				r17 = 144;
				r18 = 29;
				r19 = 135;
				r20 = 219;
				r21 = 149;
				r22 = 181;
				r23 = 97;
				r24 = 250;
				r25 = 25;
				r26 = 11;
				r27 = 223;
				r28 = 37;
				r29 = 16;
				r30 = 106;
				r31 = 73;
				r32 = 137;
				r33 = 232;
				r34 = 187;
				r35 = 172;
				dec_0 = 0;
				dec_1 = 1;
				dec_255 = 255;
				dec_169 = 169;
				dec_129 = 129;
				dec_9 = 9;
				dec_72 = 72;
				dec_242 = 242;
				dec_243 = 243;
				dec_152 = 152;
				dec_240 = 240;
				dec_4 = 4;
				dec_15 = 15;
				dec_12 = 12;
				dec_2 = 2;
				dec_3 = 3;
				dec_16 = 16;
				dec_36 = 36;
				dec_220 = 220;
				dec_11 = 11;
				dec_158 = 158;
				dec_45 = 45;
				dec_88 = 88;
				dec_99 = 99;
				#34
				$display("%d, %d", x0_0 ^ x0_1, Y0_0 ^ Y0_1);
			end
		end
			
		$finish;
	end
endmodule
