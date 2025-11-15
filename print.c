#include <stdio.h>

// void print(int a)
// {
//     int i = 1;
//     int b = a;
//     int c =1;
//     while(b >= 10){
//         b = b / 10;
//         i ++;
//         c = c * 10;

//     }
//     for( ;i >0;i--){
//         printf("%d ",a / c);
//         a = a%c;
//         c = c/10;
       


//     }
//     printf("\n");
    
// }

void print(int n){

    if(n > 9){
        print(n / 10);
    }
    printf("%d ",n % 10);
}



int main(){
    int a;
    scanf("%d",&a);
    print(a);
    printf("\n");
    return 0;
}