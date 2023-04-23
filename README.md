# K Most Popular Words
## Goal
The goal of this report is to analyze the performance of different approaches for finding the k most popular words in a dataset while taking into account various factors that affect application performance. The report aims to investigate the impact of input size, algorithm efficiency, data structures, and system resource utilization (such as CPU and memory) on the performance of each approach. Through this analysis, the report aims to understand how the size of the input dataset affects the performance of each approach and identify techniques that can be used to mitigate the problems caused by increasing input dataset size, which is the core challenge of Big Data. By comparing and evaluating the performance of each approach, the report aims to provide insights into the strengths and limitations of each approach and guide the selection of the most suitable approach for a given scenario. This analysis will help readers understand the impact of various factors on the performance of an application and make informed decisions about selecting appropriate algorithms and data structures for processing large datasets.


## The Problem Statement
The objective of this report is to design and implement an efficient python code to determine the top K most frequent/repeated words in a given dataset (example: K = 10) and present a detailed analysis of the performance through different metrics such as running time, speedup, CPU utilization, memory usage, etc. The report covers the analysis of the code execution on each of the three input data files separately.

The primary focus of this project is to obtain the result with the least possible execution time (or with the best performance on your computer) by skipping the "stop" words such as 'the' - which are provided in the stop words list available at [stop_words_link](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/stop_words.txt).

The result should preserve case sensitivity, which means that words like "Title" and "title" are considered as two different words. The input dataset contains only English alphabets, white spaces and hyphen separated words, i.e., "a-z," "A-Z," "\s."

Initially, the code has been tested on a smaller dataset provided at [small_dataset](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/small_50MB_dataset.txt). Then, the code has been executed on three larger datasets of different sizes provided in a zip file available at [zip_file_link](https://drive.google.com/file/d/1kaVM15rD9_O9HsvzrUKkIZ4R6ETUAdo4/view?usp=share_link). The zip file consists of three files with only English words, i.e., data_300MB.txt - a text file of size 300MB, data_2.5GB.txt - a text file of size 2.5GB, and data_16GB.txt - a text file of size 16GB.

This report presents a detailed analysis of why a particular algorithm or data structure has been used to solve this problem. The report also covers the presentation of the results obtained from the execution of the code and the performance metrics calculated.

## System Configurations
* **Processor**: processor used.
* **Cores**: number of cores.
* **Memory**: RAM available on the system.
* **Storage Type**: Type and size of the storage device used
* **Sorage size available**: Available disk space.
* **Operating System**: operating system and version
* **Programming Language**: Python3
* **Compiler and Runtime Environment**: Python 3 interpreter

## Experimental Process:

The goal of our experiment was to design and implement an efficient algorithm to find the top K most frequent words in a dataset. We experimented with various approaches using different data structures and algorithms and evaluated their performance on three input data files of different sizes. We implemented our approaches in Python and measured different metrics such as running time, speedup, CPU utilization, and memory usage to analyze their performance.

### Approach 1: [Hashmap File Singlethread](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/hashmap_file_singlethread.py)
In this approach, we read the entire data file in a single thread and stores the count of each word in a hashmap. , the entire dataset file is read using a single thread, and the count of each word is stored in a hashmap. Stop words are read from a separate file and removed from the word counts. The frequency of the remaining words is sorted in reverse order, and the top K words are returned.

The time complexity of this approach is O(nlogn) for sorting the frequency counts, where n is the number of words in the dataset. The space complexity is O(n) as the entire dataset needs to be stored in the hashmap. Therefore, this approach is best suited for smaller datasets where the sorting process will not be time-consuming.

this approach is efficient for small datasets but may not be the best option for larger datasets due to the time complexity of sorting. However, the advantage of using a hashmap is that it provides constant time complexity for accessing and updating the value of a key.

### Approach 2: [Counter Chunk Singlethread](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/counter_chunks_singlethread.py)
Next, in this approach, we read data in chunks using a single thread and count the occurrence of words. The data is processed by iterating through the chunks and lines within each chunk, using regular expressions to extract words, and checking if each word is in the stop words set. The word count is stored in a Counter object which provides constant time complexity for updating the value of a key.

To find the top K words, the most_common() function of the Counter object is used. This approach is more memory-efficient than storing the entire dataset in memory and eliminates the need for sorting the entire dataset. The time complexity of this approach is O(n), where n is the number of words in the dataset.

The code includes functions to read stop words from a file and to print the top K words and performance statistics. The main function prompts the user to enter the number of top words to find and processes the data with different chunk sizes. The performance statistics include the total processing time, file size, chunk size, and memory usage.

Overall, this approach provides a more efficient way to process large datasets while finding the most common words. The use of a Counter object allows for fast and memory-efficient word counting, while reading the data in chunks reduces memory usage and eliminates the need for sorting.

### Approach 3: [Counter Heapq Singlethread](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/counter_heapq_singlethread.py)
We then in this approach, we read the data in a single thread and stored the word count in the counter. It is another single-threaded approach for finding the top k frequent words in a given file. This approach uses the Counter data structure to count the frequency of each word in the file. Stop words are ignored using a predefined set of stop words. This approach uses the heapq.nlargest function to return the top k words with the highest frequency in the Counter object.

The time complexity of this approach is O(nlogk), where n is the total number of words in the file and k is the number of top words to be returned. The advantage of using heapq.nlargest is that it can efficiently find the top K elements in a list.

The program first reads the stop words from a file and stores them in a set. It then creates a Counter object to count the frequency of each word in the file. The file is read line by line, and each line is processed by lowercasing and splitting it into words using regular expressions. The frequency of each non-stop word is incremented in the Counter object.

Once the entire file has been processed, the program uses the heapq.nlargest function to find the top k words with the highest frequency in the Counter object. The program then prints the top k frequent words and performance statistics such as the time taken to process the file and the file size.

This approach is similar to Approach 2, but it uses heapq.nlargest instead of most_common to find the top k words, which may be more efficient for large values of k.

### Approach 4: [Defaultdict Chunks Heapq Singlethread](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/defaultdict_chunks%20heapq_singlethread.py)
We read the data in chunks in a single thread and stored the word count in the defaultdict. We used the heapq.nlargest function to return the top K words. This approach was similar to the previous one, but we used defaultdict instead of counter.In this approach, we read the data in chunks in a single thread and stored the word count in the defaultdict. We used the heapq.nlargest function to return the top K words. This approach is similar to the previous one, but we used defaultdict instead of counter. The advantage of using defaultdict is that it automatically initializes the value of a key to a default value, which is useful when we don't know the exact keys beforehand.

### Approach 5: [Defaultdict Chunks Multiprocess](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/defaultdict_chunks_multiprocess.py)
In this approach, we use defaultdict and heapq to find the top K frequent words in a file. The file is read in chunks in a single thread, and the word count is stored in a defaultdict. The use of defaultdict is advantageous because it automatically initializes the value of a key to a default value, which is useful when we don't know the exact keys beforehand. The chunks are processed using multiprocessing Pool to speed up the processing. Finally, heapq.nlargest is used to return the top K words from the dictionary of word counts.

The code first reads stop words from a file and then creates a list of chunks. Each chunk is processed by process_chunk function, which takes a chunk and a set of stop words as arguments and returns a dictionary of word counts. The process_chunk function uses re.findall to extract words from each line and filters out stop words. It returns a dictionary of word counts for the chunk.

The chunks are processed using multiprocessing Pool to speed up the processing. The pool.imap_unordered method is used to apply the process_chunk function to each chunk in parallel. The result is a list of dictionaries of word counts for each chunk. These dictionaries are merged using defaultdict to get the total word count for the file.

Finally, heapq.nlargest is used to find the top K frequent words from the dictionary of word counts. The result is printed using log.get_top_words_heapq function, and the performance statistics are printed using log.print_statistics function.

The time complexity of this approach is O(N log K), where N is the number of words in the file and K is the number of top words to find. The space complexity is O(N), where N is the number of unique words in the file.

### Approach 6: [Counter Chunk Multithread](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/counter_chunks_multithread.py)
This approach uses multithreading to read and process data in chunks. The file is divided into chunks, and each chunk is read by a separate thread, where the word count is stored in a counter. Stop words are removed during processing. The most_common function is used to retrieve the top K words.

The time complexity of this approach is O(n/p), where n is the size of the input file, and p is the number of threads. By using multiple threads, this approach can utilize multiple cores of a CPU, which can lead to faster processing of large datasets.

The space complexity of this approach is proportional to the number of unique words in the input file, which is stored in the counter.

The read_stop_words function reads a file containing stop words and returns a set of stop words. The read_chunk function reads a chunk of the input file, given the chunk start position and size. The process_chunk function processes a chunk of data by counting the occurrences of each word and removing stop words.

The process_data function processes the input file in chunks and prints the top K words and performance statistics. It creates a list of chunks and processes each chunk in a separate thread. The threads are then joined to wait for all threads to finish. The function also determines the chunk size if it is not specified and prints information about the file size and chunk size.

The main function sets the number of top words to find and calls the process_data function for different chunk sizes.

### Approach 7: [Counter Lines Multithread](https://github.com/divaamahajan/K-Most-Popular-Words/blob/main/counter_lines_multithread.py)
Finally, we  aim to optimize the multithreading approach used in Approach 6. Instead of creating a thread for every word in the data file, this approach creates a separate thread for every line in the file. The word count for each line is stored in a local counter, and the global counts are updated by aggregating the local counters of all threads.

The approach reads the data file in a multithreaded manner, where each thread reads a line from the file. For each line, a thread is created to count the words in that line, excluding the stop words. The word count for each line is stored in a local counter associated with the thread that counted the words. Once all threads have completed counting, the global counts are updated by aggregating the local counters of all threads. Finally, the most common words are selected and printed.

The time complexity of this approach is O(n), where n is the number of lines in the data file. The space complexity is O(k+m), where k is the number of top words to find, and m is the number of unique words in the data file.

However, this approach is not efficient for larger datasets as too many threads are being used, resulting in high CPU utilization and slow performance. Even for small datasets, the overhead of creating and managing threads is significant.

In summary, this approach aims to optimize the multithreading approach used in Approach 6 by creating a separate thread for each line in the data file and aggregating the local counters of all threads. However, this approach is not efficient for larger datasets due to the high CPU utilization and slow performance resulting from the use of too many threads.

## Evaluation
To evaluate the performance of these approaches, we measured various metrics such as running time, speedup, CPU utilization, and memory usage and mainted detailed [logs](https://github.com/divaamahajan/K-Most-Popular-Words/tree/main/logs). Based on the analysis of the results, we identified the most efficient approach. We also provided a detailed analysis of why we chose a particular algorithm or a particular data structure to solve this problem, considering the trade-offs between time complexity, space complexity, and parallelism. Overall, we aimed to achieve the best performance possible while minimizing the execution time of our code.
