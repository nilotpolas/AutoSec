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
static int A2X[8] = {0x98, 0xF3, 0xF2, 0x48, 0x09, 0x81, 0xA9, 0xFF},
           X2A[8] = {0x64, 0x78, 0x6E, 0x8C, 0x68, 0x29, 0xDE, 0x60},
           X2S[8] = {0x58, 0x2D, 0x9E, 0x0B, 0xDC, 0x04, 0x03, 0x24},
           S2X[8] = {0x8C, 0x79, 0x05, 0xEB, 0x12, 0x04, 0x51, 0x53};

/* multiply in GF(2^2), using normal basis (Omega^2,Omega) */
void G4_mul(int x, int y, int *out) {
  int a, b, c, d, e, p, q;

  a = (x & 0x2) >> 1;
  b = (x & 0x1);
  c = (y & 0x2) >> 1;
  d = (y & 0x1);
  e = (a ^ b) & (c ^ d);
  p = (a & c) ^ e;
  q = (b & d) ^ e;
  *out = ((p << 1) | q);
}

/* scale by N = Omega^2 in GF(2^2), using normal basis (Omega^2,Omega) */
void G4_scl_N(int x, int *out) {
  int a, b, p, q;

  a = (x & 0x2) >> 1;
  b = (x & 0x1);
  p = b;
  q = a ^ b;
  *out = ((p << 1) | q);
}

/* scale by N^2 = Omega in GF(2^2), using normal basis (Omega^2,Omega) */
void G4_scl_N2(int x, int *out) {
  int a, b, p, q;

  a = (x & 0x2) >> 1;
  b = (x & 0x1);
  p = a ^ b;
  q = a;
  *out = ((p << 1) | q);
}

/* square in GF(2^2), using normal basis (Omega^2,Omega) */
/* NOTE: inverse is identical */
void G4_sq(int x, int *out) {
  int a, b;

  a = (x & 0x2) >> 1;
  b = (x & 0x1);
  *out = ((b << 1) | a);
}

/* multiply in GF(2^4), using normal basis (alpha^8,alpha^2) */
void G16_mul(int x, int y, int *out) {
  int a, b, c, d, e, p, q, p1, q1;

  a = (x & 0xC) >> 2;
  b = (x & 0x3);
  c = (y & 0xC) >> 2;
  d = (y & 0x3);
  G4_mul(a ^ b, c ^ d, &e);
  G4_scl_N(e, &e);
  G4_mul(a, c, &p1);
  G4_mul(b, d, &q1);
  p = p1 ^ e;
  q = q1 ^ e;
  *out = ((p << 2) | q);
}

/* square & scale by nu in GF(2^4)/GF(2^2), normal basis (alpha^8,alpha^2) */
/*   nu = beta^8 = N^2*alpha^2, N = w^2 */
void G16_sq_scl(int x, int *out) {
  int a, b, p, q, q1;

  a = (x & 0xC) >> 2;
  b = (x & 0x3);
  G4_sq(a ^ b, &p);
  G4_sq(b, &q1);
  G4_scl_N2(q1, &q);
  *out = ((p << 2) | q);
}

/* inverse in GF(2^4), using normal basis (alpha^8,alpha^2) */
void G16_inv(int x, int *out) {
  int a, b, c, d, e, p, q, axorb;

  a = (x & 0xC) >> 2;
  b = (x & 0x3);
  G4_sq(a ^ b, &axorb);
  G4_scl_N(axorb, &c);
  G4_mul(a, b, &d);
  G4_sq(c ^ d, &e);  // really inverse, but same as square
  G4_mul(e, b, &p);
  G4_mul(e, a, &q);
  *out = ((p << 2) | q);
}

/* inverse in GF(2^8), using normal basis (d^16,d) */
void G256_inv(int x, int *out) {
  int a, b, c, d, e, p, q;

  a = (x & 0xF0) >> 4;
  b = (x & 0x0F);
  G16_sq_scl(a ^ b, &c);
  G16_mul(a, b, &d);
  G16_inv(c ^ d, &e);
  G16_mul(e, b, &p);
  G16_mul(e, a, &q);
  *out = ((p << 4) | q);
}

/* convert to new basis in GF(2^8) */
/* i.e., bit matrix multiply */
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

/* find Sbox of n in GF(2^8) mod POLY */
int Sbox(int n) {
  int t, t1, t2, t3;

  G256_newbasis(n, A2X, &t1);
  G256_inv(t1, &t2);
  G256_newbasis(t2, X2S, &t3);
  return (t3 ^ 0x63);
}

