#include <stdio.h>

int main() {

    char a = 'F';
    int b = 100;

    int *const q = &b;//b的地址不能被改变 q不能指向其他变量
    const int *w = &b;//不能通过*w来改变
    char *pa = &a;  //*pa存放的地址指向的数据类型为char
    int *pb = &b;

    printf("a = %c\n",*pa); //a = F  
    printf("b = %d\n",*pb);

    *pa = 'A';
    *pb = 200;

    printf("a = %c\n",*pa); //指针指向变量的值  
    printf("b = %d\n",*pb);

    printf("a的地址 = %p\n", pa);  //指针地址的值
    printf("b的地址 = %p\n", pb);

    printf("sizeof *pa = %lu\n",sizeof(*pa)); //指针指向变量的值的大小
    printf("sizeof *pb = %lu\n",sizeof(*pb));

    printf("sizeof pa = %lu\n",sizeof(pa));  //指针地址的值的大小
    printf("sizeof pb = %lu\n",sizeof(pb));
    



    return 0;


}
