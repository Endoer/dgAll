import pandas as pd

input_file_path = 'fourth_task.txt'
output_file_path = 'output4.csv'
stats_file_path = 'stats4.txt'
def process_csv(input_file_path, output_file_path, stats_file_path):

    df = pd.read_csv(input_file_path)
    df = df.drop(columns=['status'])

    mean_price = df['price'].mean()
    max_price = df['price'].max()
    min_price = df['price'].min()

    filtered_df = df[df['quantity'] < 97]

    with open(stats_file_path, 'w') as stats_file:
        stats_file.write(f"Mean Price: {mean_price}\n")
        stats_file.write(f"Max Price: {max_price}\n")
        stats_file.write(f"Min Price: {min_price}\n")

    filtered_df.to_csv(output_file_path, index=False)

    print(f"Results have been written to {output_file_path} and {stats_file_path}")

process_csv(input_file_path, output_file_path, stats_file_path)