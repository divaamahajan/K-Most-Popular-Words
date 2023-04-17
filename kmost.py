import string
import heapq
import psutil
import time
import urllib.request
import zipfile
import os

# set the path to the directory where zip files are stored
dir_path = "./"
zip_files = ['data_300MB.txt', 'data_2.5GB.txt', 'data_16GB.txt']

# download the zip file
url = 'https://drive.google.com/u/0/uc?id=1kaVM15rD9_O9HsvzrUKkIZ4R6ETUAdo4&export=download'
zipname = 'data.zip'
urllib.request.urlretrieve(url, zipname)


# extract the files from the zip file
with zipfile.ZipFile(zipname, 'r') as zip_ref:
    zip_ref.extractall(dir_path)

# set the number of top words to find
k = int(input("Enter the number of top words to find: "))

# set the chunk size for reading the file
chunk_size = 1024 * 1024

# load stop words
stop_words_url = "https://gist.githubusercontent.com/sebleier/554280/raw/22976e2acb4b4ad7a91f7080fa698e4a2409a1d1/stopwords.txt"
with urllib.request.urlopen(stop_words_url) as response:
    stopwords = [word.decode('utf-8').strip() for word in response.readlines()]

# loop through all zip files
for filename in zip_files:
    print(f"Processing {filename}")
    
    # initialize a dictionary to store the word count
    word_count = {}

    # start the timer
    start_time = time.time()

    # read the input file in chunks and process each chunk
    with open(os.path.join(dir_path, filename), "r") as f:
        while True:
            # read a chunk of data from the file
            data = f.read(chunk_size)
            if not data:
                break

            # process the chunk
            for word in data.split():
                # remove punctuations and convert to lowercase
                word = word.translate(str.maketrans("", "", string.punctuation)).lower()

                # ignore stop words and empty words
                if word in stopwords or not word:
                    continue

                # update the word count
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

    # get the top k words from the dictionary
    top_words = heapq.nlargest(k, word_count.items(), key=lambda x: x[1])

    # print the top k words
    for word, count in top_words:
        print(word, count)

    # calculate the running time
    end_time = time.time()
    running_time = end_time - start_time

    # print the performance metrics
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    cpu_utilization = process.cpu_percent()
    print(f"Running time: {running_time:.2f} seconds")
    print(f"Memory usage: {memory_usage / 1024 / 1024:.2f} MB")
    print(f"CPU utilization: {cpu_utilization:.2f}%")
    print("------\n")
