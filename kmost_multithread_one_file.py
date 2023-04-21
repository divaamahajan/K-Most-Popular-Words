import psutil
import time
import re
from collections import Counter
import threading
import sys
import os
import datetime

FILENAME_50MB = "small_50MB_dataset.txt"
FILENAME_300MB = "data_300MB.txt"
FILENAME_2_5GB = "data_2.5GB.txt"
FILENAME_16GB = "data_16GB.txt"
FILE_STOP_WORDS = "stop_words.txt"

stop_words = set()
lock = threading.Lock()
word_counts = Counter()
word_results = ""

def generate_logs(result):
    current_file = os.path.basename(__file__).split(".")[0]
    direc = os.getcwd()
    log_file = "log_" + current_file + ".txt"
    with open(os.path.join(direc,log_file), 'a') as logs:
        logs.write(result)
        print(f"\nLogs appended")

size_dict = {None: "None. Full file is being read at once"}

def read_stop_words(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as sw:
        global stop_words
        for line in sw:
            stop_words.update(line.strip().split(","))
        return stop_words

def count_words(line,stop_words):
    global word_counts
    global lock
    try:
        for word in re.findall(r"\w+", line.lower()):
            if word and word not in stop_words:
                with lock:
                    word_counts[word] += 1
    except Exception as e:
        print(type(line))
        print(f"\n{line}")
        sys.exit()


def read_datafile(file_name, stop_words, chunk_size=None):
    threads = []
    file_path = "/Users/rushshah/SCU/BigData/" + file_name
    with open(file_path, "r") as file:
        for line in file:
            thread = threading.Thread(target=count_words, args=(line,stop_words,))
            threads.append(thread)
            thread.start()
    
    for th in threads:
        th.join()
    return word_counts

# def count_words(file_path, stop_words, chunk_size=None):
#     return 

def print_top_words(word_counts, k):
    global word_results
    # get the top k words from the Counter
    top_words = word_counts.most_common(k)

    word_results += "\n\nTop frequent words:"
    word_results += "\n\nWord".ljust(21) + "Count"
    for word, count in top_words:
        word_results += "\n{:<20} {}".format(word, count)


def print_statistics(filename, start_time):
    # # calculate the running time
    # end_time = time.time()
    # running_time = end_time - start_time

    # # print the performance metrics
    # process = psutil.Process()
    # memory_usage = process.memory_info().rss
    # cpu_utilization = process.cpu_percent()
    # print(f"\n\nRunning time: {running_time:.2f} seconds")
    # print(f"\nMemory usage: {memory_usage / 1024 / 1024:.2f} MB")
    # print(f"\nCPU utilization: {cpu_utilization:.2f}%")
    # print("------\n")

    global word_results
    # calculate the running time
    end_time = time.time()
    running_time = end_time - start_time

    # print the performance metrics
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    cpu_utilization = process.cpu_percent()
    # file_size = filename.split("_")[-1]
    results = f"**************************************************************\
                \nOutput logs\
                \nFile name:\t{filename}\
                \nDate:\t\t{datetime.datetime.now()}\
                \n**************************************************************\n"
    results += word_results
    results += f"\n\n**************************************************************"
    results += f"\n\nRunning time:\t\t{running_time:.2f} seconds\
                \nMemory usage:\t\t{memory_usage / 1024 / 1024:.2f} MB\
                \nCPU utilization:\t{cpu_utilization:.2f} %\n"
    results += f'\n************************** END *******************************\n\n'
    print(f"{results}")
    generate_logs(results)


def process_data(filename, stop_words,top_k, chunk_size=None,):
    print(f"\n\n******Chunk Size : {size_dict[chunk_size]} ********** \n")
    start_time = time.time()

    # count words from data file
    word_counts = read_datafile(filename, stop_words, chunk_size)

    # print the top k words
    print_top_words(word_counts, top_k)

    # print the performance metrics
    print_statistics(filename, start_time)


def main():
    # set the number of top words to find
    k = int(input("Enter the number of top words to find: "))
    # read stop words from file
    stop_words = read_stop_words("stop_words.txt")

    # start the timer
    # global start_time
    # process the data with different chunk sizes
    process_data(FILENAME_300MB, stop_words, k)



if __name__ == '__main__':
    main()
