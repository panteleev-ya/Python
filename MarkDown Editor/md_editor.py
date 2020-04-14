file_in = input("Input file name: ")
file_out = input("Output file name: ")
command = input("Command: ")

input_file = open("input.txt", "r")
output_file = open("output.txt", "w")

if command == "1":
    for line in input_file.readlines():
        new_line = ""
        for i in range(len(line)):
            if line[i] == '[':
                new_line += '('

            elif line[i] == ']':
                new_line += ')'

            elif line[i] == '(':
                new_line += '['

            elif line[i] == ')':
                new_line += ']'
            else:
                new_line += line[i]
        output_file.write(new_line)
    print("All brakes was changed to similar!")
input_file.close()
output_file.close()
