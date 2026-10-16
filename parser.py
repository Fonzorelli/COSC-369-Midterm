import re

def clean(text):
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

with open("faculty.txt", "r") as infile:
    with open("knowledge.pl", "w") as outfile:
        outfile.write(":- discontiguous professor/1.\n")
        outfile.write(":- discontiguous department/2.\n")
        outfile.write(":- discontiguous teaches/2.\n\n")

        for line in infile:
            line = line.strip()

            if not line:
                continue

            parts = line.split("|")

            if len(parts) != 3:
                continue

            professor = clean(parts[0])
            department = clean(parts[1])
            courses = parts[2].split(",")

            outfile.write(f"professor({professor}).\n")
            outfile.write(f"department({professor}, {department}).\n")

            for course in courses:
                course = clean(course)
                outfile.write(f"teaches({professor}, {course}).\n")

print("knowledge.pl created")
