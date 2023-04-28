# A program to find k most frequent words in a file
import heapq
import re
import time
import os
from collections import defaultdict
from multiprocessing import Pool, cpu_count
import logging as log

# Define function to read stop words from a file
def read_stop_words(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as sw:
        stop_words = set()
        for line in sw:
            # Add words in each line of the file as a set to the stop_words set
            stop_words.update(line.strip().split(","))
        # Return the set of stop words
        return stop_words


def process_chunk(args):
    chunk, stop_words = args
    word_counts = defaultdict(int)
    for line in chunk.splitlines():
        for word in re.findall(r"\w+", line.lower()):
            if word and word not in stop_words:
                word_counts[word] += 1
    return word_counts


def process_data(filename, stop_words, top_k, chunk_size=None):

    print_size = log.size_dict[chunk_size]

    # get the file size
    file_name = f"/Users/rushshah/SCU/BigData/" + filename
    file_size = os.path.getsize(file_name)
    file_size_MB = file_size / (1024 * 1024)
    file_size_GB = file_size / (1024 * 1024 * 1024)

    if not chunk_size:
        chunk_size = file_size // (cpu_count() * 2)
        # Convert chunk_size to MB and GB
        chunk_size_MB = chunk_size / (1024 * 1024)
        chunk_size_GB = chunk_size / (1024 * 1024 * 1024)
        print_size = f"{chunk_size_MB:.2f} MB or {chunk_size_GB:.2f} GB Decided by CPU \n\t file size {file_size_MB:.2f} MB or {file_size_GB:.2f} GB /( CPU count {cpu_count()} * 2)"

    start_time = time.time()

    # create a list of chunks
    chunks = []
    offset = 0

    while offset < file_size:
        chunk_end = min(offset + chunk_size, file_size)
        chunks.append((offset, chunk_end))
        offset = chunk_end

    # process each chunk using multiprocessing Pool
    pool = Pool(processes=cpu_count())
    word_counts = defaultdict(int)
    for chunk_word_counts in pool.imap_unordered(process_chunk, [(read_chunk(file_name, chunk_start, chunk_size), stop_words) for chunk_start, chunk_end in chunks]):
        for word, count in chunk_word_counts.items():
            word_counts[word] += count
    
    word_counts =  heapq.nlargest(top_k, word_counts.items(), key=lambda x: x[1])


    current_file = os.path.basename(__file__).split(".")[0]
    
    # print the top k frequent words
    log.get_top_words_heapq(word_counts, top_k)

    # print the performance statistics
    log.print_statistics(current_file, filename, start_time, file_size_GB, print_size, top_k)


def read_chunk(file_path, chunk_start, chunk_size):
    with open(file_path, "r") as file:
        file.seek(chunk_start)
        chunk = file.read(chunk_size)
    return chunk
 
# Driver program to test above functions
def main():
    # set the number of top words to find
    k = int(input("Enter the number of top words to find: "))
    filename = log.FILENAME_16GB
    # read stop words from file
    stop_words = read_stop_words(log.FILE_STOP_WORDS)



if __name__ == '__main__':
    main()
