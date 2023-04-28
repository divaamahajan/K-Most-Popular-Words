import os 
import logging as log

from multiprocessing import Pool, cpu_count

def read_stop_words(file_path):

    with open(file_path, "r", encoding="utf-8-sig") as sw:

        stop_words = set()

        for line in sw:

            stop_words.update(line.strip().split(","))

        return stop_words
STOP_WORDS = read_stop_words(log.FILE_STOP_WORDS)
def count_words(file_path, chunk_size=None):

    # get the file size

    file_size = os.path.getsize(file_path)

    if not chunk_size:

        chunk_size = file_size // (cpu_count() * 2)

    # create a list of chunks

    chunks = []

    offset = 0

    while offset < file_size:

        chunk_end = min(offset + chunk_size, file_size)

        chunks.append((offset, chunk_end))

        offset = chunk_end

    # process each chunk using multiprocessing Pool

    pool = Pool(processes=cpu_count())

    word_counts = [pool.apply_async(process_chunk, args=(file_path, chunk_start, chunk_size)) for chunk_start, chunk_end in chunks]

    pool.close()

    pool.join()

    # combine the word counts from each chunk

    total_word_count = sum([count.get() for count in word_counts], [])

    # remove stop words from the word count

    total_word_count = [word for word in total_word_count if word not in STOP_WORDS]

    # count the total number of words

    total_count = len(total_word_count)

    return total_count

def process_chunk(file_path, chunk_start, chunk_size):

    with open(file_path, "r") as file:

        file.seek(chunk_start)

        chunk = file.read(chunk_size)

    chunk_word_count = [word for word in chunk.split() if word not in STOP_WORDS]

    return chunk_word_count

if __name__ == '__main__':

    file_path = "/Users/rushshah/SCU/BigData/"
    files = [log.FILENAME_16GB]
    print(f"{files}")
    for f in files:
      total_count= 0
      file= file_path+f
      total_count = count_words(file)
      print(f"Total number of words ({f}):", total_count)
    

      

      

      

    

    
