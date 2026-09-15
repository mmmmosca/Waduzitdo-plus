import sys

from asteval import Interpreter


variables = {}
aeval = Interpreter(usersyms=variables)

labels = {}

operators = [
    "+", "-", "*", "/", "%", "(", ")",
    "==", "!=", "<=", ">=", "<", ">",
    "and", "or", "not"
]

with open(sys.argv[1], "r") as file:
    source = file.readlines()

lines = []

for line in source:
    if not line.strip():
        continue

    try:
        command, arg = line.split(':', 1)
    except ValueError:
        continue

    command = command.strip().lower()
    arg = arg.strip()
    lines.append((command, arg))


for line_counter, (command, arg) in enumerate(lines):
    if command == 'l':
        labels[arg] = line_counter

var_name = ""
var_value = 0
line_counter = 0

while line_counter < len(lines):

    command, arg = lines[line_counter]

    if command == 't':

        if arg in variables:
            print(variables[arg])

        elif arg.startswith('"') and arg.endswith('"'):
            print(arg[1:-1])

        elif any(char in arg for char in "+-*/%()"):
            print(aeval(arg))

        else:
            print("Invalid T: command argument")


    elif command == 'o':

        if arg in variables:
            print(variables[arg], end='')

        elif arg.startswith('"') and arg.endswith('"'):
            print(arg[1:-1], end='')

        elif any(char in arg for char in "+-*/%()"):
            print(aeval(arg), end='')

        else:
            print("Invalid O: command argument")


    elif command == 'j':

        if arg in labels:
            line_counter = labels[arg]
            continue


    elif command == 'm':

        result = 0

        if any(op in arg for op in operators):
            result = aeval(arg)

        if result:
            line_counter += 1
            continue
        else:
            line_counter += 2
            continue


    elif command == 'd':

        var_name = arg


    elif command == 'i':

        if arg.lower() == 'a':
            var_value = input()
            if var_value.isdigit():
                var_value = int(var_value)

        elif arg.isdigit():
            var_value = int(arg)

        elif arg.startswith('"') and arg.endswith('"'):
            var_value = arg[1:-1]

        elif any(char in arg for char in "+-*/%()"):
            var_value = aeval(arg)

        else:
            var_value = arg

        variables[var_name] = var_value
        aeval.symtable[var_name] = var_value

        var_name = ""
        var_value = 0


    elif command == 's':
        sys.exit(0)


    line_counter += 1
