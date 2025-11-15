#include <stdio.h>

int main () {

    char str[] = "abcdehejfk";
    int count = 0;
    char *p = str;

     while(*(p++) != '\0'){  

         count++ ;

     }

    // while(*(str++) != '\0'){      错误 数组名str是常量指针 不能自增

    //     count++ ;

    // }
    printf("%d\n",count);

    return 0;





}