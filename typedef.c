#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//typedef 变量名 别名
typedef int mytype;

/*typedef struct 结构体名{

}别名;*/


typedef struct point{
    int a;
    int b;
}po;
int main(){
    po p;
    po *q = &p;
    q->a = 3;
    q->b = 4;
    printf("%d %d\n",p.a,p.b);


    char *s = NULL;
    s = (char*)malloc(6);
    strcpy(s,"abcde");
    printf("%s\n",s);
    free(s);
    s = NULL;

    return 0;
}