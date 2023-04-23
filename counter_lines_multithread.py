import time
import re
from collections import Counter
import threading
import sys
import os
import logging as log

stop_words = set()
lock = threading.Lock()

def read_stop_words(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as sw:
        global stop_words
        for line in sw:
            stop_words.update(line.strip().split(","))
        return stop_words

def count_words(line, stop_words):
    local_counts = getattr(threading.current_thread(), 'counts', None)
    if local_counts is None:
        local_counts = Counter()
        setattr(threading.current_thread(), 'counts', local_counts)
    try:
        for word in re.findall(r"\w+", line.lower()):
            if word and word not in stop_words:
                local_counts[word] += 1
    except Exception as e:
        print(type(line))
        print(f"\n{line}")
        sys.exit()


def read_datafile(file_name, stop_words):
    threads = []
    file_path = file_name
    with open(file_path, "r") as file:
        for line in file:
            thread = threading.Thread(target=count_words, args=(line,stop_words,))
            threads.append(thread)
            thread.start()
    
    for th in threads:
        th.join()

def process_data(filename, stop_words,top_k):
    # get the file size
    file_name = filename
    file_size = os.path.getsize(file_name)
    file_size_GB = file_size / (1024 * 1024 * 1024)
    start_time = time.time()

    # count words from data file
    global_counts = Counter()
    read_datafile(filename, stop_words)
    for local_counts in map(lambda t: getattr(t, 'counts', None), threading.enumerate()):
        if local_counts:
            global_counts.update(local_counts)
    
    current_file = os.path.basename(__file__).split(".")[0]

    # print the top k frequent words
    log.get_top_words_counter(global_counts, top_k)

    # print the performance statistics
    log.print_statistics(current_file, filename, start_time, file_size_GB, None, top_k)


def main():
    # set the number of top words to find
    k = int(input("Enter the number of top words to find: "))
    filename = log.FILENAME_50MB
    # read stop words from file
    stop_words = read_stop_words("stop_words.txt")

    process_data(filename,stop_words,k)


if __name__ == '__main__':
    main()
