// #include <stdio.h>
// #include <sys/types.h>
// #include <stdio.h>
// #include <stdlib.h>
// #include <time.h>

static int A2X[8] = {0x98, 0xF3, 0xF2, 0x48, 0x09, 0x81, 0xA9, 0xFF},
           X2A[8] = {0x64, 0x78, 0x6E, 0x8C, 0x68, 0x29, 0xDE, 0x60},
           X2S[8] = {0x58, 0x2D, 0x9E, 0x0B, 0xDC, 0x04, 0x03, 0x24},
           S2X[8] = {0x8C, 0x79, 0x05, 0xEB, 0x12, 0x04, 0x51, 0x53};

// int reg(int a)
// {
//     return a;
// }

void hpc1(int a0, int a1, int b0, int b1, int *y0, int *y1, int r0, int r1)
{
    int r00, r10;
    r00 = r0 % 2;
    r10 = r1 % 2;
    int b0_preshared, b1_preshared, i1, i2, p2, p3, p1, p4;
    b0_preshared = b0 ^ r00;
    b1_preshared = b1 ^ r00;
    p2 = a0 & reg(b1_preshared);
    i1 = p2 ^ r10;
    p3 = a1 & reg(b0_preshared);
    i2 = p3 ^ r10;
    p1 = a0 & reg(b0_preshared);
    p4 = a1 & reg(b1_preshared);
    *y0 = reg(i1) ^ p1;
    *y1 = reg(i2) ^ p4;
}
/* multiply in GF(2^2), using normal basis (Omega^2,Omega) */
void G4_mul(int x0, int x1, int y0, int y1, int *e0_0, int *e1_0, int r0, int r1, int r2, int r3, int r4, int r5)
{
    int r00, r10, r20, r30, r40, r50;
    r00 = r0 % 4;
    r10 = r1 % 4;
    r20 = r2 % 4;
    r30 = r3 % 4;
    r40 = r4 % 4;
    r50 = r5 % 4;
    int a0, a0_0, b0, c0, c0_0, c1_0, d0, p0, q0, a1, a1_0, b1, c1, d1, p1, q1, axorb_0, cxord_0, axorb_1, cxord_1;
    int e0, e1, p0_0, p1_0, q0_0, q1_0;

    a0_0 = x0 & 0x2;
    a1_0 = x1 & 0x2;
    a0 = a0_0 >> 1;
    a1 = a1_0 >> 1;

    b0 = x0 & 0x1;
    b1 = x1 & 0x1;

    c0_0 = y0 & 0x2;
    c1_0 = y1 & 0x2;
    c0 = c0_0 >> 1;
    c1 = c1_0 >> 1;

    d0 = y0 & 0x1;
    d1 = y1 & 0x1;
    axorb_0 = a0 ^ b0;
    cxord_0 = c0 ^ d0;
    axorb_1 = a1 ^ b1;
    cxord_1 = c1 ^ d1;

    hpc1(axorb_0, axorb_1, cxord_0, cxord_1, &e0, &e1, r00, r10);

    hpc1(a0, a1, c0, c1, &p0_0, &p1_0, r20, r30);
    p0 = p0_0 ^ e0;
    p1 = p1_0 ^ e1;

    hpc1(b0, b1, d0, d1, &q0_0, &q1_0, r40, r50);
    q0 = q0_0 ^ e0;
    q1 = q1_0 ^ e1;
    int p0ls1, p1ls1;
    p1ls1 = p1 << 1;
    p0ls1 = p0 << 1;
    *e0_0 = (p1ls1 | q1);
    *e1_0 = (p0ls1 | q0);
}
// /* scale by N = Omega^2 in GF(2^2), using normal basis (Omega^2,Omega) */
void G4_scl_N(int x0, int x1, int *e0_1, int *e1_1)
{

    int a0, a1, b0, b1, p0, p1, q0, q1, a0_0, a1_0;

    a0_0 = x0 & 0x2;
    a1_0 = x1 & 0x2;
    a0 = a0_0 >> 1;
    a1 = a1_0 >> 1;

    b0 = x0 & 0x1;
    b1 = x1 & 0x1;
    p0 = b0;
    p1 = b1;
    q0 = a0 ^ b0;
    q1 = a1 ^ b1;
    int p0ls1, p1ls1;
    p1ls1 = p1 << 1;
    p0ls1 = p0 << 1;
    *e0_1 = (p0ls1 | q0);
    *e1_1 = (p1ls1 | q1);
}
// /* scale by N^2 = Omega in GF(2^2), using normal basis (Omega^2,Omega) */
int G4_scl_N2(int x0, int x1, int *e0_0, int *e1_0)
{
    int a0, a1, b0, b1, p1, p2, q1, q2, a0_0, a1_0, p0, q0;

    a0_0 = x0 & 0x2;
    a1_0 = x1 & 0x2;
    a0 = a0_0 >> 1;
    a1 = a1_0 >> 1;

    b0 = x0 & 0x1;
    b1 = x1 & 0x1;
    p0 = a0 ^ b0;
    p1 = a1 ^ b1;
    q0 = a0;
    q1 = a1;
    int p0ls1, p1ls1;
    p1ls1 = p1 << 1;
    p0ls1 = p0 << 1;
    *e0_0 = (p0ls1 | q0);
    *e1_0 = (p1ls1 | q1);
}

void G4_sq(int x0, int x1, int *e0_0, int *e1_0)
{
    int a0, a1, b0, b1, a0_0, a1_0;
    a0_0 = x0 & 0x2;
    a1_0 = x1 & 0x2;
    a0 = a0_0 >> 1;
    a1 = a1_0 >> 1;

    b0 = x0 & 0x1;
    b1 = x1 & 0x1;
    int b0ls1, b1ls1;
    b0ls1 = (b0 << 1);
    b1ls1 = (b1 << 1);
    *e0_0 = (b0ls1 | a0);
    *e1_0 = (b1ls1 | a1);
}

void G16_mul(int x0, int x1, int y0, int y1, int *o0, int *o1, int r0, int r1, int r2, int r3, int r4, int r5,
             int r6, int r7, int r8, int r9, int r10, int r11, int r12, int r13, int r14, int r15, int r16, int r17)
{
    int r00, v_r1, r20, r30, r40, r50, r60, r70, r80;
    int r90, r100, r110, r120, r130, r140, r150, r160, r170;
    r00 = r0 % 16;
    v_r1 = r1 % 16;
    r20 = r2 % 16;
    r30 = r3 % 16;
    r40 = r4 % 16;
    r50 = r5 % 16;
    r60 = r6 % 16;
    r70 = r7 % 16;
    r80 = r8 % 16;
    r90 = r9 % 16;
    r100 = r10 % 16;
    r110 = r11 % 16;
    r120 = r12 % 16;
    r130 = r13 % 16;
    r140 = r14 % 16;
    r150 = r15 % 16;
    r160 = r16 % 16;
    r170 = r17 % 16;

    int a0, a1, b0, b1, c0, c1, d0, d1, p0, p1, q0, q1, axorb_0, cxord_0, axorb_1, cxord_1, a0_0, a1_0, c0_0, c1_0;
    int e0, e1, p0_0, p1_0, q0_0, q1_0;
    a0_0 = x0 & 0xC;
    a1_0 = x1 & 0xC;
    a0 = a0_0 >> 2;
    a1 = a1_0 >> 2;
    b0 = x0 & 0x3;
    b1 = x1 & 0x3;
    c0_0 = y0 & 0xC;
    c1_0 = y1 & 0xC;
    c0 = c0_0 >> 2;
    c1 = c1_0 >> 2;
    d0 = y0 & 0x3;
    d1 = y1 & 0x3;
    axorb_0 = a0 ^ b0;
    cxord_0 = c0 ^ d0;
    axorb_1 = a1 ^ b1;
    cxord_1 = c1 ^ d1;
    G4_mul(axorb_0, axorb_1, cxord_0, cxord_1, &e0, &e1, r00, v_r1, r20, r30, r40, r50);
    int e01, e11;
    G4_scl_N(e0, e1, &e01, &e11);

    G4_mul(a0, a1, c0, c1, &p0_0, &p1_0, r60, r70, r80, r90, r100, r110);
    p0 = p0_0 ^ e01;
    p1 = p1_0 ^ e11;

    G4_mul(b0, b1, d0, d1, &q0_0, &q1_0, r120, r130, r140, r150, r160, r170);
    q0 = q0_0 ^ e01;
    q1 = q1_0 ^ e11;
    int p0ls2, p1ls2;
    p0ls2 = p0 << 2;
    p1ls2 = p1 << 2;
    *o0 = (p0ls2 | q0);
    *o1 = (p1ls2 | q1);
}

void G16_sq_scl(int x0, int x1, int *y0, int *y1)
{
    int a0, a1, b0, b1, p0_0, p1_0, a0_0, a1_0;
    int q0_0, q1_0, p0, p1, q0, q1;
    a0_0 = x0 & 0xC;
    a1_0 = x1 & 0xC;
    a0 = a0_0 >> 2;
    a1 = a1_0 >> 2;
    b0 = x0 & 0x3;
    b1 = x1 & 0x3;
    p0_0 = a0 ^ b0;
    p1_0 = a1 ^ b1;
    G4_sq(p0_0, p1_0, &p0, &p1);

    G4_sq(b0, b1, &q0_0, &q1_0);
    G4_scl_N2(q0_0, q1_0, &q0, &q1);

    int p0ls2, p1ls2;
    p0ls2 = p0 << 2;
    p1ls2 = p1 << 2;
    *y0 = (p0ls2 | q0);
    *y1 = (p1ls2 | q1);
}
void G16_inv(int x0, int x1, int *y0, int *y1, int r0, int r1, int r2, int r3, int r4, int r5,
             int r6, int r7, int r8, int r9, int r10, int r11, int r12, int r13, int r14, int r15, int r16, int r17)
{
    int r00, v_r1, r20, r30, r40, r50, r60, r70, r80;
    int r90, r100, r110, r120, r130, r140, r150, r160, r170;
    r00 = r0 % 16;
    v_r1 = r1 % 16;
    r20 = r2 % 16;
    r30 = r3 % 16;
    r40 = r4 % 16;
    r50 = r5 % 16;
    r60 = r6 % 16;
    r70 = r7 % 16;
    r80 = r8 % 16;
    r90 = r9 % 16;
    r100 = r10 % 16;
    r110 = r11 % 16;
    r120 = r12 % 16;
    r130 = r13 % 16;
    r140 = r14 % 16;
    r150 = r15 % 16;
    r160 = r16 % 16;
    r170 = r17 % 16;

    int a0, a1, a0_0, a1_0, b0, b1;
    int c0, c1, c0_0, c1_0, d0, d1, e0, e1, p0, p1, q0, q1;
    int a0xorb0, a1xorb1, c0xord0, c1xord1;
    a0_0 = x0 & 0xC;
    a1_0 = x1 & 0xC;

    a0 = a0_0 >> 2;
    a1 = a1_0 >> 2;
    b0 = x0 & 0x3;
    b1 = x1 & 0x3;
    a0xorb0 = a0 ^ b0;
    a1xorb1 = a1 ^ b1;

    G4_sq(a0xorb0, a1xorb1, &c0_0, &c1_0);

    G4_scl_N(c0_0, c1_0, &c0, &c1);
    G4_mul(a0, a1, b0, b1, &d0, &d1, r00, v_r1, r20, r30, r40, r50);
    c0xord0 = c0 ^ d0;
    c1xord1 = c1 ^ d1;

    G4_sq(c0xord0, c1xord1, &e0, &e1); // really inverse, but same as square
    G4_mul(e0, e1, b0, b1, &p0, &p1, r60, r70, r80, r90, r100, r110);
    G4_mul(e0, e1, a0, a1, &q0, &q1, r120, r130, r140, r150, r160, r170);
    int p0ls2, p1ls2;
    p0ls2 = (p0 << 2);
    p1ls2 = (p1 << 2);
    *y0 = (p0ls2 | q0);
    *y1 = (p1ls2 | q1);
}

int G256_inv(int x0, int x1, int *y0, int *y1, int r0, int r1, int r2, int r3,
             int r4, int r5, int r6, int r7, int r8, int r9, int r10, int r11, int r12, int r13,
             int r14, int r15, int r16, int r17, int r18, int r19, int r20, int r21, int r22,
             int r23, int r24, int r25, int r26, int r27, int r28, int r29, int r30, int r31,
             int r32, int r33, int r34, int r35, int r36, int r37, int r38, int r39, int r40,
             int r41, int r42, int r43, int r44, int r45, int r46, int r47, int r48, int r49,
             int r50, int r51, int r52, int r53, int r54, int r55, int r56, int r57, int r58,
             int r59, int r60, int r61, int r62, int r63, int r64, int r65, int r66, int r67,
             int r68, int r69, int r70, int r71)
{

    int a0, a1, a0_0, a1_0, b0, b1;
    int c0, c1, d0, d1, e0, e1, p0, p1, q0, q1;
    int a0xorb0, a1xorb1, c0xord0, c1xord1;
    a0_0 = x0 & 0xF0;
    a1_0 = x1 & 0xF0;
    a0 = a0_0 >> 4;
    a1 = a1_0 >> 4;
    b0 = x0 & 0x0F;
    b1 = x1 & 0x0F;
    a0xorb0 = a0 ^ b0;
    a1xorb1 = a1 ^ b1;
    G16_sq_scl(a0xorb0, a1xorb1, &c0, &c1);
    G16_mul(a0, a1, b0, b1, &d0, &d1, r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17);
    c0xord0 = c0 ^ d0;
    c1xord1 = c1 ^ d1;
    G16_inv(c0xord0, c1xord1, &e0, &e1, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35);
    G16_mul(e0, e1, b0, b1, &p0, &p1, r36, r37, r38, r39, r40, r41, r42, r43, r44, r45, r46, r47, r48, r49, r50, r51, r52, r53);

    G16_mul(e0, e1, a0, a1, &q0, &q1, r54, r55, r56, r57, r58, r59, r60, r61, r62, r63, r64, r65, r66, r67, r68, r69, r70, r71);

    int p0ls4, p1ls4;
    p0ls4 = (p0 << 4);
    p1ls4 = (p1 << 4);
    *y0 = (p0ls4 | q0);
    *y1 = (p1ls4 | q1);
}

int G256_newbasis(int in1, int in2, int b[], int *out1, int *out2)
{

    int y, cond, yxorb, negCond, tempy, tempyIntoNegCond;
    int y1, y2, y3, y4, y5, y6, y7, y8;
    int cond1, cond2, cond3, cond4, cond5, cond6, cond7, cond8;
    int yxorb1, yxorb2, yxorb3, yxorb4, yxorb5, yxorb6, yxorb7, yxorb8;
    int negCond1, negCond2, negCond3, negCond4, negCond5, negCond6, negCond7, negCond8;
    int tempy1, tempy2, tempy3, tempy4, tempy5, tempy6, tempy7, tempy8;
    int ny1, ny2, ny3, ny4, ny5, ny6, ny7, ny8;
    int tempyIntoNegCond1, tempyIntoNegCond2, tempyIntoNegCond3, tempyIntoNegCond4, tempyIntoNegCond5, tempyIntoNegCond6;
    int tempyIntoNegCond7, tempyIntoNegCond8;
    int x1, x2, x3, x4, x5, x6, x7, x8;

    int z_y, z_cond, z_yxorb, z_negCond, z_tempy, z_tempyIntoNegCond;
    int z_y1, z_y2, z_y3, z_y4, z_y5, z_y6, z_y7, z_y8;
    int z_cond1, z_cond2, z_cond3, z_cond4, z_cond5, z_cond6, z_cond7, z_cond8;
    int z_yxorb1, z_yxorb2, z_yxorb3, z_yxorb4, z_yxorb5, z_yxorb6, z_yxorb7, z_yxorb8;
    int z_negCond1, z_negCond2, z_negCond3, z_negCond4, z_negCond5, z_negCond6, z_negCond7, z_negCond8;
    int z_tempy1, z_tempy2, z_tempy3, z_tempy4, z_tempy5, z_tempy6, z_tempy7, z_tempy8;
    int z_ny1, z_ny2, z_ny3, z_ny4, z_ny5, z_ny6, z_ny7, z_ny8;
    int z_tempyIntoNegCond1, z_tempyIntoNegCond2, z_tempyIntoNegCond3, z_tempyIntoNegCond4, z_tempyIntoNegCond5, z_tempyIntoNegCond6;
    int z_tempyIntoNegCond7, z_tempyIntoNegCond8;
    int z_x1, z_x2, z_x3, z_x4, z_x5, z_x6, z_x7, z_x8;

    y = 0;

    tempy1 = y;
    cond1 = in1 & 1;
    negCond1 = !cond1;
    yxorb1 = y ^ b[7];
    ny1 = cond1 * yxorb1;
    tempyIntoNegCond1 = tempy1 * negCond1;
    y1 = ny1 + tempyIntoNegCond1;
    x1 = in1 >> 1;

    tempy2 = y1;
    cond2 = x1 & 1;
    negCond2 = !cond2;
    yxorb2 = y1 ^ b[6];
    ny2 = cond2 * yxorb2;
    tempyIntoNegCond2 = tempy2 * negCond2;
    y2 = ny2 + tempyIntoNegCond2;
    x2 = x1 >> 1;

    tempy3 = y2;
    cond3 = x2 & 1;
    negCond3 = !cond3;
    yxorb3 = y2 ^ b[5];
    ny3 = cond3 * yxorb3;
    tempyIntoNegCond3 = tempy3 * negCond3;
    y3 = ny3 + tempyIntoNegCond3;
    x3 = x2 >> 1;

    tempy4 = y3;
    cond4 = x3 & 1;
    negCond4 = !cond4;
    yxorb4 = y3 ^ b[4];
    ny4 = cond4 * yxorb4;
    tempyIntoNegCond4 = tempy4 * negCond4;
    y4 = ny4 + tempyIntoNegCond4;
    x4 = x3 >> 1;

    tempy5 = y4;
    cond5 = x4 & 1;
    negCond5 = !cond5;
    yxorb5 = y4 ^ b[3];
    ny5 = cond5 * yxorb5;
    tempyIntoNegCond5 = tempy5 * negCond5;
    y5 = ny5 + tempyIntoNegCond5;
    x5 = x4 >> 1;

    tempy6 = y5;
    cond6 = x5 & 1;
    negCond6 = !cond6;
    yxorb6 = y5 ^ b[2];
    ny6 = cond6 * yxorb6;
    tempyIntoNegCond6 = tempy6 * negCond6;
    y6 = ny6 + tempyIntoNegCond6;
    x6 = x5 >> 1;

    tempy7 = y6;
    cond7 = x6 & 1;
    negCond7 = !cond7;
    yxorb7 = y6 ^ b[1];
    ny7 = cond7 * yxorb7;
    tempyIntoNegCond7 = tempy7 * negCond7;
    y7 = ny7 + tempyIntoNegCond7;
    x7 = x6 >> 1;

    tempy8 = y7;
    cond8 = x7 & 1;
    negCond8 = !cond8;
    yxorb8 = y7 ^ b[0];
    ny8 = cond8 * yxorb8;
    tempyIntoNegCond8 = tempy8 * negCond8;
    y8 = ny8 + tempyIntoNegCond8;
    x8 = x7 >> 1;

    *out1 = y8;

    z_y = 0;
    z_tempy1 = z_y;
    z_cond1 = in2 & 1;
    z_negCond1 = !z_cond1;
    z_yxorb1 = z_y ^ b[7];
    z_ny1 = z_cond1 * z_yxorb1;
    z_tempyIntoNegCond1 = z_tempy1 * z_negCond1;
    z_y1 = z_ny1 + z_tempyIntoNegCond1;
    z_x1 = in2 >> 1;

    z_tempy2 = z_y1;
    z_cond2 = z_x1 & 1;
    z_negCond2 = !z_cond2;
    z_yxorb2 = z_y1 ^ b[6];
    z_ny2 = z_cond2 * z_yxorb2;
    z_tempyIntoNegCond2 = z_tempy2 * z_negCond2;
    z_y2 = z_ny2 + z_tempyIntoNegCond2;
    z_x2 = z_x1 >> 1;

    z_tempy3 = z_y2;
    z_cond3 = z_x2 & 1;
    z_negCond3 = !z_cond3;
    z_yxorb3 = z_y2 ^ b[5];
    z_ny3 = z_cond3 * z_yxorb3;
    z_tempyIntoNegCond3 = z_tempy3 * z_negCond3;
    z_y3 = z_ny3 + z_tempyIntoNegCond3;
    z_x3 = z_x2 >> 1;

    z_tempy4 = z_y3;
    z_cond4 = z_x3 & 1;
    z_negCond4 = !z_cond4;
    z_yxorb4 = z_y3 ^ b[4];
    z_ny4 = z_cond4 * z_yxorb4;
    z_tempyIntoNegCond4 = z_tempy4 * z_negCond4;
    z_y4 = z_ny4 + z_tempyIntoNegCond4;
    z_x4 = z_x3 >> 1;

    z_tempy5 = z_y4;
    z_cond5 = z_x4 & 1;
    z_negCond5 = !z_cond5;
    z_yxorb5 = z_y4 ^ b[3];
    z_ny5 = z_cond5 * z_yxorb5;
    z_tempyIntoNegCond5 = z_tempy5 * z_negCond5;
    z_y5 = z_ny5 + z_tempyIntoNegCond5;
    z_x5 = z_x4 >> 1;

    z_tempy6 = z_y5;
    z_cond6 = z_x5 & 1;
    z_negCond6 = !z_cond6;
    z_yxorb6 = z_y5 ^ b[2];
    z_ny6 = z_cond6 * z_yxorb6;
    z_tempyIntoNegCond6 = z_tempy6 * z_negCond6;
    z_y6 = z_ny6 + z_tempyIntoNegCond6;
    z_x6 = z_x5 >> 1;

    z_tempy7 = z_y6;
    z_cond7 = z_x6 & 1;
    z_negCond7 = !z_cond7;
    z_yxorb7 = z_y6 ^ b[1];
    z_ny7 = z_cond7 * z_yxorb7;
    z_tempyIntoNegCond7 = z_tempy7 * z_negCond7;
    z_y7 = z_ny7 + z_tempyIntoNegCond7;
    z_x7 = z_x6 >> 1;

    z_tempy8 = z_y7;
    z_cond8 = z_x7 & 1;
    z_negCond8 = !z_cond8;
    z_yxorb8 = z_y7 ^ b[0];
    z_ny8 = z_cond8 * z_yxorb8;
    z_tempyIntoNegCond8 = z_tempy8 * z_negCond8;
    z_y8 = z_ny8 + z_tempyIntoNegCond8;
    z_x8 = z_x7 >> 1;
    *out2 = z_y8;
}
/* find Sbox of n in GF(2^8) mod POLY */
int sbox(int t0, int t1, int *y0, int *y1, int r0, int r1, int r2, int r3, int r4, int r5, int r6, int r7, int r8,
         int r9, int r10, int r11, int r12, int r13, int r14, int r15, int r16, int r17,
         int r18, int r19, int r20, int r21, int r22, int r23, int r24, int r25, int r26,
         int r27, int r28, int r29, int r30, int r31, int r32, int r33, int r34, int r35,
         int r36, int r37, int r38, int r39, int r40, int r41, int r42, int r43, int r44,
         int r45, int r46, int r47, int r48, int r49, int r50, int r51, int r52, int r53,
         int r54, int r55, int r56, int r57, int r58, int r59, int r60, int r61, int r62,
         int r63, int r64, int r65, int r66, int r67, int r68, int r69, int r70, int r71)
{
    int t2, t3, t4, t5, t6, t7;
    G256_newbasis(t0, t1, A2X, &t2, &t3);
    G256_inv(t2, t3, &t4, &t5, r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17,
             r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35, r36, r37, r38, r39,
             r40, r41, r42, r43, r44, r45, r46, r47, r48, r49, r50, r51, r52, r53, r54, r55, r56, r57, r58, r59, r60,
             r61, r62, r63, r64, r65, r66, r67, r68, r69, r70, r71);
    G256_newbasis(t4, t5, X2S, &t6, &t7);
    *y0 = t6 ^ 0x63;
    *y1 = t7;
}

// int main()
// {
//     srand(time(0));
//     int n1;
//     int n2 = 0;
//     int y0, y1;
//     for (int n1 = 1; n1 <= 255; n1++)
//     {
//         Sbox(n1, n2, &y0, &y1, 59, 190, 236, 19, 142, 253, 21, 89, 223, 88, 212, 233, 132, 12, 174,
//              33, 126, 38, 86, 238, 33, 207, 241, 197, 195, 198, 244, 2, 230, 121, 11, 18, 19, 22, 17, 6, 59, 190, 236, 19, 142, 253, 21, 89, 223, 88, 212, 233, 132, 12, 174,
//              33, 126, 38, 86, 238, 33, 207, 241, 197, 195, 198, 244, 2, 230, 121, 11, 18, 19, 22, 17, 6);
//         printf("AES Output for input %d is: %d\n", n1 ^ n2, y0 ^ y1);
//     }
// }