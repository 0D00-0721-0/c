#include <stdio.h>

int main() {

    int matrix[3][4] = {{1,2,3,4},
                        {5,6,7,8},
                        {9,10,11,12}};  //3行4列
    int i, j;

    for(i=0;i<3;i++){

        for(j=0;j<4;j++){

            printf("%d ",matrix[i][j]);

        }
        printf("\n");


    }


} 