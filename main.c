#include <stdio.h>
#include "schedule.h"
#include "officehours.h"

int main(void)
{
    printf ("Generate Your Schedule\n");
    printf("---------------------------\n\n");

    readClassSchedule("class_schedule.txt");
    readFaculty("faculty.txt");

    printSchedule();
    generateOfficeHours();
    return 0;
}




