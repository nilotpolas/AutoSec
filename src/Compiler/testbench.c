#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#include "sbox.c"
#define TEST_CASES 10

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

/* to convert between polynomial (A^7...1) basis A & normal basis X */
/* or to basis S which incorporates bit matrix of Sbox */

/* to convert between polynomial (A^7...1) basis A & normal basis X */
/* or to basis S which incorporates bit matrix of Sbox */
static int A2X[8] = {0x98, 0xF3, 0xF2, 0x48, 0x09, 0x81, 0xA9, 0xFF},
           X2A[8] = {0x64, 0x78, 0x6E, 0x8C, 0x68, 0x29, 0xDE, 0x60},
           X2S[8] = {0x58, 0x2D, 0x9E, 0x0B, 0xDC, 0x04, 0x03, 0x24},
           S2X[8] = {0x8C, 0x79, 0x05, 0xEB, 0x12, 0x04, 0x51, 0x53};

/* multiply in GF(2^2), using normal basis (Omega^2,Omega) */
void G4_mul(int x, int y, int *out)
{
    int a, b, c, d, e, p, q;
    int xand2, yand2, axorb, cxord, aAndc, bAndd, pls1;
    xand2 = (x & 0x2);
    yand2 = (y & 0x2);
    a = xand2 >> 1;
    b = (x & 0x1);
    c = yand2 >> 1;
    d = (y & 0x1);
    axorb = a ^ b;
    cxord = c ^ d;
    e = axorb & cxord;
    aAndc = a & c;
    bAndd = b & d;
    p = aAndc ^ e;
    q = bAndd ^ e;
    pls1 = p << 1;
    *out = (pls1 | q);
}

/* scale by N = Omega^2 in GF(2^2), using normal basis (Omega^2,Omega) */
void G4_scl_N(int x, int *out)
{
    int a, b, p, q;
    int xAnd2, pls1;
    xAnd2 = x & 0x2;
    a = xAnd2 >> 1;
    b = (x & 0x1);
    p = b;
    q = a ^ b;
    pls1 = p << 1;
    *out = (pls1 | q);
}

/* scale by N^2 = Omega in GF(2^2), using normal basis (Omega^2,Omega) */
void G4_scl_N2(int x, int *out)
{
    int a, b, p, q;
    int pls1, xAnd2;
    xAnd2 = x & 0x2;
    a = xAnd2 >> 1;
    b = (x & 0x1);
    p = a ^ b;
    q = a;
    pls1 = p << 1;
    *out = (pls1 | q);
}

/* square in GF(2^2), using normal basis (Omega^2,Omega) */
/* NOTE: inverse is identical */
void G4_sq(int x, int *out)
{
    int a, b;
    int bls1, xAnd2;
    xAnd2 = x & 0x2;
    a = xAnd2 >> 1;
    b = (x & 0x1);
    bls1 = b << 1;
    *out = (bls1 | a);
}

/* multiply in GF(2^4), using normal basis (alpha^8,alpha^2) */
void G16_mul(int x, int y, int *out)
{
    int a, b, c, d, e, p, q;
    int pls2, xAndC, yAndC, axorb, cxord, g4_mul_ac, g4_mul_bd;
    xAndC = (x & 0xC);
    yAndC = (y & 0xC);
    a = xAndC >> 2;
    b = (x & 0x3);
    c = yAndC >> 2;
    d = (y & 0x3);
    axorb = a ^ b;
    cxord = c ^ d;
    G4_mul(axorb, cxord, &e);
    G4_scl_N(e, &e);
    G4_mul(a, c, &g4_mul_ac);
    G4_mul(b, d, &g4_mul_bd);
    p = g4_mul_ac ^ e;
    q = g4_mul_bd ^ e;
    pls2 = (p << 2);
    *out = (pls2 | q);
}

/* square & scale by nu in GF(2^4)/GF(2^2), normal basis (alpha^8,alpha^2) */
/*   nu = beta^8 = N^2*alpha^2, N = w^2 */
void G16_sq_scl(int x, int *out)
{
    int a, b, p, q;
    int pls2, xAndC, g4_sq_b, axorb;
    xAndC = (x & 0xC);
    a = xAndC >> 2;
    b = (x & 0x3);
    axorb = a ^ b;
    G4_sq(axorb, &p);
    G4_sq(b, &g4_sq_b);
    G4_scl_N2(g4_sq_b, &q);
    pls2 = p << 2;
    *out = (pls2 | q);
}

/* inverse in GF(2^4), using normal basis (alpha^8,alpha^2) */
void G16_inv(int x, int *out)
{
    int a, b, c, d, e, p, q;
    int xAndC, axorb, g4_sq_axorb, cxord, pls2;
    xAndC = (x & 0xC);
    a = xAndC >> 2;
    b = (x & 0x3);
    axorb = a ^ b;
    G4_sq(axorb, &g4_sq_axorb);
    G4_scl_N(g4_sq_axorb, &c);
    G4_mul(a, b, &d);
    cxord = c ^ d;
    G4_sq(cxord, &e); // really inverse, but same as square
    G4_mul(e, b, &p);
    G4_mul(e, a, &q);
    pls2 = p << 2;
    *out = (pls2 | q);
}

/* inverse in GF(2^8), using normal basis (d^16,d) */
void G256_inv(int x, int *out)
{
    int a, b, c, d, e, p, q;
    int xAndF0, aOrb, cOrd, pls4;
    xAndF0 = (x & 0xF0);
    a = xAndF0 >> 4;
    b = (x & 0x0F);
    aOrb = a ^ b;
    G16_sq_scl(aOrb, &c);
    G16_mul(a, b, &d);
    cOrd = c ^ d;
    G16_inv(cOrd, &e);
    G16_mul(e, b, &p);
    G16_mul(e, a, &q);
    pls4 = p << 4;
    *out = (pls4 | q);
}

/* convert to new basis in GF(2^8) */
/* i.e., bit matrix multiply */
void G256_newbasis(int x, int b[], int *out)
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

    y = 0;

    tempy1 = y;
    cond1 = x & 1;
    negCond1 = !cond1;
    yxorb1 = y ^ b[7];
    ny1 = cond * yxorb1;
    tempyIntoNegCond = tempy1 * negCond;
    y1 = ny1 + tempyIntoNegCond;
    x = x >> 1;

    tempy2 = y1;
    cond2 = x & 1;
    negCond2 = !cond2;
    yxorb2 = y1 ^ b[6];
    ny2 = cond2 * yxorb2;
    tempyIntoNegCond2 = tempy2 * negCond2;
    y2 = ny2 + tempyIntoNegCond2;
    x = x >> 1;

    tempy3 = y2;
    cond3 = x & 1;
    negCond3 = !cond3;
    yxorb3 = y2 ^ b[5];
    ny3 = cond3 * yxorb3;
    tempyIntoNegCond3 = tempy3 * negCond3;
    y3 = ny3 + tempyIntoNegCond3;
    x = x >> 1;

    tempy4 = y3;
    cond4 = x & 1;
    negCond4 = !cond4;
    yxorb4 = y3 ^ b[4];
    ny4 = cond4 * yxorb4;
    tempyIntoNegCond4 = tempy4 * negCond4;
    y4 = ny4 + tempyIntoNegCond4;
    x = x >> 1;

    tempy5 = y4;
    cond5 = x & 1;
    negCond5 = !cond5;
    yxorb5 = y4 ^ b[3];
    ny5 = cond * yxorb;
    tempyIntoNegCond5 = tempy5 * negCond5;
    y5 = ny5 + tempyIntoNegCond5;
    x = x >> 1;

    tempy6 = y5;
    cond6 = x & 1;
    negCond6 = !cond6;
    yxorb6 = y5 ^ b[2];
    ny6 = cond6 * yxorb6;
    tempyIntoNegCond6 = tempy6 * negCond6;
    y6 = ny6 + tempyIntoNegCond6;
    x = x >> 1;

    tempy7 = y6;
    cond7 = x & 1;
    negCond7 = !cond7;
    yxorb7 = y6 ^ b[1];
    ny7 = cond7 * yxorb7;
    tempyIntoNegCond7 = tempy7 * negCond7;
    y7 = ny7 + tempyIntoNegCond7;
    x = x >> 1;

    tempy8 = y7;
    cond8 = x & 1;
    negCond8 = !cond8;
    yxorb8 = y7 ^ b[0];
    ny8 = cond8 * yxorb8;
    tempyIntoNegCond8 = tempy8 * negCond8;
    y8 = ny8 + tempyIntoNegCond8;
    x = x >> 1;

    // for (i = 7; i >= 0; i--)
    // {
    // 	tempy = y;
    // 	cond = x & 1;
    // 	negCond = !cond;
    // 	yxorb = y ^ b[i];
    // 	y = cond * yxorb;
    // 	tempyIntoNegCond = tempy * negCond;
    // 	y = y + tempyIntoNegCond;
    // 	x = x >> 1;
    // }
    *out = (y8);
}

/* find Sbox of n in GF(2^8) mod POLY */
void sbox(int n, int *out)
{
    int t, ret;

    G256_newbasis(n, A2X, &t);
    G256_inv(t, &t);
    G256_newbasis(t, X2S, &t);
    *out = (t ^ 0x63);
}

int main()
{

    int test_cases = 0;
    while (test_cases < TEST_CASES)
    {
        srand(test_cases);

        // Generate random inputs
        int x0_0 = rand() % 256;
        int x0_1 = rand() % 256;

        printf("Input: %d ", x0_0 ^ x0_1);

        printf("---");
        int Y;

        Y = Sbox(x0_0 ^ x0_1);

        printf("Output: %3d", Y);

        test_cases++;
        printf("\n");
    }
    return 0;
}
