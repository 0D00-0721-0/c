#include <stdio.h>

int my_strlen(char *str){
    int i = 0;
    if(*str != '\0'){
        
        return i =1 + my_strlen(str + 1);
    }
   
    return i;
}


int main(){

    char* str = "abc";
    printf("%d\n",my_strlen(str ));



    return 0;
}