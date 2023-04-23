# K Most Popular Words
## The Problem Statement
The objective of this report is to design and implement an efficient python code to determine the top K most frequent/repeated words in a given dataset (example: K = 10) and present a detailed analysis of the performance through different metrics such as running time, speedup, CPU utilization, memory usage, etc. The report covers the analysis of the code execution on each of the three input data files separately.

The primary focus of this project is to obtain the result with the least possible execution time (or with the best performance on your computer) by skipping the "stop" words such as 'the' - which are provided in the stop words list available at [stop_words_link](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/stop_words.txt).

The result should preserve case sensitivity, which means that words like "Title" and "title" are considered as two different words. The input dataset contains only English alphabets, white spaces and hyphen separated words, i.e., "a-z," "A-Z," "\s."

Initially, the code has been tested on a smaller dataset provided at [small_dataset](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/small_50MB_dataset.txt). Then, the code has been executed on three larger datasets of different sizes provided in a zip file available at [zip_file_link](https://drive.google.com/file/d/1kaVM15rD9_O9HsvzrUKkIZ4R6ETUAdo4/view?usp=share_link). The zip file consists of three files with only English words, i.e., data_300MB.txt - a text file of size 300MB, data_2.5GB.txt - a text file of size 2.5GB, and data_16GB.txt - a text file of size 16GB.

This report presents a detailed analysis of why a particular algorithm or data structure has been used to solve this problem. The report also covers the presentation of the results obtained from the execution of the code and the performance metrics calculated.


## Experimental Process:

The goal of our experiment was to design and implement an efficient algorithm to find the top K most frequent words in a dataset. We experimented with various approaches using different data structures and algorithms and evaluated their performance on three input data files of different sizes. We implemented our approaches in Python and measured different metrics such as running time, speedup, CPU utilization, and memory usage to analyze their performance.

### Approach 1: [Hashmap File Singlethread](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/hashmap_file_singlethread.py)
We began by reading the data in a single thread and storing the word count in a hashmap. We then sorted the frequency of the words in reverse and returned the top K words. While this approach was straightforward, it required sorting the entire dataset, making it time-consuming for larger datasets.

### Approach 2: [Counter Chunk Singlethread](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/counter_chunks_singlethread.py)
Next, we read the data in chunks in a single thread and stored the word count in a counter. We used the most_common function of the counter to return the top K words. This approach was more memory-efficient as it didn't require storing the entire dataset in memory. It also eliminated the need for sorting the entire dataset.

### Approach 3: [Counter Heapq Singlethread](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/counter_heapq_singlethread.py)
We then read the data in a single thread and stored the word count in the counter. We used the heapq.nlargest function to return the top K words. This approach was similar to the previous one, but we used heapq.nlargest to find the top K words instead of the most_common function.

### Approach 4: [Defaultdict Chunks Heapq Singlethread](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/defaultdict_chunks%20heapq_singlethread.py)
We read the data in chunks in a single thread and stored the word count in the defaultdict. We used the heapq.nlargest function to return the top K words. This approach was similar to the previous one, but we used defaultdict instead of counter.

### Approach 5: [Defaultdict Chunks Multiprocess](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/defaultdict_chunks_multiprocess.py)
We read the data in chunks using multiprocessing and stored the word count in the defaultdict. We sorted the frequency of the words in reverse and returned the top K words. This approach leverages multiprocessing to speed up the computation for larger datasets.

### Approach 6: [Counter Chunk Multithread](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/counter_chunks_multithread.py)
We read the data in chunks using multithreading, where each thread was reading a chunk. We stored the word count in the counter and used the most_common function to return the top K words. This approach leverages multithreading to speed up the computation for larger datasets.

### Approach 7: [Counter Lines Multithread](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/counter_lines_multithread.py)
Finally, we read the data in a multithread, where each thread was reading a line. We stored the word count in the counter and used the most_common function to return the top K words. However, this approach was not efficient for larger datasets as too many threads were being used, resulting in high CPU utilization and slow performance.

To evaluate the performance of these approaches, we measured various metrics such as running time, speedup, CPU utilization, and memory usage and mainted detailed [logs](https://github.com/divaamahajan/K-Most-Popular-Words/tree/main/logs). Based on the analysis of the results, we identified the most efficient approach. We also provided a detailed analysis of why we chose a particular algorithm or a particular data structure to solve this problem, considering the trade-offs between time complexity, space complexity, and parallelism. Overall, we aimed to achieve the best performance possible while minimizing the execution time of our code.
