import sys

input_path = sys.argv[1]
output_path = sys.argv[2]
file = open(input_path, "r")
lines = file.readlines()
file.close()
file = open(output_path, "w")
epoch_cnt = 0
for i in range(len(lines)):
    line = lines[i]
    line = line.strip()
    line = line.split(" ")
    if line[0] == 'Averaged' and line[1] == 'stats:' and line[2] == 'class_error:':
        file.write("Epoch " + str(epoch_cnt) + "\n")
        for j in range(16):
            file.write(lines[i + j])
        epoch_cnt += 1
file.close()

