# A program to find k most frequent words in a file
import heapq
import re
import sys
import time
import psutil

from collections import Counter

FILENAME_50MB = "small_50MB_dataset.txt"
FILENAME_300MB = "data_300MB.txt"
FILENAME_2_5GB = "data_2.5GB.txt"
FILENAME_16GB = "data_16GB.txt"
FILE_STOP_WORDS = "stop_words.txt"# Define function to read stop words from a file
def read_stop_words(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as sw:
        stop_words = set()
        for line in sw:
            # Add words in each line of the file as a set to the stop_words set
            stop_words.update(line.strip().split(","))
        # Return the set of stop words
        return stop_words

# Define function to read a data file and return the top k words in it
def read_datafile(filename, stop_words, k):
    # Create a Counter object to count the frequency of words
    word_counts = Counter()
    with open(filename, "r", encoding="utf-8-sig") as f:
        for line in f:
            # Iterate over each line in the file
            for word in re.findall(r"\w+", line.lower()):
                if word not in stop_words:
                    # If word is not in the set of stop words, increment its count
                    word_counts[word] += 1

    # Return the k words with highest frequency in the Counter object
    return heapq.nlargest(k, word_counts.items(), key=lambda x: x[1])

# Define function to print the top words and their frequency
def print_top_words(word_counts):
    # Print the header for the top frequent words list
    print("\nTop frequent words:")
    print("Word".ljust(20) + "Count")
    # Iterate over each word and its count in the word_counts list and print them
    for word, count in word_counts:
        print("{:<20} {}".format(word, count))


def print_statistics(start_time):
    # calculate the running time
    end_time = time.time()
    running_time = end_time - start_time

    # print the performance metrics
    memory_usage = sys.getsizeof(heapq)
    cpu_utilization = psutil.cpu_percent()
    print(f"\n\nRunning time: {running_time:.2f} seconds")
    print(f"\nMemory usage: {memory_usage / 1024 / 1024:.2f} MB")
    print(f"\nCPU utilization: {cpu_utilization:.2f}%")
    print("------\n")


# Driver program to test above functions
def main():
    # set the number of top words to find
    k = int(input("Enter the number of top words to find: "))
    filename = FILENAME_50MB
    # read stop words from file
    stop_words = read_stop_words(FILE_STOP_WORDS)

    start_time = time.time()

    most_frequent_words = read_datafile(filename, stop_words, k)
    print(type(most_frequent_words))
    print_top_words(most_frequent_words)
    print_statistics(start_time)


if __name__ == '__main__':
    main()