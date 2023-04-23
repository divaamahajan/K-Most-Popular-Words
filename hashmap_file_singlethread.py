import time
import re
import logging as log
import os

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


def main():
    # set the number of top words to find
    k = int(input("Enter the number of top words to find: "))
    filename = log.FILENAME_50MB

    # get the file size
    file_name = filename
    file_size = os.path.getsize(file_name)
    file_size_GB = file_size / (1024 * 1024 * 1024)
    
    # read stop words from file
    stop_words = read_stop_words(log.FILE_STOP_WORDS)
    start_time = time.time()

    # count words from data file
    word_counts = read_datafile(filename, stop_words)

    current_file = os.path.basename(__file__).split(".")[0]
    
    # print the top k frequent words
    log.get_top_words_hashmap(word_counts, k)

    # print the performance statistics
    log.print_statistics(current_file, filename, start_time, file_size_GB, None, k)

if __name__ == '__main__':
    main()
