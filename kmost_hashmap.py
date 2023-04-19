import psutil
import time
import os
import string

# set the number of top words to find
k = int(input("Enter the number of top words to find: "))
dict_words = {}
stop_words = []
word = ""
with open("stop_words.txt","r", encoding='utf-8-sig') as sw:
    while True:
        wordList = sw.read()
        for words in wordList:
            if(words != "\n"):
                word += words
            else:
                stop_words.append(word)
                word = ""
        if not wordList:
            break

# start the timer
start_time = time.time()

with open("small_50MB_dataset.txt",'r') as file:
    while True:
        input = file.read()
        if not input:
            break
        lists = input.split()
        for data in lists:
            # readData = data.translate(str.maketrans("","",string.punctuation)).lower()
            readData = data
            if readData and (readData not in stop_words):
                if(readData not in dict_words.keys()):
                    dict_words[readData] = 1
                else:
                    dict_words[readData] += 1
print(f"\nTop frequent words:")
print(f"{dict_words}")

# calculate the running time
end_time = time.time()
running_time = end_time - start_time

# print the performance metrics
process = psutil.Process()
memory_usage = process.memory_info().rss
cpu_utilization = process.cpu_percent()
print(f"Running time: {running_time:.2f} seconds")
print(f"\nMemory usage: {memory_usage / 1024 / 1024:.2f} MB")
print(f"\nCPU utilization: {cpu_utilization:.2f}%")
print("------\n")
