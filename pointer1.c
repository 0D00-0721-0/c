#include  <stdio.h>
#include  <string.h>

int main(){

     int str[10] = {1,2,3,4,5};

     
     int *p = str;

     printf("%d\n%d\n",*p,*(p+2)); //执行 p + 2 时，地址的实际偏移量为 2 × sizeof(int)

     char *arr = "abcde";
     int i, l;
     l = strlen(arr);

     for (i = 0;i < l;i++){
        printf("%c\n",arr[i]);
     }



     
    /*

     printf("str的地址是%p\n", str);  //数组名指向第一个元素的地址
     printf("str的地址是%p\n", &str[0]);
     printf("str的地址是%p\n", &str[1]);
     */


     return 0;

}
