from pyswip import Prolog
from datetime import datetime
from collections import Counter
import re

prolog = Prolog()

prolog.consult("knowledge.pl")
prolog.consult("schedule.pl")
prolog.consult("rules.pl")

def clean(text):
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')


def pretty(text):
    text = str(text)

    if text.startswith("v_"):
        text = text[2:]

    text = text.replace("_", " ")

    parts = text.split()

    if len(parts) == 3:
        if parts[0].isdigit() and parts[1].isdigit():
            return f"{parts[0]}:{parts[1]} {parts[2].upper()}"

    return text


def pretty_course(course):
    course = str(course)

    parts = course.split("_")

    if len(parts) >= 3:
        return f"{parts[0].upper()} {parts[1]}.{parts[2]}"

    return pretty(course).upper()


def current_day():
    day = datetime.now().strftime("%A").lower()

    days = {
        "monday": "m",
        "tuesday": "t",
        "wednesday": "w",
        "thursday": "r",
        "friday": "f"
    }

    return days.get(day, "")


def current_day_name():
    return datetime.now().strftime("%A")


def current_time():
    return datetime.now().strftime("%I:%M %p")


def time_to_minutes(time_text):
    time_text = pretty(time_text)

    try:
        time_part, period = time_text.split()

        hour, minute = time_part.split(":")

        hour = int(hour)
        minute = int(minute)

        if period.upper() == "PM" and hour != 12:
            hour += 12

        if period.upper() == "AM" and hour == 12:
            hour = 0

        return hour * 60 + minute

    except:
        return -1


def minutes_to_time(minutes):
    hour = minutes // 60
    minute = minutes % 60

    period = "AM"

    if hour >= 12:
        period = "PM"

    display_hour = hour % 12

    if display_hour == 0:
        display_hour = 12

    return f"{display_hour}:{minute:02d} {period}"


def normalize_day(day):
    day = day.strip().lower()

x    days = {
        "monday": "m",
        "mon": "m",
        "m": "m",

        "tuesday": "t",
        "tue": "t",
        "t": "t",

        "wednesday": "w",
        "wed": "w",
        "w": "w",

        "thursday": "r",
        "thu": "r",
        "r": "r",

        "friday": "f",
        "fri": "f",
        "f": "f"
    }

    return days.get(day, day)


def get_classes():
    classes = []

    query = """
    course(Course),
    days(Course, Days),
    start_time(Course, Start),
    end_time(Course, End),
    room(Course, Room),
    professor_for(Course, Professor)
    """

    for result in prolog.query(query):

        classes.append({
            "course": str(result["Course"]),
            "days": str(result["Days"]),
            "start": str(result["Start"]),
            "end": str(result["End"]),
            "room": str(result["Room"]),
            "professor": str(result["Professor"])
        })

    return classes


def show_course():
    course_input = input("\nEnter course: ")

    course = clean(course_input)

    found = False

    for result in prolog.query(
        f"""
        days({course}, Days),
        start_time({course}, Start),
        end_time({course}, End),
        room({course}, Room),
        professor_for({course}, Professor)
        """
    ):

        found = True

        print()
        print("Course:", pretty_course(course))
        print("Professor:", pretty(result["Professor"]).title())
        print("Room:", pretty(result["Room"]))
        print("Days:", pretty(result["Days"]).upper())
        print("Start:", pretty(result["Start"]))
        print("End:", pretty(result["End"]))

    if not found:
        print("Course not found.")


def classes_today():
    day = current_day()

    classes = get_classes()

    found = False

    print()
    print("Today:", current_day_name())
    print("Classes today:")

    for c in classes:

        if day in c["days"].lower():

            found = True

            print(
                pretty_course(c["course"]),
                "|",
                pretty(c["start"]),
                "-",
                pretty(c["end"]),
                "| Room",
                pretty(c["room"])
            )

    if not found:
        print("No classes scheduled today.")


def classes_by_day():
    day_input = input("\nEnter day: ")

    day = normalize_day(day_input)

    classes = get_classes()

    found = False

    print("\nClasses:")

    for c in classes:

        if day in c["days"].lower():

            found = True

            print(
                pretty_course(c["course"]),
                "|",
                pretty(c["start"]),
                "-",
                pretty(c["end"]),
                "| Room",
                pretty(c["room"])
            )

    if not found:
        print("No classes found.")


def rooms_in_use_now():
    day = current_day()

    now = current_time()

    now_minutes = time_to_minutes(now)

    classes = get_classes()

    found = False

    print()
    print("Day:", current_day_name())
    print("Time:", now)
    print()
    print("Rooms being used right now:")

    for c in classes:

        start = time_to_minutes(c["start"])
        end = time_to_minutes(c["end"])

        if (
            day in c["days"].lower()
            and start <= now_minutes < end
        ):

            found = True

            print(
                "Room",
                pretty(c["room"]),
                "-",
                pretty_course(c["course"]),
                "-",
                pretty(c["professor"]).title()
            )

    if not found:
        print("No rooms are being used right now.")


def free_rooms_now():
    day = current_day()

    now = current_time()

    now_minutes = time_to_minutes(now)

    classes = get_classes()

    all_rooms = set()

    busy_rooms = set()

    for c in classes:

        room = pretty(c["room"])

        all_rooms.add(room)

        start = time_to_minutes(c["start"])
        end = time_to_minutes(c["end"])

        if (
            day in c["days"].lower()
            and start <= now_minutes < end
        ):
            busy_rooms.add(room)

    open_rooms = sorted(all_rooms - busy_rooms)

    print()
    print("Day:", current_day_name())
    print("Time:", now)
    print()
    print("Open rooms right now:")

    if open_rooms:

        for room in open_rooms:
            print("Room", room)

    else:
        print("No rooms are open right now.")


def most_used_rooms():
    classes = get_classes()

    rooms = []

    for c in classes:
        rooms.append(pretty(c["room"]))

    counts = Counter(rooms)

    print("\nMost used rooms:")

    for room, count in counts.most_common():

        print(
            "Room",
            room,
            "-",
            count,
            "classes"
        )


def room_schedule():
    room_input = clean(
        input("\nEnter room number: ")
    )

    if room_input and room_input[0].isdigit():
        room_input = "v_" + room_input

    classes = get_classes()

    room_classes = []

    for c in classes:

        if c["room"] == room_input:
            room_classes.append(c)

    room_classes.sort(
        key=lambda x: time_to_minutes(x["start"])
    )

    print(
        "\nSchedule for Room",
        pretty(room_input)
    )

    if not room_classes:
        print("No classes found for this room.")
        return

    for c in room_classes:

        print(
            pretty_course(c["course"]),
            "|",
            pretty(c["days"]).upper(),
            "|",
            pretty(c["start"]),
            "-",
            pretty(c["end"]),
            "|",
            pretty(c["professor"]).title()
        )


def open_times_today():
    room_input = clean(
        input("\nEnter room number: ")
    )

    if room_input and room_input[0].isdigit():
        room_input = "v_" + room_input

    day = current_day()

    classes = get_classes()

    room_classes = []

    for c in classes:

        if (
            c["room"] == room_input
            and day in c["days"].lower()
        ):
            room_classes.append(c)

    room_classes.sort(
        key=lambda x: time_to_minutes(x["start"])
    )

    day_start = 8 * 60
    day_end = 22 * 60

    current = day_start

    print()
    print("Day:", current_day_name())
    print(
        "Open times for Room",
        pretty(room_input)
    )

    if not room_classes:
        print("8:00 AM - 10:00 PM")
        return

    found_open_time = False

    for c in room_classes:

        start = time_to_minutes(c["start"])
        end = time_to_minutes(c["end"])

        if start > current:

            found_open_time = True

            print(
                minutes_to_time(current),
                "-",
                minutes_to_time(start)
            )

        if end > current:
            current = end

    if current < day_end:

        found_open_time = True

        print(
            minutes_to_time(current),
            "-",
            minutes_to_time(day_end)
        )

    if not found_open_time:
        print("No open times today.")


def room_usage_at_time():
    day = current_day()

    user_time = input(
        "\nEnter time, example 4:30 PM: "
    )

    user_minutes = time_to_minutes(user_time)

    classes = get_classes()

    found = False

    print()
    print("Day:", current_day_name())
    print("Time:", user_time)
    print()
    print("Rooms being used:")

    for c in classes:

        start = time_to_minutes(c["start"])
        end = time_to_minutes(c["end"])

        if (
            day in c["days"].lower()
            and start <= user_minutes < end
        ):

            found = True

            print(
                "Room",
                pretty(c["room"]),
                "-",
                pretty_course(c["course"])
            )

    if not found:
        print("No rooms are being used at that time.")


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
    print("10. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        show_course()

    elif choice == "2":
        classes_today()

    elif choice == "3":
        rooms_in_use_now()

    elif choice == "4":
        free_rooms_now()

    elif choice == "5":
        most_used_rooms()

    elif choice == "6":
        room_schedule()

    elif choice == "7":
        open_times_today()

    elif choice == "8":
        classes_by_day()

    elif choice == "9":
        room_usage_at_time()

    elif choice == "10":
        print("Goodbye")
        break

    else:
        print("Invalid option.")
