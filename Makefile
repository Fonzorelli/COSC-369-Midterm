CC = gcc
CFLAGS = -Wall

all: scheduler output.txt

schedule.o: schedule.c schedule.h
	$(CC) $(CFLAGS) -c schedule.c -o schedule.o

libschedule.a: schedule.o
	ar rcs libschedule.a schedule.o

officehours.o: officehours.c officehours.h
	$(CC) $(CFLAGS) -c officehours.c -o officehours.o

main.o: main.c schedule.h officehours.h
	$(CC) $(CFLAGS) -c main.c -o main.o

scheduler: main.o officehours.o libschedule.a
	$(CC) $(CFLAGS) main.o officehours.o -L. -lschedule -o scheduler

output.txt: scheduler class_schedule.txt faculty.txt
	./scheduler > output.txt

run: scheduler
	./scheduler

clean:
	rm -f *.o *.a scheduler output.txt
