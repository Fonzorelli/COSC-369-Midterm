:- dynamic office_hours/4.

has_office_hours_on(Professor, Day, Start, End) :-
    office_hours(Professor, Day, Start, End).

wednesday_office_hours(Professor, Start, End) :-
    has_office_hours_on(Professor, wednesday, Start, End).
