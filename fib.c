#include <stdio.h>

int fib(int n){

    int a =1;
    int b =1;
    int c = a + b;
    for(int i = 1;i<n;i++){
        a = b;
        b = c;
        c = a + b;
    }
    return a;
}

int main(){

    int n = 0;
    scanf("%d",&n);
    int y = fib(n);
    printf("%d\n",y);

    return 0;
}