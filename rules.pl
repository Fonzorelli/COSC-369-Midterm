instructor(Course, Professor) :-
    professor_for(Course, Professor).

teaching(Professor, Course) :-
    professor_for(Course, Professor).

wednesday_class(Course) :-
    days(Course, Days),
    sub_atom(Days, _, 1, _, w).

teaches_wednesday(Professor) :-
    professor_for(Course, Professor),
    wednesday_class(Course).

course_in_room(Course, Room) :-
    room(Course, Room).

same_professor(Course1, Course2) :-
    professor_for(Course1, Professor),
    professor_for(Course2, Professor),
    Course1 \= Course2.
