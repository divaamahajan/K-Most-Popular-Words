# A program to find k most frequent words in a file
import psutil
import time

MAX_CHARS = 26
MAX_WORD_SIZE = 30

SIZE_5MB  = int(5  * 1024 * 1024 )# 5 MB
SIZE_10MB = int(10 * 1024 * 1024 )# 10 MB
SIZE_20MB = int(20 * 1024 * 1024 )# 20 MB
SIZE_40MB = int(40 * 1024 * 1024 )# 40 MB

FILENAME_50MB = "small_50MB_dataset.txt"
FILENAME_300MB = "data_300MB.txt"
FILENAME_2_5GB = "data_2.5GB.txt"
FILENAME_16GB = "data_16GB.txt"
FILE_STOP_WORDS = "stop_words.txt"

size_dict = {None: "None. Full file is being read at once" ,SIZE_5MB: '5MB', SIZE_10MB: '10MB', SIZE_20MB: '20MB', SIZE_40MB: '40MB'}


# A Trie node
class TrieNode:
    def __init__(self):
        self.isEndOfWord = False # indicates end of word
        self.word_count = 0 # the number of occurrences of a word
        self.indexMinHeap = -1 # the index of the word in minHeap
        # self.children = [None] * MAX_CHARS # represents 26 slots each for 'a' to 'z'
        self.children = {}


# A Min Heap node
class MinHeapNode:
    def __init__(self, root, word_count, word):
        self.root = root # indicates the leaf node of TRIE
        self.node_count = word_count # number of occurrences
        self.word = word # the actual word stored

# A Min Heap
class MinHeap:
    def __init__(self, k):
        self.capacity = k # the total size a min heap
        self.heap_size = 0 # indicates the number of slots filled
        self.heap = [] # represents the collection of minHeapNodes

    # This is the standard minHeapify function. It does one thing extra.
    # It updates the minHapIndex in Trie when two nodes are swapped in
    # in min heap
    def minHeapify(self, idx):
        left = 2 * idx + 1
        right = 2 * idx + 2
        smallest = idx

        if (left < self.heap_size and
            self.heap[left].node_count < self.heap[smallest].node_count):
            smallest = left

        if (right < self.heap_size and
            self.heap[right].node_count < self.heap[smallest].node_count):
            smallest = right

        if smallest != idx:
            # Update the corresponding index in Trie node.
            self.heap[smallest].root.indexMinHeap = idx
            self.heap[idx].root.indexMinHeap = smallest

            # Swap nodes in min heap
            self.heap[smallest], self.heap[idx] = self.heap[idx], self.heap[smallest]

            self.minHeapify(smallest)

    # A standard function to build a heap
    def buildMinHeap(self):
        n = self.heap_size - 1
        for i in range((n - 1) // 2, -1, -1):
            self.minHeapify(i)

    # Inserts a word to heap, the function handles the 3 cases explained above
    def insert_in_min_heap(self, root, word):
        # Case 1: the word is already present in minHeap
        if root.indexMinHeap != -1:
            self.heap[root.indexMinHeap].node_count += 1

            # percolate down
            self.minHeapify(root.indexMinHeap)

        # Case 2: Word is not present and heap is not full
        elif self.heap_size < self.capacity:
            count = self.heap_size
            self.heap.append(MinHeapNode(root, root.node_count, word))
            self.heap[count].root.indexMinHeap = self.heap_size
            self.heap_size += 1
            self.buildMinHeap()

        # Case 3: Word is not present and heap is full. And word_count of word
        # is more than root. The root is the least frequent word in heap,
        # replace root with new word
        elif root.node_count > self.heap[0].node_count:
            self.heap[0].root.indexMinHeap = -1
            self.heap[0].root = root
            self.heap[0].root.indexMinHeap = 0
            self.heap[0].node_count = root.node_count
            self.heap[0].word = word

            # percolate down the root to maintain min heap property
            self.minHeapify(0)

    # Return the root of the heap
    def get_min(self):
        if self.heap_size > 0:
            return self.heap[0].word
        return None
# A Trie data structure to store words

    def print_min_heap(self):
        print("Min Heap:")
        for i in range(self.heap_size):
            print(f"{self.heap[i].word} ({self.heap[i].node_count})")

class Trie:
    def __init__(self):
        self.root = TrieNode()
        # self.wordList = []
    
    # A utility function to insert a word to Trie
    def insert_trie(self, word):
        currentNode = self.root
        for ch in word:
            index = ord(ch) - ord('a')
            if not currentNode.children[index]:
                currentNode.children[index] = TrieNode()
            currentNode = currentNode.children[index]
        currentNode.isEndOfWord = True
        currentNode.word_count += 1
        return currentNode


    # A function to insert a word to Trie and Min Heap
    def insertUtil(self, word, minHeap, k):
        # If the word is already present in Trie, update its word_count
        currentNode = self.root
        for ch in word:
            index = ord(ch) - ord('a')
            if not currentNode.children[index]:
                currentNode.children[index] = TrieNode()
            currentNode = currentNode.children[index]
        if currentNode.isEndOfWord:
            currentNode.word_count += 1
        else:
            currentNode.isEndOfWord = True
            currentNode.word_count = 1
            self.wordList.append(word)

        # Insert the word to Min Heap
        minHeap.insert_in_min_heap(currentNode, word)

        # If Min Heap has more than k words, remove the least frequent word
        if len(minHeap.heap) > k:
            minHeap.heap[0].root.isEndOfWord = False
            minHeap.heap[0].root.word_count = minHeap.heap[0].word_count
            minHeap.heap[0].root.indexMinHeap = -1
            minHeap.heap[0] = minHeap.heap[-1]
            minHeap.heap.pop()
            minHeap.heap_size -= 1
            minHeap.minHeapify(0)

    # A recursive function to print the k most frequent words in Trie
    def kMostFrequentUtil(self, currentNode, minHeap):
        if currentNode.isEndOfWord:
            minHeap.insert_in_min_heap(currentNode, self.wordList[currentNode.word_count - 1])

        for i in range(MAX_CHARS):
            if currentNode.children[i]:
                self.kMostFrequentUtil(currentNode.children[i], minHeap)

    # The main function to print the k most frequent words in Trie
    def kMostFrequent(self, k):
        minHeap = MinHeap(k)

        self.kMostFrequentUtil(self.root, minHeap)

        for i in range(k):
            word = minHeap.get_min()
            if word:
                print(word)
            else:
                break

def print_top_words(word_counts, k):
    # get the top k words from the Counter
    top_words = word_counts.most_common(k)

    # print the top k wordsprint("\nTop frequent words:")
    print("Word".ljust(20) + "Count")
    for word, count in top_words:
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


def read_stop_words(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as sw:
        stop_words = set()
        for line in sw:
            stop_words.update(line.strip().split(","))
        return stop_words

def read_datafile(file_path, stop_words, top_k):
    root = TrieNode()
    min_heap = MinHeap(top_k)
    with open(file_path, "r") as file:
        for line in file:
            for word in line.strip().split():
                # skipping stop words
                if word.lower() not in stop_words:
                    current_node = root
                    for char in word:
                        current_node = current_node.children.setdefault(char, TrieNode())
                    current_node.isEndOfWord = True
                    current_node.word_count += 1
                    if current_node.indexMinHeap == -1:
                        min_heap.insert_heap(word, current_node.word_count, current_node)
                    else:
                        min_heap.heapify(current_node.indexMinHeap)
    return root, min_heap


def process_data(filename, stop_words,top_k):
    start_time = time.time()

    # count words from data file
    word_counts = read_datafile(filename, stop_words)

    # print the top k words
    print_top_words(word_counts, top_k)

    # print the performance metrics
    print_statistics(start_time)

# Driver program to test above functions
def main():
    # set the number of top words to find
    k = int(input("Enter the number of top words to find: "))
    filename = FILENAME_50MB
    # read stop words from file
    stop_words = read_stop_words(FILE_STOP_WORDS)

    trie = Trie()
    minHeap = MinHeap(k)

    
    start_time = time.time()
    # Open file and read its content
    root, min_heap = read_datafile(filename, stop_words, k)

    # Print the k most frequent words in the file
    print("The", k, "most frequent words are:")
    for i in range(k):
        print(minHeap.get_min())
        minHeap.heap.pop(0)
        minHeap.heap_size -= 1
        minHeap.buildMinHeap()


    # print the performance metrics
    print_statistics(start_time)
    
    min_heap.print_min_heap()


if __name__ == '__main__':
    main()