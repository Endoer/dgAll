from collections import Counter

input_filepath = 'first_task.txt'
output_freq_filepath = 'outputFreq1.txt'
output_avg_filepath = 'output_avg1.txt'

def count_words(input_filepath, output_filepath):
    with open(input_filepath, 'r') as input_file:
        text = input_file.read()
        words = text.split()
        freq = Counter(words)
        with open(output_filepath, 'w') as output_file:
            for word, count in freq.most_common():
                output_file.write(f'{word}:{count}\n')

def avg_words(input_filepath, output_filepath):
    with open(input_filepath, 'r') as input_file:
        text = input_file.read()
        words = text.split()
        sentences = text.split('.')
        avg = len(words) / len(sentences)
        with open(output_filepath, 'w') as output_file:
            output_file.write(f'{avg}\n')

count_words(input_filepath, output_freq_filepath)
avg_words(input_filepath, output_avg_filepath)