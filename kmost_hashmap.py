import psutil
import time
import re

SIZE_5MB  = int(5  * 1024 * 1024 )# 5 MB
SIZE_10MB = int(10 * 1024 * 1024 )# 10 MB
SIZE_20MB = int(20 * 1024 * 1024 )# 20 MB
SIZE_40MB = int(40 * 1024 * 1024 )# 40 MB

FILENAME_50MB = "small_50MB_dataset.txt"
FILENAME_300MB = "data_300MB.txt"
FILENAME_2_5GB = "data_2.5GB.txt"
FILENAME_16GB = "data_16GB.txt"
FILE_STOP_WORDS = "stop_words.txt"

def read_stop_words(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as sw:

        stop_words = set()
        for line in sw:
            stop_words.update(line.strip().split(","))
        return stop_words


def read_datafile(file_path, stop_words):
    word_counts = dict()
    with open(file_path, "r", encoding="utf-8-sig") as file:
        for line in file:
            for word in re.findall(r"\w+", line.lower()):
                if word and word not in stop_words:
                    word_counts[word] = word_counts.get(word,0) + 1
    return word_counts


def print_top_words(word_counts, k):
    # get the top k words from the dictionary
    top_words = sorted(word_counts, key=word_counts.get, reverse=True)[:k]
    
    # print the top k words
    print("\nTop frequent words:")
    print("Word".ljust(20) + "Count")
    for word in top_words:
        count = word_counts[word]
        print("{:<20} {}".format(word, count))



def print_statistics(start_time):
    # calculate the running time
    end_time = time.time()
    running_time = end_time - start_time

    # print the performance metrics
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    cpu_utilization = process.cpu_percent()
    print(f"\n\nRunning time: {running_time:.2f} seconds")
    print(f"\nMemory usage: {memory_usage / 1024 / 1024:.2f} MB")
    print(f"\nCPU utilization: {cpu_utilization:.2f}%")
    print("------\n")
    
def main():
    # set the number of top words to find
    k = int(input("Enter the number of top words to find: "))
    filename = FILENAME_50MB
    # read stop words from file
    stop_words = read_stop_words(FILE_STOP_WORDS)
    start_time = time.time()

    # count words from data file
    word_counts = read_datafile(filename, stop_words)

    # print the top k words
    print_top_words(word_counts, k)

    # print the performance metrics
    print_statistics(start_time)

if __name__ == '__main__':
    main()
