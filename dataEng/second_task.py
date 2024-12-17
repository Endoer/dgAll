import math

input_filepath = 'second_task.txt'

def sum_of_square_roots(raw):
    total_sum = 0
    for num in raw.split(' '):
        if int(num) > 0:
            root = math.sqrt(int(num))
            rounded_root = root
            total_sum += rounded_root
    return round(total_sum)

with open(input_filepath, 'r') as input_file:
    text = input_file.read()
    raw = text.split('\n')
    results = []
    for i in raw:
            results.append(sum_of_square_roots(i))
    results.sort(reverse=True)
    k=0
    with open('output2.txt', 'w') as output_file:
        while k < 10:
             output_file.write(f'{results[k]}\n')
             k+=1
