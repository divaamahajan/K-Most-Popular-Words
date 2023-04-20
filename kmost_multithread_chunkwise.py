import psutil
import time
import re
from collections import Counter
import threading
import os
import datetime

SIZE_5MB  = int(5  * 1024 * 1024 )# 5 MB
SIZE_10MB = int(10 * 1024 * 1024 )# 10 MB
SIZE_20MB = int(20 * 1024 * 1024 )# 20 MB
SIZE_40MB = int(40 * 1024 * 1024 )# 40 MB

FILENAME_50MB = "small_50MB_dataset.txt"
FILENAME_300MB = "data_300MB.txt"
FILENAME_2_5GB = "data_2.5GB.txt"
FILENAME_16GB = "data_16GB.txt"
FILE_STOP_WORDS = "stop_words.txt"

size_dict = {None: "None. Full file is being read at once" ,SIZE_5MB: '5MB', SIZE_10MB: '10MB', SIZE_20MB: '20MB', SIZE_40MB: '40MB'}

word_results = ""

def generate_logs(result):
    current_file = os.path.basename(__file__).split(".")[0]
    direc = os.getcwd()
    log_file = "log_" + current_file + ".txt"
    with open(os.path.join(direc,log_file), 'a') as logs:
        logs.write(result)
        print(f"\nLogs appended")

def read_stop_words(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as sw:
        stop_words = set()
        for line in sw:
            stop_words.update(line.strip().split(","))
        return stop_words

def read_chunk(file_path, chunk_start, chunk_size):
    with open(file_path, "r") as file:
        file.seek(chunk_start)
        chunk = file.read(chunk_size)
    return chunk

def process_chunk(chunk, stop_words):
    word_counts = Counter()
    for line in chunk.splitlines():
        for word in re.findall(r"\w+", line.lower()):
            if word and word not in stop_words:
                word_counts[word] += 1
    return word_counts

def print_top_words(word_counts, k):
    global word_results
    # get the top k words from the Counter
    top_words = word_counts.most_common(k)

    # print the top k words
    # print(f"\nTop {k} frequent words:")
    # print("Word".ljust(20) + "Count")
    # for word, count in top_words:
    #     print("{:<20} {}".format(word, count))
    word_results += "\n\nTop frequent words:"
    word_results += "\n\nWord".ljust(21) + "Count"
    for word, count in top_words:
        word_results += "\n{:<20} {}".format(word, count)


def print_statistics(filename, start_time):
    # calculate the running time
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


def process_data(filename, stop_words, k, chunk_size=None):
    global word_results
    word_results += f"\n\n***************** Chunk Size : {size_dict[chunk_size]} ******************* \n"
    start_time = time.time()

    # get the file size
    file_size = os.path.getsize(filename)

    # create a list of chunks
    chunks = []
    offset = 0
    while offset < file_size:
        chunk_end = min(offset + chunk_size, file_size)
        chunks.append((offset, chunk_end))
        offset = chunk_end

    # process each chunk in a separate thread
    threads = []
    word_counts = Counter()
    for chunk_start, chunk_end in chunks:
        chunk_thread = threading.Thread(target=lambda: word_counts.update(process_chunk(read_chunk(filename, chunk_start, chunk_size), stop_words)))
        chunk_thread.start()
        threads.append(chunk_thread)

    # wait for all threads to finish
    for thread in threads:
        thread.join()
    
    # print the top k frequent words
    print_top_words(word_counts, k)

    # print the performance statistics
    print_statistics(filename, start_time)



def main():
    # set the number of top words to find
    k = int(input("Enter the number of top words to find: "))
    filename = FILENAME_50MB

    # read stop words
    stop_words = read_stop_words(FILE_STOP_WORDS)

    # process the file in chunks of 5MB
    process_data(filename, stop_words, k, chunk_size=SIZE_5MB)

    # # process the file in chunks of 10MB
    process_data(filename, stop_words, k, chunk_size=SIZE_10MB)

    # # process the file in chunks of 20MB
    process_data(filename, stop_words, k, chunk_size=SIZE_20MB)

    # # process the file in chunks of 40MB
    process_data(filename, stop_words, k, chunk_size=SIZE_40MB)


if __name__ == '__main__':
    main()
