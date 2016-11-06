#include "mbed.h"
#include "SDFileSystem.h"
#include "stdio.h"

AnalogIn IRSensor(p19);
Serial pc(USBTX, USBRX); // tx, rx
SDFileSystem sd(p5, p6, p7, p8, "sd"); // the pinout on the mbed Cool Components workshop board

int main()
{
    int time = 0.5;
    mkdir("/sd/mydir", 0777);
    FILE *fp = fopen("/sd/mydir/data.csv", "w+");
    if(fp == NULL) {
        error("Could not open file for write\n");
    }
    //fclose(fp);
    int i = 0;
    while(1) {
        wait(time);
        //3.1V at 4cm to 0.3V at 30cm.
        float ir = IRSensor;// 1=4cm 0=30cm
        //pc.printf("IR sensor reads %2.2f\n ", a);
        ir = 1-ir;// now 0=4cm and 1=30cm
        pc.printf("\rDistance is %2.2f cm \n ", (ir*26+4)); // print and convert to distance by taking x=0->1 and 26*x+4
        //fprintf(fp, "Hello fun SD Card World!");
        fprintf(fp,"%f\n", ir*26+4);
        i++;
        if (i > 100) {
            break;
        }
        // save to file
    }
    fclose(fp);
    pc.printf("I am done");
}
