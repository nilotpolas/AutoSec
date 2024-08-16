/* sbox.c
 *
 * by: David Canright
 *
 * illustrates compact implementation of AES S-box via subfield operations
 *   case # 4 : [d^16, d], [alpha^8, alpha^2], [Omega^2, Omega]
 *   nu = beta^8 = N^2*alpha^2, N = w^2
 */

#include <stdio.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/* to convert between polynomial (A^7...1) basis A & normal basis X */
/* or to basis S which incorporates bit matrix of Sbox */
static int A2X[8] = {0x98, 0xF3, 0xF2, 0x48, 0x09, 0x81, 0xA9, 0xFF},
           X2A[8] = {0x64, 0x78, 0x6E, 0x8C, 0x68, 0x29, 0xDE, 0x60},
           X2S[8] = {0x58, 0x2D, 0x9E, 0x0B, 0xDC, 0x04, 0x03, 0x24},
           S2X[8] = {0x8C, 0x79, 0x05, 0xEB, 0x12, 0x04, 0x51, 0x53};

int reg(int a)
{
    return a;
}

void comar(int a0, int b0, int a1, int b1, int *y0, int *y1, int r0, int r1, int r0_1, int r1_1, int r2_1, int r3_1)
{
    int r00, r10, r0_10, r1_10, r2_10, r3_10;
    r00 = r0 % 2;
    r10 = r1 % 2;
    r0_10 = r0_1 % 2;
    r1_10 = r1_1 % 2;
    r2_10 = r2_1 % 2;
    r3_10 = r3_1 % 2;
    int i1, i2, p4, p2, p3, p1, i1xori2, i0xori3, m0, m1, m2, m3, i0, i3;
    int y1_1, y1_2, y1_3, y1_4;
    m0 = a0 ^ r00;
    m1 = b1 ^ r10;
    m2 = b0 ^ r10;
    m3 = a1 ^ r00;
    p2 = reg(m0) & reg(m1);
    p3 = reg(m3) & reg(m2);
    p1 = reg(m0) & reg(m2);
    p4 = reg(m3) & reg(m1);
    i0 = p1 ^ r0_10;
    i1 = p2 ^ r1_10;
    i2 = p3 ^ r2_10;
    i3 = p4 ^ r3_10;
    i1xori2 = reg(i1) ^ reg(i2);
    i0xori3 = reg(i0) ^ reg(i3);
    *y0 = reg(i1xori2 ^ i0xori3);
    y1_1 = r00 ^ r10;
    y1_2 = y1_1 ^ r0_10;
    y1_3 = y1_2 ^ r1_10;
    y1_4 = y1_3 ^ r2_10;
    *y1 = y1_4 ^ r3_10;
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

    comar(axorb_0, cxord_0, axorb_1, cxord_1, &e0, &e1, r00, r10, r20, r30, r40, r50);

    comar(a0, c0, a1, c1, &p0_0, &p1_0, r00, r10, r20, r30, r40, r50);
    p0 = p0_0 ^ e0;
    p1 = p1_0 ^ e1;

    comar(b0, d0, b1, d1, &q0_0, &q1_0, r00, r10, r20, r30, r40, r50);
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

void G16_mul(int x0, int x1, int y0, int y1, int *o0, int *o1, int r0, int r1, int r2, int r3, int r4, int r5)
{
    int r00, r10, r20, r30, r40, r50;
    r00 = r0 % 16;
    r10 = r1 % 16;
    r20 = r2 % 16;
    r30 = r3 % 16;
    r40 = r4 % 16;
    r50 = r5 % 16;

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
    G4_mul(axorb_0, axorb_1, cxord_0, cxord_1, &e0, &e1, r00, r10, r20, r30, r40, r50);
    int e01, e11;
    G4_scl_N(e0, e1, &e01, &e11);

    G4_mul(a0, a1, c0, c1, &p0_0, &p1_0, r00, r10, r20, r30, r40, r50);
    p0 = p0_0 ^ e01;
    p1 = p1_0 ^ e11;

    G4_mul(b0, b1, d0, d1, &q0_0, &q1_0, r00, r10, r20, r30, r40, r50);
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
void G16_inv(int x0, int x1, int *y0, int *y1, int r0, int r1, int r2, int r3, int r4, int r5)
{
    int r00, r10, r20, r30, r40, r50;
    r00 = r0 % 16;
    r10 = r1 % 16;
    r20 = r2 % 16;
    r30 = r3 % 16;
    r40 = r4 % 16;
    r50 = r5 % 16;

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
    G4_mul(a0, a1, b0, b1, &d0, &d1, r00, r10, r20, r30, r40, r50);
    c0xord0 = c0 ^ d0;
    c1xord1 = c1 ^ d1;

    G4_sq(c0xord0, c1xord1, &e0, &e1); // really inverse, but same as square
    G4_mul(e0, e1, b0, b1, &p0, &p1, r00, r10, r20, r30, r40, r50);
    G4_mul(e0, e1, a0, a1, &q0, &q1, r00, r10, r20, r30, r40, r50);
    int p0ls2, p1ls2;
    p0ls2 = (p0 << 2);
    p1ls2 = (p1 << 2);
    *y0 = (p0ls2 | q0);
    *y1 = (p1ls2 | q1);
}

int G256_inv(int x0, int x1, int *y0, int *y1, int r0, int r1, int r2, int r3, int r4, int r5)
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
    G16_mul(a0, a1, b0, b1, &d0, &d1, r0, r1, r2, r3, r4, r5);
    c0xord0 = c0 ^ d0;
    c1xord1 = c1 ^ d1;
    G16_inv(c0xord0, c1xord1, &e0, &e1, r0, r1, r2, r3, r4, r5);
    G16_mul(e0, e1, b0, b1, &p0, &p1, r0, r1, r2, r3, r4, r5);

    G16_mul(e0, e1, a0, a1, &q0, &q1, r0, r1, r2, r3, r4, r5);

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
int sbox(int t0, int t1, int *y0, int *y1, int r0, int r1, int r2, int r3, int r4, int r5)
{
    int t2, t3, t4, t5, t6, t7;
    G256_newbasis(t0, t1, A2X, &t2, &t3);
    G256_inv(t2, t3, &t4, &t5, r0, r1, r2, r3, r4, r5);
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
//         sbox(n1, n2, &y0, &y1, 59, 190, 236, 19, 142, 253);
//         printf("AES Output for input %d is: %d\n", n1 ^ n2, y0 ^ y1);
//     }
// }