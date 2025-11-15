#include <stdio.h>

void get_array(int a[]){
    
    printf("sizeof(a) = %lu\n",sizeof(a));
    for(int i = 0;i <= 4;i++){
        printf("%d\n",a[i]);
    }

}

int main(){

    int a[5] = {0,1,2,3,4};
    get_array(a);//a[0]的地址

    printf("sizeof(b) = %lu\n",sizeof(a));
    return 0;
} 