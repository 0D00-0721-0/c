#include <stdio.h>

int max(int a,int b){

    if(a <b){
        return b;
    }
    else{
        return a;
    }
        
    
}


int main(){

    int a,b =0;
    printf("请输入两个数： \n");
    scanf("%d %d",&a,&b);

    printf("max(a,b) = %d\n",max(a,b));



    return 0;
}

