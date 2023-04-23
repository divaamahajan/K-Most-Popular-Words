import os
import psutil
import time
import datetime
import csv

SIZE_5MB  = int(5  * 1024 * 1024 )# 5 MB
SIZE_10MB = int(10 * 1024 * 1024 )# 10 MB
SIZE_20MB = int(20 * 1024 * 1024 )# 20 MB
SIZE_40MB = int(40 * 1024 * 1024 )# 40 MB
SIZE_100MB = int(100 * 1024 * 1024 )# 100 MB

FILENAME_50MB = "small_50MB_dataset.txt"
FILENAME_300MB = "data_300MB.txt"
FILENAME_2_5GB = "data_2.5GB.txt"
FILENAME_16GB = "data_16GB.txt"
FILE_STOP_WORDS = "stop_words.txt"

size_dict = {None: "None. Full file is being read at once" ,
             SIZE_5MB: '5 MB', 
             SIZE_10MB: '10 MB', 
             SIZE_20MB: '20 MB', 
             SIZE_40MB: '40 MB',
             SIZE_100MB: '100 MB'}

word_results = ""

def generate_logs(result, current_file):
    logs_folder = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    log_file = os.path.join(logs_folder, f"log_{current_file}.txt")
    with open(log_file, 'a') as logs:
        logs.write(result)
        print(f"\nLogs appended")

def get_top_words_counter(word_counts, k):
    global word_results
    # get the top k words from the Counter
    top_words = word_counts.most_common(k)
    print_top_words(top_words)

def get_top_words_hashmap(word_counts, k):
    # get the top k words from the dictionary
    top_words = sorted(word_counts, key=word_counts.get, reverse=True)[:k]
    global word_results
    word_results += "\n\nTop frequent words:"
    word_results += "\n\nWord".ljust(21) + "Count"
    for word in top_words:
        count = word_counts[word]
        word_results += "\n{:<20} {}".format(word, count)

def get_top_words_defaultdict(word_counts, k):
    # get the top k words from the defaultdict
    top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:k]
    print_top_words(top_words)


def get_top_words_heapq(top_words, top_k):
    print_top_words(top_words)

def print_top_words(top_words):
    global word_results
    word_results += "\n\nTop frequent words:"
    word_results += "\n\nWord".ljust(21) + "Count"
    for word, count in top_words:
        word_results += "\n{:<20} {}".format(word, count)

def print_statistics(current_file, filename, start_time, file_size, chunk_size, top_k):
    global word_results
    # calculate the running time
    end_time = time.time()
    running_time = end_time - start_time

    # print the performance metrics
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss
    cpu_utilization = psutil.cpu_percent(interval=running_time)

    
    # file_size = filename.split("_")[-1]
    results = f"**************************************************************\
                \nOutput logs\
                \nDate:\t\t{datetime.datetime.now()}\
                \n**************************************************************\n"
    results += word_results
    results += f"\n\n-------------------------------------------------------------"
    results += f"\n\nFile name:\t\t{filename}\
                \nFile Size: \t\t{file_size:.2f} GB\
                \nChunk Size: \t\t{chunk_size}\
                \nRunning time:\t\t{running_time:.2f} seconds\
                \nMemory usage:\t\t{memory_usage / 1024 / 1024:.2f} MB\
                \nCPU utilization:\t{cpu_utilization:.2f} %\n"

    results += f'\n************************** END *******************************\n\n'
    print(f"{results}")
    generate_logs(results, current_file)
    log_csv(top_k, current_file, filename, file_size, chunk_size, running_time, memory_usage, cpu_utilization)

def log_csv(top_k, current_file, filename, file_size, chunk_size, running_time, memory_usage, cpu_utilization):
    logs_folder = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    csv_file = os.path.join(logs_folder, "logs.csv")
    if chunk_size: chunk = chunk_size.split(' ')[0]
    else: chunk = None
    headers = ['Top k','Data Structure', 'File division', 'Algorithm Approach', 'Filename','File Size (GB)', 'Chunk Size (MB)', 'Running time (seconds)', 'Memory usage (MB)', 'CPU utilization %']
    values = [top_k, current_file.split('_')[0], current_file.split('_')[1], current_file.split('_')[2],filename ,f"{file_size:.2f}", chunk, f"{running_time:.2f}", f"{memory_usage/ 1024 / 1024:.2f}", f"{cpu_utilization:.2f}"]
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(values)
    print("\nLogs appended to logs.csv")