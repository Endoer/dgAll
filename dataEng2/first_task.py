import numpy as np
import json

matrix = np.load('first_task.npy')

total_sum = np.sum(matrix)
total_avg = np.mean(matrix)
main_diag_sum = np.trace(matrix)
main_diag_avg = main_diag_sum / matrix.shape[0]
side_diag_sum = np.trace(np.fliplr(matrix))
side_diag_avg = side_diag_sum / matrix.shape[0]
max_value = np.max(matrix)
min_value = np.min(matrix)

results = {
    "sum": int(total_sum),
    "avr": int(total_avg),
    "sumMD": int(main_diag_sum),
    "avrMD": int(main_diag_avg),
    "sumSD": int(side_diag_sum),
    "avrSD": int(side_diag_avg),
    "max": int(max_value),
    "min": int(min_value)
}
with open('first_task.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)

print(json.dumps(results, indent=4))
