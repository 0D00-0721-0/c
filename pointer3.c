#include <stdio.h>


int main (){


    int a[3] = {1 ,2 ,3};
    int (*p)[3] = &a; //数组指针

    

    printf("%d\n",*(*p+1));   //*p为a的地址 *(*p+1)将地址取值

    printf("%p\n",&a);

    return 0;




}  