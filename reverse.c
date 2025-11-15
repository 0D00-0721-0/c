#include <stdio.h>
#include <string.h>

void reverse(char arr[],int i,int e){
   
    
   if(i < e){
        char temp = arr[i];
        arr[i] = arr[e];
        arr[e] = temp;
        reverse(arr,i+1,e-1);
    }
    else
    return;


    
}
int main(){

    char arr[] = "abcdef";
    int len = strlen(arr);
    reverse(arr,0,len-1);
    printf("%s\n",arr);
    return 0;
}