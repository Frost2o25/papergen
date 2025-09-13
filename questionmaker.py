import re
import os
import random

# -----------------------------
# File paths
# -----------------------------
counter_file = "counter.txt"  # Stores the current function count
target_file = "/home/yash/Projects/tpm/newtpm/new/new1.py"  # File where new functions are inserted


# -----------------------------
# Load / initialize counter
# -----------------------------
if os.path.exists(counter_file):
    with open(counter_file, "r") as f:
        # Read previous count (default to 0 if empty)
        count = int(f.read().strip() or 0)
else:
    count = 0


# -----------------------------
# Helper: generate next label
# Produces "A", "B", ..., "Z", "AA", ...
# -----------------------------
def next_label(label: str) -> str:
    if not label:
        return "A"
    label = list(label.upper())
    i = len(label) - 1
    while i >= 0:
        if label[i] == "Z":
            label[i] = "A"
            i -= 1
        else:
            label[i] = chr(ord(label[i]) + 1)
            return "".join(label)
    return "A" * (len(label) + 1)


# -----------------------------
# Question template setup
# -----------------------------
question = "find c in 10^2 + 15^2 = z^2"  # Base string to convert into function
exception = (2,)                          # Numbers to exclude from randomization
lr, ur = 10, 20                           # Random range (lower, upper)
label = ""


# -----------------------------
# Build new function dynamically
# -----------------------------
# Function header
new_line = f"def qestion{count}():\n\n"

# Assign random values to numeric tokens (except exceptions)
number_re = re.compile(r"\b\d+\b")
for match in number_re.findall(question):
    if match.isnumeric() and int(match) not in exception:
        label = next_label(label)
        new_line += f"\t{label} = random.randint({lr}, {ur})\n\n"

# Build the question string (mix of constants + variables)
new_line += "\tq = f\""
label = ""
for token in re.findall(r"\d+|[a-zA-Z]+|\S", question):
    if token.isnumeric() and int(token) not in exception:
        label = next_label(label)
        new_line += f"{{{label}}} "
    else:
        new_line += token + " "
# Finish string + add return
new_line = new_line.strip() + "\".format(" + ", ".join(
    [chr(c) for c in range(ord("A"), ord("A") + len(set(re.findall(r"\d+", question)))) if chr(c) <= label]
) + ")\n\treturn q\n\n"


# -----------------------------
# Insert function into target file
# -----------------------------
with open(target_file, "r+") as f:
    lines = f.readlines()
    lines.insert(15, new_line)  # Insert function at line 15
    f.seek(0)
    f.writelines(lines)
    f.truncate()


# -----------------------------
# Update counter for next run
# -----------------------------
count += 1
with open(counter_file, "w") as f:
    f.write(str(count))


# -----------------------------
# Patch last line of target file
# Adds a call to the new function
# -----------------------------
with open(target_file, "r+") as f:
    lines = f.readlines()
    if not lines:
        raise ValueError("File is empty!")

    last_line = lines[-2]  # Take 2nd-to-last line
    if len(last_line) < 16:
        raise ValueError("Last line has fewer than 16 characters.")

    # Insert function call into the line
    lines[-2] = last_line[:15] + f"qestion{count-1}(), " + last_line[15:]
    f.seek(0)
    f.writelines(lines)
    f.truncate()
