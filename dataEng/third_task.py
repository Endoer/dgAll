def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip().split() for line in lines]

def replace_na_with_mean(row):
    for i in range(len(row)):
        if row[i] == 'N/A':
            if i == 0:
                row[i] = row[i + 1]
            elif i == len(row) - 1:
                row[i] = row[i - 1]
            else:
                row[i] = (float(row[i - 1]) + float(row[i + 1])) / 2
    return row

def filter_positive_even(row):
    return [float(x) for x in row if float(x) > 0 and float(x) % 2 == 0]

def calculate_mean(row):
    if not row:
        return 0
    return sum(row) / len(row)

input_file_path = 'third_task.txt'
output_file_path = 'output3.txt'

data = read_file(input_file_path)
results = []

for row in data:

    row = replace_na_with_mean(row)

    filtered_row = filter_positive_even(row)

    mean = calculate_mean(filtered_row)
    results.append(mean)

with open(output_file_path, 'w') as file:
    for i, mean in enumerate(results):
        file.write(f"{i+1}:{mean}\n")

