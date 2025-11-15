#include <stdio.h>

int main(){

    int a = 100;
    int *pa = &a;
    
    char *ps = "abcde";


    void *p;
    p = pa;
    printf("p = %p pa = %p\n",p,pa);
    printf("*p = %d *pa = %d\n",*(int*)p,*pa);


    p = ps;
    printf("*p = %s *ps = %s\n",(char*)p,ps);

    int *q = NULL;
    printf("%p\n",q);




    return 0;
}