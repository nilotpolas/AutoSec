// longest path 5
#include <stdbool.h>

void hpc2(bool a0, bool a1, bool b0, bool b1, bool r, bool *y0, bool *y1)
{
    bool u0, u1, i0, i1, v0, v1, p0, p1, p01, p2, p3, p23, a0_neg, a1_neg;
    a0_neg = !a0;
    a1_neg = !a1;
    u0 = a0_neg & reg(r);
    u1 = a1_neg & reg(r);
    v0 = b0 ^ r;
    v1 = b1 ^ r;
    p0 = a0 & reg(b0);
    p1 = a0 & reg(v1);
    p01 = reg(u0) ^ reg(p1);
    *y0 = reg(p0) ^ p01; 
    p2 = a1 & reg(b1);                                            
    p3 = a1 & reg(v0);
    p23 = reg(u1) ^ reg(p3);
    *y1 = reg(p2) ^ p23;
    
}

void sbox(bool x0_0, bool x1_0, bool x2_0, bool x3_0, bool x0_1, bool x1_1, bool x2_1, bool x3_1, bool r, bool *Y0_0, bool *Y1_0, bool *Y2_0, bool *Y3_0, bool *Y0_1, bool *Y1_1, bool *Y2_1, bool *Y3_1){

    bool L0_0, L1_0, L2_0, L3_0, L4_0, L5_0, L6_0, L7_0, L8_0, L9_0, L10_0, L11_0, Q0_0, Q1_0, Q2_0, Q3_0, Q4_0, Q5_0, Q6_0, Q7_0,
        T0_0, T1_0, T2_0, T3_0, L0_1, L1_1, L2_1, L3_1, L4_1, L5_1, L6_1, L7_1, L8_1, L9_1, L10_1, L11_1, Q0_1, Q1_1, Q2_1, Q3_1, Q4_1,
        Q5_1, Q6_1, Q7_1, T0_1, T1_1, T2_1, T3_1, Y0_01, Y1_01, Y0_11, Y1_11;

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

    hpc2(Q0_0, Q0_1, Q1_0, Q1_1, r, &T0_0, &T0_1);

    L10_0 = !L2_0;
    L10_1 = !L2_1;

    hpc2(x1_0, x1_1, Q4_0, Q4_1, r, &T2_0, &T2_1);

    Q2_0 = T0_0 ^ L2_0;
    L4_0 = T0_0 ^ T2_0;
    Q7_0 = T0_0 ^ L5_0;
    Q6_0 = L4_0 ^ L3_0;
    Q2_1 = T0_1 ^ L2_1;
    L4_1 = T0_1 ^ T2_1;
    Q7_1 = T0_1 ^ L5_1;
    Q6_1 = L4_1 ^ L3_1;

    hpc2(Q2_0, Q2_1, Q3_0, Q3_1, r, &T1_0, &T1_1);

    hpc2(Q6_0, Q6_1, Q7_0, Q7_1, r, &T3_0, &T3_1);

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