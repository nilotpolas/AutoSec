// #include <stdio.h>
// #include <stdlib.h>
// #include <time.h>

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

// int reg(int a)
// {
//     return a;
// }

/* to convert between polynomial (A^7...1) basis A & normal basis X */
/* or to basis S which incorporates bit matrix of Sbox */
static int A2X[8] = {0x98, 0xF3, 0xF2, 0x48, 0x09, 0x81, 0xA9, 0xFF},
           X2A[8] = {0x64, 0x78, 0x6E, 0x8C, 0x68, 0x29, 0xDE, 0x60},
           X2S[8] = {0x58, 0x2D, 0x9E, 0x0B, 0xDC, 0x04, 0x03, 0x24},
           S2X[8] = {0x8C, 0x79, 0x05, 0xEB, 0x12, 0x04, 0x51, 0x53};
// ap_int<1> a0, ap_int<1> a1, ap_int<1> b0, ap_int<1> b1, ap_int<1> *y0, ap_int<1> *y1, ap_int<1> z

/* multiply in GF(2^2), using normal basis (Omega^2,Omega) 
ap_int<2> x0, ap_int<2> x1, ap_int<2> y0, ap_int<2> y1, ap_int<2> *e0_0, ap_int<2> *e1_0, ap_int<1> r0, ap_int<1> r1, ap_int<1> r2
*/
void G4_mul(int x0, int y0, int *e1_0)
{
   
    int a0, a0_0, b0, c0, c0_0, d0, p0, q0, axorb_0, cxord_0;
    int e0, p0_0, q0_0;

    a0_0 = x0 & 0x2;
    // a1_0 = x1 & 0x2;
    a0 = a0_0 >> 1;
    // a1 = a1_0 >> 1;

    b0 = x0 & 0x1;
    // b1 = x1 & 0x1;

    c0_0 = y0 & 0x2;
    // c1_0 = y1 & 0x2;
    c0 = c0_0 >> 1;
    // c1 = c1_0 >> 1;

    d0 = y0 & 0x1;
    // d1 = y1 & 0x1;
    axorb_0 = a0 ^ b0;
    cxord_0 = c0 ^ d0;
    // axorb_1 = a1 ^ b1;
    // cxord_1 = c1 ^ d1;

    e0 = (axorb_0 & cxord_0);

    p0_0 = (a0 & c0);
    p0 = p0_0 ^ e0;
    // p1 = p1_0 ^ e1;

    q0_0 = (b0 & d0);
    q0 = q0_0 ^ e0;
    // q1 = q1_0 ^ e1;
    int p0ls1;
    // p1ls1 = p1 << 1;
    p0ls1 = p0 << 1;
    // *e0_0 = (p1ls1 | q1);
    *e1_0 = (p0ls1 | q0);
}
/* scale by N = Omega^2 in GF(2^2), using normal basis (Omega^2,Omega) 
ap_int<2> x0, ap_int<2> x1, ap_int<2> *e0_1, ap_int<2> *e1_1
*/
void G4_scl_N(int x0, int *e0_1)
{

    int a0, b0, p0, q0, a0_0;

    a0_0 = x0 & 0x2;
    // a1_0 = x1 & 0x2;
    a0 = a0_0 >> 1;
    // a1 = a1_0 >> 1;

    b0 = x0 & 0x1;
    // b1 = x1 & 0x1;
    p0 = b0;
    // p1 = b1;
    q0 = a0 ^ b0;
    // q1 = a1 ^ b1;
    int p0ls1;
    // p1ls1 = p1 << 1;
    p0ls1 = p0 << 1;
    *e0_1 = (p0ls1 | q0);
    // *e1_1 = (p1ls1 | q1);
}
/* scale by N^2 = Omega in GF(2^2), using normal basis (Omega^2,Omega) 
ap_int<2> x0, ap_int<2> x1, ap_int<2> *e0_0, ap_int<2> *e1_0
*/
void G4_scl_N2(int x0, int *e0_0)
{
    int a0, a1, b0, b1, p1, p2, q1, q2, a0_0, a1_0, p0, q0;

    a0_0 = x0 & 0x2;
    // a1_0 = x1 & 0x2;
    a0 = a0_0 >> 1;
    // a1 = a1_0 >> 1;

    b0 = x0 & 0x1;
    // b1 = x1 & 0x1;
    p0 = a0 ^ b0;
    // p1 = a1 ^ b1;
    q0 = a0;
    // q1 = a1;
    int p0ls1;
    // p1ls1 = p1 << 1;
    p0ls1 = p0 << 1;
    *e0_0 = (p0ls1 | q0);
    // *e1_0 = (p1ls1 | q1);
}
// ap_int<2> x0, ap_int<2> x1, ap_int<2> *e0_0, ap_int<2> *e1_0
void G4_sq(int x0, int *e0_0)
{
    int a0, a1, b0, b1, a0_0, a1_0;
    a0_0 = x0 & 0x2;
    // a1_0 = x1 & 0x2;
    a0 = a0_0 >> 1;
    // a1 = a1_0 >> 1;

    b0 = x0 & 0x1;
    // b1 = x1 & 0x1;
    int b0ls1;
    b0ls1 = (b0 << 1);
    // b1ls1 = (b1 << 1);
    *e0_0 = (b0ls1 | a0);
    // *e1_0 = (b1ls1 | a1);
}
// ap_int<4> x0, ap_int<4> x1, ap_int<1> y0, ap_int<4> y1, ap_int<4> *o0, ap_int<4> *o1, ap_int<1> r0, ap_int<1> r1, ap_int<1> r2, ap_int<1> r3, ap_int<1> r4, ap_int<1> r5, ap_int<1> r6, ap_int<1> r7, ap_int<1> r8
void G16_mul(int x0, int y0, int *o0)
{
    int a0, b0, c0, d0, p0, q0, axorb_0, cxord_0, a0_0, c0_0;
    int e0, p0_0, q0_0;
    a0_0 = x0 & 0xC;
    // a1_0 = x1 & 0xC;
    a0 = a0_0 >> 2;
    // a1 = a1_0 >> 2;
    b0 = x0 & 0x3;
    // b1 = x1 & 0x3;
    c0_0 = y0 & 0xC;
    // c1_0 = y1 & 0xC;
    c0 = c0_0 >> 2;
    // c1 = c1_0 >> 2;
    d0 = y0 & 0x3;
    // d1 = y1 & 0x3;
    axorb_0 = a0 ^ b0;
    cxord_0 = c0 ^ d0;
    // axorb_1 = a1 ^ b1;
    // cxord_1 = c1 ^ d1;
    G4_mul(axorb_0, cxord_0, &e0);
    int e01, e11;
    G4_scl_N(e0, &e01);

    G4_mul(a0, c0, &p0_0);
    p0 = p0_0 ^ e01;
    // p1 = p1_0 ^ e11;

    G4_mul(b0, d0, &q0_0);
    q0 = q0_0 ^ e01;
    // q1 = q1_0 ^ e11;
    int p0ls2;
    p0ls2 = p0 << 2;
    // p1ls2 = p1 << 2;
    *o0 = (p0ls2 | q0);
    // *o1 = (p1ls2 | q1);
}
// ap_int<4> x0, ap_int<4> x1, ap_int<4> *y0, ap_int<4> *y1
void G16_sq_scl(int x0, int *y0)
{
    int a0, b0, p0_0, a0_0;
    int q0_0, p0, q0;
    a0_0 = x0 & 0xC;
    // a1_0 = x1 & 0xC;
    a0 = a0_0 >> 2;
    // a1 = a1_0 >> 2;
    b0 = x0 & 0x3;
    // b1 = x1 & 0x3;
    p0_0 = a0 ^ b0;
    // p1_0 = a1 ^ b1;
    G4_sq(p0_0, &p0);

    G4_sq(b0, &q0_0);
    G4_scl_N2(q0_0, &q0);

    int p0ls2;
    p0ls2 = p0 << 2;
    // p1ls2 = p1 << 2;
    *y0 = (p0ls2 | q0);
    // *y1 = (p1ls2 | q1);
}
// ap_int<4> x0, ap_int<4> x1, ap_int<4> *y0, ap_int<4> *y1, ap_int<1> r0, ap_int<1> r1, ap_int<1> r2, ap_int<1> r3, ap_int<1> r4, ap_int<1> r5, ap_int<1> r6, ap_int<1> r7, ap_int<1> r8
void G16_inv(int x0, int *y0)
{

    int a0, a0_0, b0;
    int c0, c0_0, d0, e0, p0, q0;
    int a0xorb0, c0xord0;
    a0_0 = x0 & 0xC;
    // a1_0 = x1 & 0xC;

    a0 = a0_0 >> 2;
    // a1 = a1_0 >> 2;
    b0 = x0 & 0x3;
    // b1 = x1 & 0x3;
    a0xorb0 = a0 ^ b0;
    // a1xorb1 = a1 ^ b1;

    G4_sq(a0xorb0, &c0_0);

    G4_scl_N(c0_0, &c0);
    G4_mul(a0, b0, &d0);
    c0xord0 = c0 ^ d0;
    // c1xord1 = c1 ^ d1;

    G4_sq(c0xord0, &e0); // really inverse, but same as square
    G4_mul(e0, b0, &p0);
    G4_mul(e0, a0, &q0);
    int p0ls2;
    p0ls2 = (p0 << 2);
    // p1ls2 = (p1 << 2);
    *y0 = (p0ls2 | q0);
    // *y1 = (p1ls2 | q1);
}
/* inverse in GF(2^8)/GF(2^4), using normal basis [d^16, d] 
    G256_inv(ap_int<8> x0, ap_int<8> x1, ap_int<8> *y0, ap_int<8> *y1, ap_int<1> r0, ap_int<1> r1, ap_int<1> r2,
    ap_int<1> r3, ap_int<1> r4, ap_int<1> r5, ap_int<1> r6, ap_int<1> r7, ap_int<1> r8, ap_int<1> r9, 
    ap_int<1> r10, ap_int<1> r11, ap_int<1> r12, ap_int<1> r13, ap_int<1> r14, ap_int<1> r15, ap_int<1> r16,
    ap_int<1> r17, ap_int<1> r18, ap_int<1> r19, ap_int<1> r20, ap_int<1> r21, ap_int<1> r22, ap_int<1> r23,
    ap_int<1> r24, ap_int<1> r25, ap_int<1> r26, ap_int<1> r27, ap_int<1> r28, ap_int<1> r29, ap_int<1> r30,
    ap_int<1> r31, ap_int<1> r32, ap_int<1> r33, ap_int<1> r34, ap_int<1> r35) */

void G256_inv(int x0, int *y0)
{

    int a0, a1, a0_0, a1_0, b0, b1;
    int c0, d0, e0, p0, q0;
    int a0xorb0, c0xord0;
    a0_0 = x0 & 0xF0;
    // a1_0 = x1 & 0xF0;
    a0 = a0_0 >> 4;
    // a1 = a1_0 >> 4;
    b0 = x0 & 0x0F;
    // b1 = x1 & 0x0F;
    a0xorb0 = a0 ^ b0;
    // a1xorb1 = a1 ^ b1;
    G16_sq_scl(a0xorb0, &c0);
    G16_mul(a0, b0, &d0);
    c0xord0 = c0 ^ d0;
    // c1xord1 = c1 ^ d1;
    G16_inv(c0xord0, &e0);
    G16_mul(e0, b0, &p0);

    G16_mul(e0, a0, &q0);

    int p0ls4, p1ls4;
    p0ls4 = (p0 << 4);
    // p1ls4 = (p1 << 4);
    *y0 = (p0ls4 | q0);
    // *y1 = (p1ls4 | q1);
}
//ap_int<8> G256_newbasis(ap_int<8> in1, ap_int<8> in2, ap_int<8> b[], ap_int<8> *out1, ap_int<8> *out2)
void G256_newbasis(int in1, int b[], int *out1)
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
}
/* find Sbox of n in GF(2^8) mod POLY 
    ap_int<8> t0, ap_int<8> t1, ap_int<8> *y0, ap_int<8> *y1, ap_int<1> r0, ap_int<1> r1, ap_int<1> r2, ap_int<1> r3, ap_int<1> r4, ap_int<1> r5, ap_int<1> r6, ap_int<1> r7,
    ap_int<1> r8, ap_int<1> r9, ap_int<1> r10, ap_int<1> r11, ap_int<1> r12, ap_int<1> r13, ap_int<1> r14, ap_int<1> r15, ap_int<1> r16, ap_int<1> r17,ap_int<1> r18, 
    ap_int<1> r19, ap_int<1> r20, ap_int<1> r21, ap_int<1> r22, ap_int<1> r23, ap_int<1> r24, ap_int<1> r25, ap_int<1> r26,ap_int<1> r27, ap_int<1> r28, ap_int<1> r29,
    ap_int<1> r30, ap_int<1> r31, ap_int<1> r32, ap_int<1> r33, ap_int<1> r34, ap_int<1> r35
*/
int Sbox(int t)
{
    int t2, t4, t6;
    G256_newbasis(t, A2X, &t2);
    G256_inv(t2, &t4);
    G256_newbasis(t4, X2S, &t6);
    return (t6 ^ 0x63);
    
}

// int main()
// {
//     srand(time(0));
//     int n1;
//     int n2 = 0;
//     int y0, y1;
//     for (int n1 = 1; n1 <= 255; n1++)
//     {
//         sbox(n1, n2, &y0, &y1, 59, 190, 236, 19, 142, 253, 21, 89, 223, 88, 212, 233, 132, 12, 174,
//              33, 126, 38, 86, 238, 33, 207, 241, 197, 195, 198, 244, 2, 230, 121, 11, 18, 19, 22, 17, 6);
//         printf("AES Output for input %d is: %d\n", n1 ^ n2, y0 ^ y1);
//     }
// }

