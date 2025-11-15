#include <stdio.h>

int main(){

    int i ;
    int a ;
    int c = 1;
    printf("请输入一个数\n");
    scanf("%d",&a);

    for (i = 2; i <= a/2; i++)
    {
        int ret = a%i;
        if (ret == 0)
        {
            c = 0;
            break;
        }

    }

    if (c == 1)
    {
        printf("%d是素数\n", a);
    }
    else
    {
        printf("%d不是素数\n", a);
    }

    return 0;
}
       


        

        
    
   
   

    

