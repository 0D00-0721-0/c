#include <stdio.h>
#define maxsize 50
#include <stdbool.h>

typedef struct {
        int data[maxsize];
        int length;
    }sqList;
//初始化
void InitList(sqList *L){
    L->length = 0;

}
//第i个位置插入e
bool ListInsert(sqList *L,int i,int e){
    if(i>L->length+1||i<1){
         return false;
    }
    if(L->length==maxsize){
        return false;
    }
    for(int j =L->length;j>i-1;j--){//T(n)=O(n)
        L->data[j]=L->data[j-1];
    }
        L->data[i-1]=e;
        L->length++;
        return true;
    
}
//删除第i个数
bool ListDelete(sqList *L,int i,*e){
    if(i>L->length+1 || i<1){
         return false;
    }
    if(L->length==0){
        return false;
    }
    *e = L->data[i-1]; 
    for(int j = i;j<L->length;j++){
        L->data[j-1]=L->data[j];
    }
    L->length--;
    return true;
    
}
//按位查找
int GetElem(sqList *L,int i){
    return L->data[i-1];
}
//按值查找
void LocalElem(sqList *L,int n){
    for(int i = 0;i<L->length;i++){
        if(L->data[i]==n){
        return i+1 ;
        }
    }
    return 0;
    
}



int main(){
    sqList L;
    InitList(&L);
    for (int i = 1; i <= 10; i++) {
        ListInsert(&L, i, i);  // 在第i个位置插入i
    }
    ListInsert(&L,3,1);
    ListDelete(&L,3);
    for(int i = 0;i<L.length;i++){
    printf("%d ",L.data[i]);
    }
    return 0;
}