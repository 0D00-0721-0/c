#include <stdio.h>

void bubblesort(int arr[], int sz){
    int i =0;
    if(sz<=1)
    return;
    for(i = 0;i<sz-1;i++){
        int temp =arr[i];
        if(arr[i]>arr[i+1])
        {
            arr[i] = arr[i+1];
            arr[i+1] = temp;

        }
    }
    bubblesort(arr,sz-1);
}

int main(){

    int arr[] = {1,4,6,2,8,3};
    int sz= sizeof(arr)/sizeof(arr[0]);
    bubblesort(arr,sz);
    for(int i =0;i < sz;i++){
        printf("%d ",arr[i]);
        
    }
    
    printf("\n");
    return 0 ;
}