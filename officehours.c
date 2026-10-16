#include <stdio.h>
#include <string.h>
#include "officehours.h"

#define MAX_FACULTY 50

struct Faculty {
    char name[100];
    char department[50];
    char courses[300];
};

struct Faculty faculty[MAX_FACULTY];
int facultyCount = 0;

void readFaculty(const char *filename)
{
    FILE *file = fopen(filename, "r");

    if (file == NULL) {
        printf("Could not open %s\n", filename);
        return;
    }

    char line[500];

    while (fgets(line, sizeof(line), file) != NULL &&
           facultyCount < MAX_FACULTY) {

        char *part = strtok(line, "|");

        if (part != NULL) {
            strcpy(faculty[facultyCount].name, part);
        }

        part = strtok(NULL, "|");

        if (part != NULL) {
            strcpy(faculty[facultyCount].department, part);
        }

        part = strtok(NULL, "\n");

        if (part != NULL) {
            strcpy(faculty[facultyCount].courses, part);
        }

        facultyCount++;
    }

    fclose(file);
}

void generateOfficeHours(void)
{
    printf("\nOFFICE HOURS\n");
    printf("============\n");
    printf("NOTE: Instructors are not to be interrupted during class times.\n\n");

    for (int i = 0; i < facultyCount; i++) {

        int monday = 0;
        int tuesday = 0;
        int wednesday = 0;
        int thursday = 0;
        int friday = 0;

        FILE *file = fopen("class_schedule.txt", "r");

        if (file != NULL) {

            char line[500];

            while (fgets(line, sizeof(line), file) != NULL) {

                char copy[500];
                strcpy(copy, line);

                char *code = strtok(copy, "|");
                char *name = strtok(NULL, "|");
                char *days = strtok(NULL, "|");
                char *start = strtok(NULL, "|");
                char *end = strtok(NULL, "|");
                char *room = strtok(NULL, "|");
                char *professor = strtok(NULL, "|\n");

                if (professor != NULL &&
                    strcmp(professor, faculty[i].name) == 0) {

                    if (days != NULL) {

                        if (strchr(days, 'M') != NULL)
                            monday = 1;

                        if (strchr(days, 'T') != NULL)
                            tuesday = 1;

                        if (strchr(days, 'W') != NULL)
                            wednesday = 1;

                        if (strchr(days, 'R') != NULL)
                            thursday = 1;

                        if (strchr(days, 'F') != NULL)
                            friday = 1;
                    }
                }

                (void)code;
                (void)name;
                (void)start;
                (void)end;
                (void)room;
            }

            fclose(file);
        }

        printf("Professor: %s\n", faculty[i].name);
        printf("Department: %s\n", faculty[i].department);
        printf("Courses: %s\n", faculty[i].courses);

        if (!monday) {
            printf("Office Hours: Monday 10:00 AM - 12:00 PM\n");
        }
        else if (!tuesday) {
            printf("Office Hours: Tuesday 10:00 AM - 12:00 PM\n");
        }
        else if (!wednesday) {
            printf("Office Hours: Wednesday 10:00 AM - 12:00 PM\n");
        }
        else if (!thursday) {
            printf("Office Hours: Thursday 10:00 AM - 12:00 PM\n");
        }
        else if (!friday) {
            printf("Office Hours: Friday 10:00 AM - 12:00 PM\n");
        }
        else {
            printf("Office Hours: No available weekday found\n");
        }

        printf("\n");
    }
}

