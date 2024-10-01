/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Expert(TM) in wire load mode
// Version   : O-2018.06-SP1
// Date      : Thu May 16 20:11:38 2024
/////////////////////////////////////////////////////////////


module sbox ( clk, x0_0, x1_0, x2_0, x3_0, x0_1, x1_1, x2_1, x3_1, r, Y0_0, 
        Y1_0, Y2_0, Y3_0, Y0_1, Y1_1, Y2_1, Y3_1 );
  input clk, x0_0, x1_0, x2_0, x3_0, x0_1, x1_1, x2_1, x3_1, r;
  output Y0_0, Y1_0, Y2_0, Y3_0, Y0_1, Y1_1, Y2_1, Y3_1;
  wire   L8_0, L5_0, L8_1, L5_1, L2_0, L3_0, L2_1, L3_1, a0_neg_hpc20_reg,
         r_inp_reg, u0_hpc20, a1_neg_hpc20_reg, u1_hpc20, v0_hpc20, v1_hpc20,
         Q0_0_reg, Q1_0_reg, p0_hpc20, v1_hpc20_reg, p1_hpc20, u0_hpc20_reg,
         p1_hpc20_reg, p0_hpc20_reg, T0_0, Q0_1_reg, Q1_1_reg, p2_hpc20,
         v0_hpc20_reg, p3_hpc20, u1_hpc20_reg, p3_hpc20_reg, p2_hpc20_reg,
         T0_1, a0_neg_hpc21_reg, u0_hpc21, a1_neg_hpc21_reg, u1_hpc21,
         v0_hpc21, v1_hpc21, x1_0_inp_reg, Q4_0_reg, p0_hpc21, v1_hpc21_reg,
         p1_hpc21, u0_hpc21_reg, p1_hpc21_reg, p0_hpc21_reg, T2_0,
         x1_1_inp_reg, Q4_1_reg, p2_hpc21, v0_hpc21_reg, p3_hpc21,
         u1_hpc21_reg, p3_hpc21_reg, p2_hpc21_reg, T2_1, z135_assgn135,
         z139_assgn139, Q7_0, z141_assgn141, Q6_0, z143_assgn143,
         z147_assgn147, Q7_1, z149_assgn149, Q6_1, z155_assgn155, u0_hpc22,
         z157_assgn157, u1_hpc22, v0_hpc22, v1_hpc22, z163_assgn163, p0_hpc22,
         z165_assgn165, p1_hpc22, u0_hpc22_reg, p1_hpc22_reg, p0_hpc22_reg,
         z171_assgn171, p2_hpc22, z173_assgn173, p3_hpc22, u1_hpc22_reg,
         p3_hpc22_reg, p2_hpc22_reg, z183_assgn183, u0_hpc23, z185_assgn185,
         u1_hpc23, z187_assgn187, v0_hpc23, z189_assgn189, v1_hpc23, Q6_0_reg,
         Q7_0_reg, p0_hpc23, v1_hpc23_reg, p1_hpc23, z196_assgn196,
         p1_hpc23_reg, p0_hpc23_reg, Q6_1_reg, Q7_1_reg, p2_hpc23,
         v0_hpc23_reg, p3_hpc23, z204_assgn204, p3_hpc23_reg, p2_hpc23_reg,
         T0_0_reg, L7_0, z209_assgn209, T0_1_reg, L7_1, z213_assgn213,
         T2_0_reg, z218_assgn218, T2_1_reg, z222_assgn222, z224_assgn224,
         z1_assgn1, L7_0_reg, z3_assgn3, z5_assgn5, z235_assgn235, z7_assgn7,
         z240_assgn240, z9_assgn9, L7_1_reg, z11_assgn11, z13_assgn13,
         z251_assgn251, z15_assgn15, z483_assgn4830, z489_assgn4890,
         z495_assgn4950, z495_assgn4951, z501_assgn5010, z501_assgn5011,
         z505_assgn5050, z523_assgn5230, z525_assgn5250, z543_assgn5430,
         z373_assgn3730, z379_assgn3790, z383_assgn3830, z387_assgn3870,
         z393_assgn3930, z397_assgn3970, z405_assgn4050, z409_assgn4090,
         z417_assgn4170, z421_assgn4210, z429_assgn4290, z433_assgn4330,
         z445_assgn4450, z449_assgn4490, z453_assgn4530, z457_assgn4570,
         z465_assgn4650, z475_assgn4750, z483_assgn4831, z489_assgn4891,
         z495_assgn4952, z501_assgn5012, z505_assgn5051, z509_assgn5090,
         z517_assgn5170, z519_assgn5190, z523_assgn5231, z525_assgn5251,
         z529_assgn5290, z537_assgn5370, z539_assgn5390, z543_assgn5431, n1,
         n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16,
         n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30,
         n31, n32, n33, n34, n35, n36, n37, n38, n39, n40;

  dfnrq2 z539_assgn5390_reg ( .D(L5_1), .CP(clk), .Q(z539_assgn5390) );
  dfnrq2 z525_assgn5250_reg ( .D(x3_1), .CP(clk), .Q(z525_assgn5250) );
  dfnrq2 z525_assgn5251_reg ( .D(z525_assgn5250), .CP(clk), .Q(z525_assgn5251)
         );
  dfnrq2 z519_assgn5190_reg ( .D(L5_0), .CP(clk), .Q(z519_assgn5190) );
  dfnrq2 z505_assgn5050_reg ( .D(x3_0), .CP(clk), .Q(z505_assgn5050) );
  dfnrq2 z505_assgn5051_reg ( .D(z505_assgn5050), .CP(clk), .Q(z505_assgn5051)
         );
  dfnrq2 z501_assgn5010_reg ( .D(L8_1), .CP(clk), .Q(z501_assgn5010) );
  dfnrq2 z501_assgn5011_reg ( .D(z501_assgn5010), .CP(clk), .Q(z501_assgn5011)
         );
  dfnrq2 z501_assgn5012_reg ( .D(z501_assgn5011), .CP(clk), .Q(z501_assgn5012)
         );
  dfnrq2 z495_assgn4950_reg ( .D(L8_0), .CP(clk), .Q(z495_assgn4950) );
  dfnrq2 z495_assgn4951_reg ( .D(z495_assgn4950), .CP(clk), .Q(z495_assgn4951)
         );
  dfnrq2 z495_assgn4952_reg ( .D(z495_assgn4951), .CP(clk), .Q(z495_assgn4952)
         );
  dfnrq2 z489_assgn4890_reg ( .D(n10), .CP(clk), .Q(z489_assgn4890) );
  dfnrq2 z489_assgn4891_reg ( .D(z489_assgn4890), .CP(clk), .Q(z489_assgn4891)
         );
  dfnrq2 z483_assgn4830_reg ( .D(n5), .CP(clk), .Q(z483_assgn4830) );
  dfnrq2 z483_assgn4831_reg ( .D(z483_assgn4830), .CP(clk), .Q(z483_assgn4831)
         );
  dfnrq2 z457_assgn4570_reg ( .D(r), .CP(clk), .Q(z457_assgn4570) );
  dfnrq2 z453_assgn4530_reg ( .D(r), .CP(clk), .Q(z453_assgn4530) );
  dfnrq2 z449_assgn4490_reg ( .D(r), .CP(clk), .Q(z449_assgn4490) );
  dfnrq2 z445_assgn4450_reg ( .D(r), .CP(clk), .Q(z445_assgn4450) );
  dfnrq2 z433_assgn4330_reg ( .D(v0_hpc22), .CP(clk), .Q(z433_assgn4330) );
  dfnrq2 z429_assgn4290_reg ( .D(n14), .CP(clk), .Q(z429_assgn4290) );
  dfnrq2 z421_assgn4210_reg ( .D(v1_hpc22), .CP(clk), .Q(z421_assgn4210) );
  dfnrq2 z417_assgn4170_reg ( .D(n9), .CP(clk), .Q(z417_assgn4170) );
  dfnrq2 z409_assgn4090_reg ( .D(r), .CP(clk), .Q(z409_assgn4090) );
  dfnrq2 z405_assgn4050_reg ( .D(r), .CP(clk), .Q(z405_assgn4050) );
  dfnrq2 z397_assgn3970_reg ( .D(L3_1), .CP(clk), .Q(z397_assgn3970) );
  dfnrq2 z393_assgn3930_reg ( .D(L5_1), .CP(clk), .Q(z393_assgn3930) );
  dfnrq2 z387_assgn3870_reg ( .D(L2_1), .CP(clk), .Q(z387_assgn3870) );
  dfnrq2 z383_assgn3830_reg ( .D(L3_0), .CP(clk), .Q(z383_assgn3830) );
  dfnrq2 z379_assgn3790_reg ( .D(L5_0), .CP(clk), .Q(z379_assgn3790) );
  dfnrq2 z373_assgn3730_reg ( .D(L2_0), .CP(clk), .Q(z373_assgn3730) );
  dfnrq2 a0_neg_hpc20_reg_reg ( .D(n6), .CP(clk), .Q(a0_neg_hpc20_reg) );
  dfnrq2 r_inp_reg_reg ( .D(r), .CP(clk), .Q(r_inp_reg) );
  dfnrq2 a1_neg_hpc20_reg_reg ( .D(n11), .CP(clk), .Q(a1_neg_hpc20_reg) );
  dfnrq2 Q0_0_reg_reg ( .D(n38), .CP(clk), .Q(Q0_0_reg) );
  dfnrq2 Q1_0_reg_reg ( .D(n37), .CP(clk), .Q(Q1_0_reg) );
  dfnrq2 v1_hpc20_reg_reg ( .D(v1_hpc20), .CP(clk), .Q(v1_hpc20_reg) );
  dfnrq2 u0_hpc20_reg_reg ( .D(u0_hpc20), .CP(clk), .Q(u0_hpc20_reg) );
  dfnrq2 p1_hpc20_reg_reg ( .D(p1_hpc20), .CP(clk), .Q(p1_hpc20_reg) );
  dfnrq2 p0_hpc20_reg_reg ( .D(p0_hpc20), .CP(clk), .Q(p0_hpc20_reg) );
  dfnrq2 Q0_1_reg_reg ( .D(n40), .CP(clk), .Q(Q0_1_reg) );
  dfnrq2 Q1_1_reg_reg ( .D(n39), .CP(clk), .Q(Q1_1_reg) );
  dfnrq2 v0_hpc20_reg_reg ( .D(v0_hpc20), .CP(clk), .Q(v0_hpc20_reg) );
  dfnrq2 u1_hpc20_reg_reg ( .D(u1_hpc20), .CP(clk), .Q(u1_hpc20_reg) );
  dfnrq2 p3_hpc20_reg_reg ( .D(p3_hpc20), .CP(clk), .Q(p3_hpc20_reg) );
  dfnrq2 p2_hpc20_reg_reg ( .D(p2_hpc20), .CP(clk), .Q(p2_hpc20_reg) );
  dfnrq2 a0_neg_hpc21_reg_reg ( .D(n7), .CP(clk), .Q(a0_neg_hpc21_reg) );
  dfnrq2 a1_neg_hpc21_reg_reg ( .D(n12), .CP(clk), .Q(a1_neg_hpc21_reg) );
  dfnrq2 x1_0_inp_reg_reg ( .D(x1_0), .CP(clk), .Q(x1_0_inp_reg) );
  dfnrq2 Q4_0_reg_reg ( .D(n8), .CP(clk), .Q(Q4_0_reg) );
  dfnrq2 v1_hpc21_reg_reg ( .D(v1_hpc21), .CP(clk), .Q(v1_hpc21_reg) );
  dfnrq2 u0_hpc21_reg_reg ( .D(u0_hpc21), .CP(clk), .Q(u0_hpc21_reg) );
  dfnrq2 p1_hpc21_reg_reg ( .D(p1_hpc21), .CP(clk), .Q(p1_hpc21_reg) );
  dfnrq2 p0_hpc21_reg_reg ( .D(p0_hpc21), .CP(clk), .Q(p0_hpc21_reg) );
  dfnrq2 x1_1_inp_reg_reg ( .D(x1_1), .CP(clk), .Q(x1_1_inp_reg) );
  dfnrq2 Q4_1_reg_reg ( .D(n13), .CP(clk), .Q(Q4_1_reg) );
  dfnrq2 v0_hpc21_reg_reg ( .D(v0_hpc21), .CP(clk), .Q(v0_hpc21_reg) );
  dfnrq2 u1_hpc21_reg_reg ( .D(u1_hpc21), .CP(clk), .Q(u1_hpc21_reg) );
  dfnrq2 p3_hpc21_reg_reg ( .D(p3_hpc21), .CP(clk), .Q(p3_hpc21_reg) );
  dfnrq2 p2_hpc21_reg_reg ( .D(p2_hpc21), .CP(clk), .Q(p2_hpc21_reg) );
  dfnrq2 z135_assgn135_reg ( .D(z373_assgn3730), .CP(clk), .Q(z135_assgn135)
         );
  dfnrq2 z139_assgn139_reg ( .D(z379_assgn3790), .CP(clk), .Q(z139_assgn139)
         );
  dfnrq2 z141_assgn141_reg ( .D(z383_assgn3830), .CP(clk), .Q(z141_assgn141)
         );
  dfnrq2 z143_assgn143_reg ( .D(z387_assgn3870), .CP(clk), .Q(z143_assgn143)
         );
  dfnrq2 z147_assgn147_reg ( .D(z393_assgn3930), .CP(clk), .Q(z147_assgn147)
         );
  dfnrq2 z149_assgn149_reg ( .D(z397_assgn3970), .CP(clk), .Q(z149_assgn149)
         );
  dfnrq2 z155_assgn155_reg ( .D(z405_assgn4050), .CP(clk), .Q(z155_assgn155)
         );
  dfnrq2 z157_assgn157_reg ( .D(z409_assgn4090), .CP(clk), .Q(z157_assgn157)
         );
  dfnrq2 z163_assgn163_reg ( .D(z417_assgn4170), .CP(clk), .Q(z163_assgn163)
         );
  dfnrq2 z165_assgn165_reg ( .D(z421_assgn4210), .CP(clk), .Q(z165_assgn165)
         );
  dfnrq2 u0_hpc22_reg_reg ( .D(u0_hpc22), .CP(clk), .Q(u0_hpc22_reg) );
  dfnrq2 p1_hpc22_reg_reg ( .D(p1_hpc22), .CP(clk), .Q(p1_hpc22_reg) );
  dfnrq2 p0_hpc22_reg_reg ( .D(p0_hpc22), .CP(clk), .Q(p0_hpc22_reg) );
  dfnrq2 z171_assgn171_reg ( .D(z429_assgn4290), .CP(clk), .Q(z171_assgn171)
         );
  dfnrq2 z173_assgn173_reg ( .D(z433_assgn4330), .CP(clk), .Q(z173_assgn173)
         );
  dfnrq2 u1_hpc22_reg_reg ( .D(u1_hpc22), .CP(clk), .Q(u1_hpc22_reg) );
  dfnrq2 p3_hpc22_reg_reg ( .D(p3_hpc22), .CP(clk), .Q(p3_hpc22_reg) );
  dfnrq2 p2_hpc22_reg_reg ( .D(p2_hpc22), .CP(clk), .Q(p2_hpc22_reg) );
  dfnrq2 z183_assgn183_reg ( .D(z445_assgn4450), .CP(clk), .Q(z183_assgn183)
         );
  dfnrq2 z465_assgn4650_reg ( .D(u0_hpc23), .CP(clk), .Q(z465_assgn4650) );
  dfnrq2 z185_assgn185_reg ( .D(z449_assgn4490), .CP(clk), .Q(z185_assgn185)
         );
  dfnrq2 z475_assgn4750_reg ( .D(u1_hpc23), .CP(clk), .Q(z475_assgn4750) );
  dfnrq2 z187_assgn187_reg ( .D(z453_assgn4530), .CP(clk), .Q(z187_assgn187)
         );
  dfnrq2 z189_assgn189_reg ( .D(z457_assgn4570), .CP(clk), .Q(z189_assgn189)
         );
  dfnrq2 Q6_0_reg_reg ( .D(Q6_0), .CP(clk), .Q(Q6_0_reg) );
  dfnrq2 Q7_0_reg_reg ( .D(Q7_0), .CP(clk), .Q(Q7_0_reg) );
  dfnrq2 v1_hpc23_reg_reg ( .D(v1_hpc23), .CP(clk), .Q(v1_hpc23_reg) );
  dfnrq2 z196_assgn196_reg ( .D(z465_assgn4650), .CP(clk), .Q(z196_assgn196)
         );
  dfnrq2 p1_hpc23_reg_reg ( .D(p1_hpc23), .CP(clk), .Q(p1_hpc23_reg) );
  dfnrq2 p0_hpc23_reg_reg ( .D(p0_hpc23), .CP(clk), .Q(p0_hpc23_reg) );
  dfnrq2 Q6_1_reg_reg ( .D(Q6_1), .CP(clk), .Q(Q6_1_reg) );
  dfnrq2 Q7_1_reg_reg ( .D(Q7_1), .CP(clk), .Q(Q7_1_reg) );
  dfnrq2 v0_hpc23_reg_reg ( .D(v0_hpc23), .CP(clk), .Q(v0_hpc23_reg) );
  dfnrq2 z204_assgn204_reg ( .D(z475_assgn4750), .CP(clk), .Q(z204_assgn204)
         );
  dfnrq2 p3_hpc23_reg_reg ( .D(p3_hpc23), .CP(clk), .Q(p3_hpc23_reg) );
  dfnrq2 p2_hpc23_reg_reg ( .D(p2_hpc23), .CP(clk), .Q(p2_hpc23_reg) );
  dfnrq2 T0_0_reg_reg ( .D(T0_0), .CP(clk), .Q(T0_0_reg) );
  dfnrq2 z209_assgn209_reg ( .D(z483_assgn4831), .CP(clk), .Q(z209_assgn209)
         );
  dfnrq2 T0_1_reg_reg ( .D(T0_1), .CP(clk), .Q(T0_1_reg) );
  dfnrq2 z213_assgn213_reg ( .D(z489_assgn4891), .CP(clk), .Q(z213_assgn213)
         );
  dfnrq2 T2_0_reg_reg ( .D(T2_0), .CP(clk), .Q(T2_0_reg) );
  dfnrq2 z517_assgn5170_reg ( .D(z5_assgn5), .CP(clk), .Q(z517_assgn5170) );
  dfnrq2 z218_assgn218_reg ( .D(z495_assgn4952), .CP(clk), .Q(z218_assgn218)
         );
  dfnrq2 T2_1_reg_reg ( .D(T2_1), .CP(clk), .Q(T2_1_reg) );
  dfnrq2 z537_assgn5370_reg ( .D(z13_assgn13), .CP(clk), .Q(z537_assgn5370) );
  dfnrq2 z222_assgn222_reg ( .D(z501_assgn5012), .CP(clk), .Q(z222_assgn222)
         );
  dfnrq2 z224_assgn224_reg ( .D(z505_assgn5051), .CP(clk), .Q(z224_assgn224)
         );
  dfnrq2 z509_assgn5090_reg ( .D(z1_assgn1), .CP(clk), .Q(z509_assgn5090) );
  dfnrq2 Y0_0_reg ( .D(z509_assgn5090), .CP(clk), .Q(Y0_0) );
  dfnrq2 L7_0_reg_reg ( .D(L7_0), .CP(clk), .Q(L7_0_reg) );
  dfnrq2 Y1_0_reg ( .D(z3_assgn3), .CP(clk), .Q(Y1_0) );
  dfnrq2 Y2_0_reg ( .D(z517_assgn5170), .CP(clk), .Q(Y2_0) );
  dfnrq2 z235_assgn235_reg ( .D(z519_assgn5190), .CP(clk), .Q(z235_assgn235)
         );
  dfnrq2 z523_assgn5230_reg ( .D(z7_assgn7), .CP(clk), .Q(z523_assgn5230) );
  dfnrq2 z523_assgn5231_reg ( .D(z523_assgn5230), .CP(clk), .Q(z523_assgn5231)
         );
  dfnrq2 Y3_0_reg ( .D(z523_assgn5231), .CP(clk), .Q(Y3_0) );
  dfnrq2 z240_assgn240_reg ( .D(z525_assgn5251), .CP(clk), .Q(z240_assgn240)
         );
  dfnrq2 z529_assgn5290_reg ( .D(z9_assgn9), .CP(clk), .Q(z529_assgn5290) );
  dfnrq2 Y0_1_reg ( .D(z529_assgn5290), .CP(clk), .Q(Y0_1) );
  dfnrq2 L7_1_reg_reg ( .D(L7_1), .CP(clk), .Q(L7_1_reg) );
  dfnrq2 Y1_1_reg ( .D(z11_assgn11), .CP(clk), .Q(Y1_1) );
  dfnrq2 Y2_1_reg ( .D(z537_assgn5370), .CP(clk), .Q(Y2_1) );
  dfnrq2 z251_assgn251_reg ( .D(z539_assgn5390), .CP(clk), .Q(z251_assgn251)
         );
  dfnrq2 z543_assgn5430_reg ( .D(z15_assgn15), .CP(clk), .Q(z543_assgn5430) );
  dfnrq2 z543_assgn5431_reg ( .D(z543_assgn5430), .CP(clk), .Q(z543_assgn5431)
         );
  dfnrq2 Y3_1_reg ( .D(z543_assgn5431), .CP(clk), .Q(Y3_1) );
  inv0d1 U3 ( .I(n28), .ZN(n1) );
  inv0d1 U4 ( .I(Q6_0), .ZN(n2) );
  inv0d1 U5 ( .I(n27), .ZN(n3) );
  inv0d1 U6 ( .I(Q6_1), .ZN(n4) );
  inv0d1 U7 ( .I(L2_0), .ZN(n5) );
  inv0d1 U8 ( .I(n38), .ZN(n6) );
  inv0d1 U9 ( .I(x1_0), .ZN(n7) );
  inv0d1 U10 ( .I(x2_0), .ZN(n8) );
  inv0d1 U11 ( .I(x3_0), .ZN(n9) );
  inv0d1 U12 ( .I(L2_1), .ZN(n10) );
  inv0d1 U13 ( .I(n40), .ZN(n11) );
  inv0d1 U14 ( .I(x1_1), .ZN(n12) );
  inv0d1 U15 ( .I(x2_1), .ZN(n13) );
  inv0d1 U16 ( .I(x3_1), .ZN(n14) );
  xr02d2 U17 ( .A1(n15), .A2(n16), .Z(z9_assgn9) );
  xr02d2 U18 ( .A1(T0_1_reg), .A2(z240_assgn240), .Z(n16) );
  xr02d2 U19 ( .A1(z235_assgn235), .A2(T2_0), .Z(z7_assgn7) );
  xr02d2 U20 ( .A1(n17), .A2(n18), .Z(z5_assgn5) );
  xr02d2 U21 ( .A1(z209_assgn209), .A2(T2_0_reg), .Z(n18) );
  xr02d2 U22 ( .A1(n19), .A2(n20), .Z(z3_assgn3) );
  xr02d2 U23 ( .A1(p0_hpc23_reg), .A2(L7_0_reg), .Z(n20) );
  xr02d2 U24 ( .A1(p1_hpc23_reg), .A2(n21), .Z(n19) );
  xr02d2 U25 ( .A1(z218_assgn218), .A2(z196_assgn196), .Z(n21) );
  xr02d2 U26 ( .A1(L7_0), .A2(n22), .Z(z1_assgn1) );
  xr02d2 U27 ( .A1(T2_0_reg), .A2(z224_assgn224), .Z(n22) );
  xr02d2 U28 ( .A1(z251_assgn251), .A2(T2_1), .Z(z15_assgn15) );
  xr02d2 U29 ( .A1(z213_assgn213), .A2(n15), .Z(z13_assgn13) );
  xr02d2 U30 ( .A1(n23), .A2(T2_1_reg), .Z(n15) );
  xr02d2 U31 ( .A1(n24), .A2(n25), .Z(z11_assgn11) );
  xr02d2 U32 ( .A1(p2_hpc23_reg), .A2(L7_1_reg), .Z(n25) );
  xr02d2 U33 ( .A1(p3_hpc23_reg), .A2(n26), .Z(n24) );
  xr02d2 U34 ( .A1(z222_assgn222), .A2(z204_assgn204), .Z(n26) );
  xr02d2 U35 ( .A1(z189_assgn189), .A2(Q7_1), .Z(v1_hpc23) );
  xr02d2 U36 ( .A1(n14), .A2(r), .Z(v1_hpc22) );
  xr02d2 U37 ( .A1(n13), .A2(r), .Z(v1_hpc21) );
  xr02d2 U38 ( .A1(r), .A2(n39), .Z(v1_hpc20) );
  xr02d2 U39 ( .A1(z187_assgn187), .A2(Q7_0), .Z(v0_hpc23) );
  xr02d2 U40 ( .A1(n9), .A2(r), .Z(v0_hpc22) );
  xr02d2 U41 ( .A1(n8), .A2(r), .Z(v0_hpc21) );
  xr02d2 U42 ( .A1(r), .A2(n37), .Z(v0_hpc20) );
  an02d2 U43 ( .A1(z185_assgn185), .A2(n4), .Z(u1_hpc23) );
  an02d2 U44 ( .A1(z157_assgn157), .A2(n3), .Z(u1_hpc22) );
  an02d2 U45 ( .A1(r_inp_reg), .A2(a1_neg_hpc21_reg), .Z(u1_hpc21) );
  an02d2 U46 ( .A1(a1_neg_hpc20_reg), .A2(r_inp_reg), .Z(u1_hpc20) );
  an02d2 U47 ( .A1(z183_assgn183), .A2(n2), .Z(u0_hpc23) );
  an02d2 U48 ( .A1(z155_assgn155), .A2(n1), .Z(u0_hpc22) );
  an02d2 U49 ( .A1(a0_neg_hpc21_reg), .A2(r_inp_reg), .Z(u0_hpc21) );
  an02d2 U50 ( .A1(a0_neg_hpc20_reg), .A2(r_inp_reg), .Z(u0_hpc20) );
  an02d2 U51 ( .A1(v0_hpc23_reg), .A2(Q6_1_reg), .Z(p3_hpc23) );
  an02d2 U52 ( .A1(z173_assgn173), .A2(n27), .Z(p3_hpc22) );
  an02d2 U53 ( .A1(x1_1_inp_reg), .A2(v0_hpc21_reg), .Z(p3_hpc21) );
  an02d2 U54 ( .A1(v0_hpc20_reg), .A2(Q0_1_reg), .Z(p3_hpc20) );
  an02d2 U55 ( .A1(Q7_1_reg), .A2(Q6_1_reg), .Z(p2_hpc23) );
  an02d2 U56 ( .A1(z171_assgn171), .A2(n27), .Z(p2_hpc22) );
  xr02d2 U57 ( .A1(T0_1), .A2(z143_assgn143), .Z(n27) );
  an02d2 U58 ( .A1(Q4_1_reg), .A2(x1_1_inp_reg), .Z(p2_hpc21) );
  an02d2 U59 ( .A1(Q1_1_reg), .A2(Q0_1_reg), .Z(p2_hpc20) );
  an02d2 U60 ( .A1(v1_hpc23_reg), .A2(Q6_0_reg), .Z(p1_hpc23) );
  an02d2 U61 ( .A1(z165_assgn165), .A2(n28), .Z(p1_hpc22) );
  an02d2 U62 ( .A1(x1_0_inp_reg), .A2(v1_hpc21_reg), .Z(p1_hpc21) );
  an02d2 U63 ( .A1(v1_hpc20_reg), .A2(Q0_0_reg), .Z(p1_hpc20) );
  an02d2 U64 ( .A1(Q7_0_reg), .A2(Q6_0_reg), .Z(p0_hpc23) );
  an02d2 U65 ( .A1(z163_assgn163), .A2(n28), .Z(p0_hpc22) );
  xr02d2 U66 ( .A1(T0_0), .A2(z135_assgn135), .Z(n28) );
  an02d2 U67 ( .A1(Q4_0_reg), .A2(x1_0_inp_reg), .Z(p0_hpc21) );
  an02d2 U68 ( .A1(Q1_0_reg), .A2(Q0_0_reg), .Z(p0_hpc20) );
  xr02d2 U69 ( .A1(T0_1), .A2(z147_assgn147), .Z(Q7_1) );
  xr02d2 U70 ( .A1(T0_0), .A2(z139_assgn139), .Z(Q7_0) );
  xr02d2 U71 ( .A1(n29), .A2(T0_1), .Z(Q6_1) );
  xr02d2 U72 ( .A1(p2_hpc20_reg), .A2(n30), .Z(T0_1) );
  xr02d2 U73 ( .A1(u1_hpc20_reg), .A2(p3_hpc20_reg), .Z(n30) );
  xr02d2 U74 ( .A1(T2_1), .A2(z149_assgn149), .Z(n29) );
  xr02d2 U75 ( .A1(p2_hpc21_reg), .A2(n31), .Z(T2_1) );
  xr02d2 U76 ( .A1(u1_hpc21_reg), .A2(p3_hpc21_reg), .Z(n31) );
  xr02d2 U77 ( .A1(n32), .A2(T0_0), .Z(Q6_0) );
  xr02d2 U78 ( .A1(p0_hpc20_reg), .A2(n33), .Z(T0_0) );
  xr02d2 U79 ( .A1(u0_hpc20_reg), .A2(p1_hpc20_reg), .Z(n33) );
  xr02d2 U80 ( .A1(T2_0), .A2(z141_assgn141), .Z(n32) );
  xr02d2 U81 ( .A1(p0_hpc21_reg), .A2(n34), .Z(T2_0) );
  xr02d2 U82 ( .A1(u0_hpc21_reg), .A2(p1_hpc21_reg), .Z(n34) );
  xr02d2 U83 ( .A1(x2_1), .A2(x0_1), .Z(L8_1) );
  xr02d2 U84 ( .A1(x2_0), .A2(x0_0), .Z(L8_0) );
  xr02d2 U85 ( .A1(T0_1_reg), .A2(n23), .Z(L7_1) );
  xr02d2 U86 ( .A1(p2_hpc22_reg), .A2(n35), .Z(n23) );
  xr02d2 U87 ( .A1(u1_hpc22_reg), .A2(p3_hpc22_reg), .Z(n35) );
  xr02d2 U88 ( .A1(n17), .A2(T0_0_reg), .Z(L7_0) );
  xr02d2 U89 ( .A1(p0_hpc22_reg), .A2(n36), .Z(n17) );
  xr02d2 U90 ( .A1(u0_hpc22_reg), .A2(p1_hpc22_reg), .Z(n36) );
  xr02d2 U91 ( .A1(x3_1), .A2(x0_1), .Z(L5_1) );
  xr02d2 U92 ( .A1(x3_0), .A2(x0_0), .Z(L5_0) );
  xr02d2 U93 ( .A1(n14), .A2(n11), .Z(L3_1) );
  xr02d2 U94 ( .A1(n9), .A2(n6), .Z(L3_0) );
  xr02d2 U95 ( .A1(x2_1), .A2(n39), .Z(L2_1) );
  xr02d2 U96 ( .A1(x0_1), .A2(n12), .Z(n39) );
  xr02d2 U97 ( .A1(x2_0), .A2(n37), .Z(L2_0) );
  xr02d2 U98 ( .A1(x0_0), .A2(n7), .Z(n37) );
  xr02d2 U99 ( .A1(n12), .A2(x2_1), .Z(n40) );
  xr02d2 U100 ( .A1(n7), .A2(x2_0), .Z(n38) );
endmodule
