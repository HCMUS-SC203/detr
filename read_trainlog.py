import sys

input_path = sys.argv[1]
output_path = sys.argv[2]
file = open(input_path, "r")
lines = file.readlines()
file.close()
file = open(output_path, "w")
epoch_cnt = 34
for i in range(len(lines)):
    line = lines[i]
    line = line.strip()
    line = line.split(" ")
    if line[0] == 'Averaged' and line[1] == 'stats:' and line[2] == 'class_error:':
        file.write("Epoch " + str(epoch_cnt).zfill(2) + ":\n\n")
        for j in range(2, 16):
            file.write(lines[i + j][j >= 4:])
        epoch_cnt += 1
        if i + 1 < len(lines):
            file.write("\n")
file.close()

