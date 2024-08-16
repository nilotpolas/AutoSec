#include <stdbool.h>

void comar(bool a0, bool b0, bool a1, bool b1, bool r0, bool r1, bool r0_1, bool r1_1, bool r2_1, bool r3_1, bool *y0, bool *y1)
{
    bool i1, i2, p4, p2, p3, p1, i1xori2, i0xori3, m0, m1, m2, m3, i0, i3;
    bool y1_1, y1_2, y1_3, y1_4;
    m0 = a0 ^ r0;
    m1 = b1 ^ r1;
    m2 = b0 ^ r1;
    m3 = a1 ^ r0;
    p2 = reg(m0) & reg(m1);
    p3 = reg(m3) & reg(m2);
    p1 = reg(m0) & reg(m2);
    p4 = reg(m3) & reg(m1);
    i0 = p1 ^ r0_1;
    i1 = p2 ^ r1_1;
    i2 = p3 ^ r2_1;
    i3 = p4 ^ r3_1;
    i1xori2 = reg(i1) ^ reg(i2);
    i0xori3 = reg(i0) ^ reg(i3);
    *y0 = reg(i1xori2 ^ i0xori3);
    y1_1 = r0 ^ r1;
    y1_2 = y1_1 ^ r0_1;
    y1_3 = y1_2 ^ r1_1;
    y1_4 = y1_3 ^ r2_1;
    *y1 = y1_4 ^ r3_1;
    
}
void sbox(bool x0_0, bool x1_0, bool x2_0, bool x3_0, bool x0_1, bool x1_1, bool x2_1, bool x3_1, bool r0, bool r1, bool r0_1, bool r1_1, bool r2_1, bool r3_1, bool *Y0_0, bool *Y1_0, bool *Y2_0, bool *Y3_0, bool *Y0_1, bool *Y1_1, bool *Y2_1, bool *Y3_1)
{

    bool L0_0, L1_0, L2_0, L3_0, L4_0, L5_0, L6_0, L7_0, L8_0, L9_0, L10_0, L11_0, Q0_0, Q1_0, Q2_0, Q3_0, Q4_0, Q5_0, Q6_0, Q7_0,
        T0_0, T1_0, T2_0, T3_0, Y0_01, Y1_01, L0_1, L1_1, L2_1, L3_1, L4_1, L5_1, L6_1, L7_1, L8_1, L9_1, L10_1, L11_1, Q0_1, Q1_1, Q2_1, Q3_1, Q4_1, Q5_1, Q6_1, Q7_1,
        T0_1, T1_1, T2_1, T3_1, Y0_11, Y1_11;

    L0_0 = x1_0 ^ x2_0;
    L1_0 = x0_0 ^ x1_0;
    L8_0 = x2_0 ^ x0_0;
    L5_0 = x0_0 ^ x3_0;
    L0_1 = x1_1 ^ x2_1;
    L1_1 = x0_1 ^ x1_1;
    L8_1 = x2_1 ^ x0_1;
    L5_1 = x0_1 ^ x3_1;

    Q0_0 = !L0_0;
    Q1_0 = !L1_0;
    Q3_0 = !x3_0;
    Q4_0 = !x2_0;
    Q0_1 = !L0_1;
    Q1_1 = !L1_1;
    Q3_1 = !x3_1;
    Q4_1 = !x2_1;

    L2_0 = Q1_0 ^ x2_0;
    L3_0 = Q0_0 ^ x3_0;
    L2_1 = Q1_1 ^ x2_1;
    L3_1 = Q0_1 ^ x3_1;

    comar(Q0_0, Q1_0, Q0_1, Q1_1, r0, r1, r0_1, r1_1, r2_1, r3_1, &T0_0, &T0_1);
    L10_0 = !L2_0;
    L10_1 = !L2_1;
    comar(x1_0, Q4_0, x1_1, Q4_1, r0, r1, r0_1, r1_1, r2_1, r3_1, &T2_0, &T2_1);

    Q2_0 = T0_0 ^ L2_0;
    L4_0 = T0_0 ^ T2_0;
    Q7_0 = T0_0 ^ L5_0;
    Q6_0 = L4_0 ^ L3_0;
    Q2_1 = T0_1 ^ L2_1;
    L4_1 = T0_1 ^ T2_1;
    Q7_1 = T0_1 ^ L5_1;
    Q6_1 = L4_1 ^ L3_1;
    comar(Q2_0, Q3_0, Q2_1, Q3_1, r0, r1, r0_1, r1_1, r2_1, r3_1, &T1_0, &T1_1);

    comar(Q6_0, Q7_0, Q6_1, Q7_1, r0, r1, r0_1, r1_1, r2_1, r3_1, &T3_0, &T3_1);

    L7_0 = T0_0 ^ T1_0;
    L11_0 = T1_0 ^ L10_0;
    L7_1 = T0_1 ^ T1_1;
    L11_1 = T1_1 ^ L10_1;

    Y0_01 = L7_0 ^ T2_0;
    Y1_01 = L8_0 ^ T3_0;
    Y0_11 = L7_1 ^ T2_1;
    Y1_11 = L8_1 ^ T3_1;

    *Y0_0 = reg(x3_0 ^ Y0_01);
    *Y1_0 = reg(L7_0 ^ Y1_01);
    *Y2_0 = reg(L11_0 ^ T2_0);
    *Y3_0 = reg(T2_0 ^ L5_0);
    *Y0_1 = reg(x3_1 ^ Y0_11);
    *Y1_1 = reg(L7_1 ^ Y1_11);
    *Y2_1 = reg(L11_1 ^ T2_1);
    *Y3_1 = reg(T2_1 ^ L5_1);
}