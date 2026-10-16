import re

def clean(text):
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = text.strip('_')

    if text and text[0].isdigit():
        text = "v_" + text

    return text

with open("class_schedule.txt", "r") as infile:
    with open("schedule.pl", "w") as outfile:

        outfile.write(":- discontiguous course/1.\n")
        outfile.write(":- discontiguous course_name/2.\n")
        outfile.write(":- discontiguous days/2.\n")
        outfile.write(":- discontiguous start_time/2.\n")
        outfile.write(":- discontiguous end_time/2.\n")
        outfile.write(":- discontiguous room/2.\n")
        outfile.write(":- discontiguous professor_for/2.\n\n")

        for line in infile:
            line = line.strip()

            if not line:
                continue

            parts = line.split("|")

            if len(parts) != 7:
                continue

            code = clean(parts[0])
            name = clean(parts[1])
            days = clean(parts[2])
            start = clean(parts[3])
            end = clean(parts[4])
            room = clean(parts[5])
            professor = clean(parts[6])

            outfile.write(f"course({code}).\n")
            outfile.write(f"course_name({code}, {name}).\n")
            outfile.write(f"days({code}, {days}).\n")
            outfile.write(f"start_time({code}, {start}).\n")
            outfile.write(f"end_time({code}, {end}).\n")
            outfile.write(f"room({code}, {room}).\n")
            outfile.write(f"professor_for({code}, {professor}).\n")

print("schedule.pl created")
