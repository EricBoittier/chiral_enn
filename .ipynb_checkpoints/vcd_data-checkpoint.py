import os
import csv

START = 1
END   = 5000
OUTPUT = "vcd_resultsR.csv"

with open(OUTPUT, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["file", "mode_index", "vcd"])

    for i in range(START, END + 1):
        filename = f"com{i}R.out"
        if not os.path.isfile(filename):
            continue

        mode_counter = 0

        with open(filename) as f:
            for line in f:
                if line.strip().startswith("Rot. str."):
                    values = [float(x) for x in line.split()[3:]]
                    for v in values:
                        mode_counter += 1
                        writer.writerow([filename, mode_counter, v])
