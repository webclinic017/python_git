#include<stdio.h>
#include<string.h>



int main() {
    FILE* fp = fopen("main_Lot_1_Wafer_1_Oct_13_09h33m41s_STDF.tar", "rb");

    char SpaceSize = 18;
    char space[SpaceSize];
    int x, y;
    char PartId[3];
    char IdLength;
    int num = 0;
    int MaxDataNum = 100;
    int X[MaxDataNum];
    int Y[MaxDataNum];
    int id[MaxDataNum];
    int row, column;
    int MaxX, MinX;
    int MaxY, MinY;
    char c;

    if (fp == NULL) {
        printf("open file error!!\n");
        return -1;
    }
    while (!feof(fp)) {

        c = fgetc(fp);
        if (c == 0x05){
            c = fgetc(fp);
            if (c == 0x14) {
                fread(space, sizeof(char), SpaceSize, fp);
                x=-(~(space[9]|space[10]<<8)+1);
                y=-(~(space[11]|space[12]<<8)+1);
                IdLength=space[17];
                fread(PartId, sizeof(char),IdLength,fp);
                X[num]=x;
                Y[num]=y;
                sscanf(PartId,"%d",&id[num]);
                if (num == MaxDataNum) {
                    break;
                }
                else if (num == 0) {
                    MaxX=X[0];
                    MinX=X[0];
                    MaxY=Y[0];
                    MinY=Y[0];
                }
                else {
                    MaxX=X[num]>MaxX?X[num]:MaxX;
                    MinX=X[num]<MinX?X[num]:MinX;
                    MaxY=Y[num]>MaxY?Y[num]:MaxY;
                    MinY=Y[num]<MinY?Y[num]:MinY;
                }
                num++;
            }
        }
    }
    fclose(fp);

    row=MaxY-MinY+1;
    column=MaxX-MinX+1;
    int matrix[row][column];
    memset(matrix,0, sizeof(matrix));

    for (int i=0;i<num;i++) {
        matrix[Y[i]-MinY][X[i]-MinX]=id[i];
    }
    printf("ANS: ");

    for (int i=0;i<column;i++) {
        printf("%3d",MinX+i);
    }
    printf("\n");

    for (int i=0;i<row;i++) {
        printf("%3d: ",MinY+i);

        for (int j=0;j<column;j++) {
            printf("%3d", matrix[i][j]);
        }

        printf("\n");
    }
    for(int i=0;i<num;i++){
    printf(" y=%3d, x=%3d, PartId=%3d\n",Y[i],X[i],id[i]);
    }

    return 0;
}
