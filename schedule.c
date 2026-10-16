#include <stdio.h>
#include <string.h>
#include "schedule.h"

#define MAX_CLASSES 60

struct ClassInfo {
    char code[20];
    char name[100];
    char days[50];
    char startTime[50];
    char endTime[20];
    char room[20];
    char professor[100];
};

struct ClassInfo classes[MAX_CLASSES];
int classCount = 0;

void readClassSchedule(const char *filename)
{
    FILE *file = fopen(filename, "r");

    if (file == NULL) {
        printf("Could not open %s\n", filename);
        return;
    }

    char line[400];

    while (fgets(line, sizeof(line), file) != NULL &&
           classCount < MAX_CLASSES) {

        char *part = strtok(line, "|");

        if (part != NULL) {
            strcpy(classes[classCount].code, part);
        }

        part = strtok(NULL, "|");
        if (part != NULL) {
            strcpy(classes[classCount].name, part);
        }

        part = strtok(NULL, "|");
        if (part != NULL) {
            strcpy(classes[classCount].days, part);
        }

        part = strtok(NULL, "|");
        if (part != NULL) {
            strcpy(classes[classCount].startTime, part);
        }

        part = strtok(NULL, "|");
        if (part != NULL) {
            strcpy(classes[classCount].endTime, part);
        }

        part = strtok(NULL, "|");
        if (part != NULL) {
            strcpy(classes[classCount].room, part);
        }

        part = strtok(NULL, "|\n");
        if (part != NULL) {
            strcpy(classes[classCount].professor, part);
        }

        classCount++;
    }

    fclose(file);
}

void printSchedule(void)
{
    printf("\nCLASS SCHEDULE\n");
    printf("==============\n");

    for (int i = 0; i < classCount; i++) {

        printf("\nCourse: %s - %s\n",
               classes[i].code,
               classes[i].name);

        printf("Days: %s\n",
               classes[i].days);

        printf("Time: %s - %s\n",
               classes[i].startTime,
               classes[i].endTime);

        printf("Room: %s\n",
               classes[i].room);

        printf("Professor: %s\n",
               classes[i].professor);
    }
}
