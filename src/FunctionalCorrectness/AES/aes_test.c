#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#include "aes.c" 
#define TEST_CASES 255

int Sbox(int n);

int main() {

    int test_cases = 0;
    // while(test_cases < TEST_CASES){
	// srand(test_cases);

	// Generate random inputs
	for(int x0_0 = 0; x0_0 < 255; x0_0++){
        for(int x0_1 = 0; x0_1 < 255; x0_1++){
            printf("%d, ", x0_0 ^ x0_1);
        
        
        int Y;

        Y = Sbox(x0_0 ^ x0_1);

        printf("%3d", Y);
       
        test_cases++;
        printf("\n");
        }
    }
	
    return 0;  
}


