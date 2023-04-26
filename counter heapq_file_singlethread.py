import heapq
import time
import re
import os
from collections import Counter
import logging as log

def read_stop_words(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as sw:
        stop_words = set()
        for line in sw:
            # Add words in each line of the file as a set to the stop_words set
            stop_words.update(line.strip().split(","))
        # Return the set of stop words
        return stop_words

# Define function to read a data file and return the top k words in it
def read_datafile(filename, stop_words, top_k):
    # Create a Counter object to count the frequency of words
    word_counts = Counter()

    # get the file size
    file_name = filename
    file_size = os.path.getsize(file_name)
    file_size_GB = file_size / (1024 * 1024 * 1024)
    
    start_time = time.time()

    with open(filename, "r", encoding="utf-8-sig") as f:
        for line in f:
            # Iterate over each line in the file
            for word in re.findall(r"\w+", line.lower()):
                if word not in stop_words:
                    # If word is not in the set of stop words, increment its count
                    word_counts[word] += 1

    # Return the k words with highest frequency in the Counter object
    word_counts = heapq.nlargest(top_k, word_counts.items(), key=lambda x: x[1])

    current_file = os.path.basename(__file__).split(".")[0]
    
    # print the top k frequent words
    log.get_top_words_heapq(word_counts, top_k)

    # print the performance statistics
    log.print_statistics(current_file, filename, start_time, file_size_GB, None, top_k)


# Driver program to test above functions
def main():
    # set the number of top words to find
    k = int(input("Enter the number of top words to find: "))
    filename = log.FILENAME_50MB
    # read stop words from file
    stop_words = read_stop_words(log.FILE_STOP_WORDS)
    read_datafile(filename, stop_words, k)


if __name__ == '__main__':
    main()
