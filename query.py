
from pyswip import Prolog
from datetime import datetime
from collections import Counter
import re

prolog = Prolog()
prolog.consult("knowledge.pl")
prolog.consult("schedule.pl")
prolog.consult("rules.pl")
prolog.consult("office_hours.pl")

DAYS = {
    "monday": "m", "mon": "m", "m": "m",
    "tuesday": "t", "tue": "t", "t": "t",
    "wednesday": "w", "wed": "w", "w": "w",
    "thursday": "r", "thu": "r", "r": "r",
    "friday": "f", "fri": "f", "f": "f"
}


def clean(text):
    text = re.sub(r"[^a-z0-9]+", "_", text.strip().lower())
    text = text.strip("_")
    if text and text[0].isdigit():
        text = "v_" + text
    return text


def pretty(text):
    text = str(text)
    if text.startswith("v_"):
        text = text[2:]
    return text.replace("_", " ")


def pretty_course(course):
    parts = str(course).split("_")
    if len(parts) >= 3:
        return f"{parts[0].upper()} {parts[1]}.{parts[2]}"
    return pretty(course).upper()


def current_day():
    return DAYS.get(datetime.now().strftime("%A").lower(), "")


def current_day_name():
    return datetime.now().strftime("%A")


def current_time():
    return datetime.now().strftime("%I:%M %p")


def time_to_minutes(value):
    value = pretty(value).strip().upper()
    try:
        t = datetime.strptime(value, "%I:%M %p")
        return t.hour * 60 + t.minute
    except ValueError:
        return None


def minutes_to_time(minutes):
    hour, minute = divmod(minutes, 60)
    period = "AM" if hour < 12 else "PM"
    display_hour = hour % 12 or 12
    return f"{display_hour}:{minute:02d} {period}"


def get_classes():
    query = """
        course(Course),
        days(Course, Days),
        start_time(Course, Start),
        end_time(Course, End),
        room(Course, Room),
        professor_for(Course, Professor)
    """
    classes = []
    for r in prolog.query(query):
        classes.append({
            "course": str(r["Course"]),
            "days": str(r["Days"]),
            "start": str(r["Start"]),
            "end": str(r["End"]),
            "room": str(r["Room"]),
            "professor": str(r["Professor"])
        })
    return classes


def is_on_day(c, day):
    return bool(day) and day in c["days"].lower()


def is_active(c, day, minute):
    start = time_to_minutes(c["start"])
    end = time_to_minutes(c["end"])
    return (
        is_on_day(c, day)
        and minute is not None
        and start is not None
        and end is not None
        and start < end
        and start <= minute < end
    )


def is_physical_room(room):
    return pretty(room).isdigit()


def show_class(c):
    print(
        pretty_course(c["course"]),
        "|", pretty(c["days"]).upper(),
        "|", pretty(c["start"]),
        "-", pretty(c["end"]),
        "| Room", pretty(c["room"]),
        "|", pretty(c["professor"]).title()
    )


def show_course():
    course = clean(input("\nEnter course: "))
    results = [c for c in get_classes() if c["course"] == course]

    if not results:
        print("Course not found.")
        return

    for c in results:
        print("\nCourse:", pretty_course(c["course"]))
        print("Professor:", pretty(c["professor"]).title())
        print("Room:", pretty(c["room"]))
        print("Days:", pretty(c["days"]).upper())
        print("Start:", pretty(c["start"]))
        print("End:", pretty(c["end"]))


def classes_today():
    print("\nToday:", current_day_name())
    print("Classes today:")
    results = [c for c in get_classes()
               if is_on_day(c, current_day())]

    if not results:
        print("No classes scheduled today.")

    for c in results:
        show_class(c)


def classes_by_day():
    day = DAYS.get(input("\nEnter day: ").strip().lower())
    if not day:
        print("Invalid weekday.")
        return

    results = [c for c in get_classes() if is_on_day(c, day)]
    print("\nClasses:")

    if not results:
        print("No classes found.")

    for c in results:
        show_class(c)


def rooms_in_use_now():
    day = current_day()
    minute = time_to_minutes(current_time())
    print("\nDay:", current_day_name())
    print("Time:", current_time())
    print("Rooms being used right now:")

    results = [
        c for c in get_classes()
        if is_physical_room(c["room"])
        and is_active(c, day, minute)
    ]

    if not results:
        print("No physical rooms are being used right now.")

    for c in results:
        show_class(c)


def free_rooms_now():
    classes = get_classes()
    all_rooms = {
        c["room"] for c in classes
        if is_physical_room(c["room"])
    }
    busy = {
        c["room"] for c in classes
        if is_physical_room(c["room"])
        and is_active(c, current_day(),
                      time_to_minutes(current_time()))
    }

    print("\nOpen rooms right now:")
    print("Based on rooms listed in the schedule.")

    for room in sorted(all_rooms - busy):
        print("Room", pretty(room))

    if not all_rooms - busy:
        print("No available rooms found.")


def most_used_rooms():
    counts = Counter(
        pretty(c["room"]) for c in get_classes()
        if is_physical_room(c["room"])
    )

    print("\nMost used rooms:")
    for room, count in counts.most_common():
        print("Room", room, "-", count, "class entries")


def room_schedule():
    room = clean(input("\nEnter room number: "))
    results = [c for c in get_classes() if c["room"] == room]

    print("\nSchedule for Room", pretty(room))
    if not results:
        print("No classes found.")
        return

    results.sort(
        key=lambda c: time_to_minutes(c["start"]) or 0
    )
    for c in results:
        show_class(c)


def open_times_today():
    room = clean(input("\nEnter room number: "))
    day = current_day()
    start_day = 8 * 60
    end_day = 22 * 60
    intervals = []

    for c in get_classes():
        if c["room"] != room or not is_on_day(c, day):
            continue

        start = time_to_minutes(c["start"])
        end = time_to_minutes(c["end"])

        if start is None or end is None or start >= end:
            continue

        start = max(start_day, start)
        end = min(end_day, end)

        if start < end:
            intervals.append((start, end))

    intervals.sort()
    current = start_day

    print("\nOpen times for Room", pretty(room))
    print("Day:", current_day_name())

    found = False

    for start, end in intervals:
        if start > current:
            print(
                minutes_to_time(current),
                "-", minutes_to_time(start)
            )
            found = True
        current = max(current, end)

    if current < end_day:
        print(
            minutes_to_time(current),
            "-", minutes_to_time(end_day)
        )
        found = True

    if not found:
        print("No open times today.")


def room_usage_at_time():
    user_time = input("\nEnter time, example 4:30 PM: ")
    minute = time_to_minutes(user_time)

    if minute is None:
        print("Invalid time. Use 4:30 PM format.")
        return

    print("\nRooms being used on", current_day_name())
    print("Time:", user_time)

    results = [
        c for c in get_classes()
        if is_physical_room(c["room"])
        and is_active(c, current_day(), minute)
    ]

    if not results:
        print("No physical rooms are being used at that time.")

    for c in results:
        show_class(c)


def search_professor():
    name = input("\nEnter professor name: ")
    professor = clean(name)

    results = list(
        prolog.query(f"teaching({professor}, Course)")
    )

    if not results:
        print("Professor not found.")
        return

    print("\nProfessor:", name.title())
    print("Courses taught:")

    for result in results:
        print(pretty_course(result["Course"]))


def who_teaches_course():
    course = clean(input("\nEnter course: "))

    results = list(
        prolog.query(f"instructor({course}, Professor)")
    )

    if not results:
        print("Course not found.")
        return

    for result in results:
        print(
            "\nProfessor:",
            pretty(result["Professor"]).title()
        )


def wednesday_professors():
    results = list(
        prolog.query("setof(P, teaches_wednesday(P), Professors)")
    )

    print("\nProfessors teaching Wednesday:")

    if not results:
        print("No professors found.")
        return

    for professor in results[0]["Professors"]:
        print(pretty(professor).title())


def wednesday_office_hours():
    print("\nWednesday Office Hours")

    available = bool(list(prolog.query(
        "current_predicate(office_hours/4)"
    )))

    if not available:
        print("Verified office-hour facts are not loaded.")
        print("Add the office-hour information from the syllabi.")
        return

    results = list(prolog.query(
        "office_hours(Professor, wednesday, Start, End)"
    ))

    if not results:
        print("No Wednesday office hours recorded.")
        return

    for r in results:
        print(
            pretty(r["Professor"]).title(),
            "|", pretty(r["Start"]),
            "-", pretty(r["End"])
        )


def main():
    while True:
        print("\n==============================")
        print("    OFFICE HOURS SCHEDULER")
        print("==============================")
        print("Today:", current_day_name())
        print("Current time:", current_time())
        print()
        print("1. Look up course")
        print("2. Show today's classes")
        print("3. Rooms being used right now")
        print("4. Open rooms right now")
        print("5. Most used rooms")
        print("6. Room schedule")
        print("7. Open times for a room today")
        print("8. Classes by another day")
        print("9. Room usage at a certain time today")
        print("10. Search for professor")
        print("11. Who teaches a course")
        print("12. Professors teaching Wednesday")
        print("13. Wednesday office hours")
        print("14. Exit")

        choice = input("\nChoose an option: ")

        actions = {
            "1": show_course,
            "2": classes_today,
            "3": rooms_in_use_now,
            "4": free_rooms_now,
            "5": most_used_rooms,
            "6": room_schedule,
            "7": open_times_today,
            "8": classes_by_day,
            "9": room_usage_at_time,
            "10": search_professor,
            "11": who_teaches_course,
            "12": wednesday_professors,
            "13": wednesday_office_hours
        }

        if choice == "14":
            print("Goodbye")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

