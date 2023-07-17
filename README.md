# UNLV-Research
- In **U**niversity of **N**evada, **L**as **V**egas
- Period: 2023.06.25 ~ 2023.07.23
- Project: Definition of scaleable machine learning for big data
- Description: Big data analytics provides scalable solutions for distributed or very large data. For this project, students will have hands-on experience installing Apache Spark, and practicing python libraries, e.g., MLLib, while applying supervised and unsupervised machine learning algorithms to large datasets for data analysis and developing machine learning models.

## JupyterLab
- username: su2023grp7
  
### terminal setting
1. <code>conda init bash</code>
2. <code>conda create -n [env_name] python=3.8</code>
3. <code>conda activate [env_name]</code>
4. <code>pip install jupyter notebook</code>, <code>pip install ipykernel</code>
5. <code>python -m ipykernel install --user --name [env_name] --display-name [env_name]</code>
6. <code>jupyter notebook</code>
7. Jupyter Notebook: [setting]kernel -> change kernel
- remove virtualenv: <code>rm -rf [env_path]</code>

### GPU setting
```python
import os

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="2" #don't use 0 in dione
```
### background running
1. <code>byobu -S1</code> (S1, S2 etc.)
2. <code>conda activate [env_name]</code>
3. <code>python3 main.py</code>

## 1. About
### Subject
How to implement **map** and **reduce** function using Spark

### Weekly Plan
- Week 1: Intro Machine Learning
- Week 2: Semina about Spark [[slide]](https://github.com/riverallzero/UNLV-proj/blob/main/Week2(mon)-session.pdf)
- Week 3: Develop MapReduce with python [[code]](https://github.com/riverallzero/UNLV/blob/main/Project/MapReduce_multiprocessing.py)
- Week 4: Develop MapReduce with pyspark [[code]](https://github.com/riverallzero/UNLV/blob/main/Project/MapReduce_pyspark.py)
- Final: Write a paper
  
### Papers
[📁 Paper [go]](https://github.com/riverallzero/UNLV-proj/tree/main/Paper)
- [Spark: Cluster Computing with Working Sets](https://www.usenix.org/legacy/event/hotcloud10/tech/full_papers/Zaharia.pdf)
- [PySpark : High-performance data processing without learning Scala](https://www.ibm.com/downloads/cas/DVRQZYOE)
- [MLlib: Machine Learning in Apache Spark](https://www.jmlr.org/papers/volume17/15-237/15-237.pdf)
- [Scalable Machine Learning Using PySpark](https://ieeexplore.ieee.org/document/9842696)
- [A MapReduce based distributed SVM
algorithm for binary classification](https://arxiv.org/pdf/1312.4108.pdf)

#### summary
- [A MapReduce based distributed SVM
algorithm for binary classification](https://github.com/riverallzero/UNLV/blob/main/Paper/2023-07-03-A%20MapReduce%20based%20distributed%20SVM%20algorithm%20for%20binary%20classification.md)

### Book
[📁 Book [go]](https://github.com/riverallzero/UNLV-proj/tree/main/Book)
- [Big Data Analytics with Spark](https://github.com/riverallzero/UNLV-proj/blob/main/Book/Big%20Data%20Analytics%20with%20Spark.pdf)(Mohammed Guller)

## 2. MapReduce
MapReduce is a software framework for processing large data sets in a distributed fashion over a several machines. The core idea behind MapReduce is mapping your data set into a collection of (key, value) pairs, and then reducing over all pairs with the same key.
The overall concept is simple, but is actually quite expressive when you consider that:

- Almost all data can be mapped into (key, value) pairs somehow, and
- Keys and values may be of any type: strings, integers, dummy types, and, of course, (key, value) pairs themselves

The canonical MapReduce use case is counting word frequencies in a large text, but some other examples of what you can do in the MapReduce framework include:

- Distributed sort
- Distributed search
- Web‐link graph traversal
- Machine learning

Counting the number of occurrences of words in a text is sometimes considered as the “Hello world!” equivalent of MapReduce. A classical way to write such a program is presented in the python script below. The script is very simple. It parses the file from which it extracts and counts words and stores the result in a dictionary that uses words as keys and the number of occurrences as values. [[data.txt]](https://nyu-cds.github.io/python-bigdata/files/pg2701.txt)

```python
import re


def splitter(line):
    line = re.sub(r"^\W+|\W+$", "", line)

    return map(str.lower, re.split(r"\W+", line))
    
sums = {}
try:
    in_file = open("data.txt", "r")

    for line in in_file:
        for word in splitter(line):
            word = word.lower()
            sums[word] = sums.get(word, 0) + 1
                 
    in_file.close()

except IOError:
    print("error performing file operation")
else:
    M = max(sums.keys(), key=lambda k: sums[k])
    print("max: %s = %d" % (M, sums[M]))
```

```
>> max: the = 14620
```

The main problem with this approach comes from the fact that it requires the use of a dictionary, i.e., a central data structure used to progressively build and store all the intermediate results until the final result is reached.

Since the code we use can only run on a single processor, the best we can expect is that the time necessary to process a given text will be proportional to the size of the text (i.e., the number of words processed per second is constant).

In reality though, the performance degrades as the size of the dictionary grows. As shown on the diagram below, the number of words processed per second diminishes when the size of the dictionary reaches the size of the processor data cache (note that if the cache is structured in several layers of different speeds, the processing speed will decrease each time the dictionary reaches the size of a layer).

An even larger decrease in processing speed will occur when the dictionary reaches the size of the computer’s Random Access Memory (RAM).
Eventually, if the dictionary continues to grow, it will exceed the capacity of the swap space and an exception will be raised.

![](https://github.com/riverallzero/UNLV/assets/93754504/88ecd5b0-1e57-4ced-a7c8-fd222e04e23f)

### Aproach
The main advantage of the MapReduce approach is that it does not require a central data structure so the memory issues that occur with the simplistic approch are avoided.

MapReduce consists of 3 steps:
- A mapping step that produces intermediate results and associates them with an output key
- A shuffling step that groups intermediate results associated with the same output key
- A reducing step that processes groups of intermediate results with the same output key
  
![](https://github.com/riverallzero/UNLV/assets/93754504/9f3bdc8f-b9a5-4ea0-adb8-1d66797cb61b)

#### Mapping
The mapping step is very simple. The idea is to apply a function to each element of a list and collect the result. This is essentially the same as the Python map method that takes a function and sequence of input values and returns a sequence of values that have had the function applied to them.

```python
import re


def splitter(line):
    line = re.sub(r"^\W+|\W+$", "", line)
    
    return map(str.lower, re.split(r"\W+", line))
    
input_file = "data.txt"
map_file = "data_map.txt"

sums = {}
try:
    in_file = open(input_file, "r")
    out_file = open(map_file, "w")

    for line in in_file:
        for word in splitter(line):
            out_file.write(word.lower() + "\t1\n")
    in_file.close()
    out_file.close()

except IOError:
    print("error performing file operation")
```

Then the result "data_map.txt" contains:

```
the     1
project 1
gutenberg       1
ebook   1
of      1
moby    1
...
```

#### Shuffling
The shuffling step consists of grouping all the intermediate values that have the same output key. In our word count example, we want to sort the intermediate key/value pairs on their keys.

```python
map_file = "data_map.txt"
sorted_map_file = "data_map_sorted.txt"

def build_index(filename):
    index = []
    f = open(filename)
    while True:
        offset = f.tell()
        line = f.readline()
        if not line:
            break
        length = len(line)
        col = line.split("\t")[0].strip()
        index.append((col, offset, length))
    f.close()
    index.sort()
    
    return index

try:
    index = build_index(map_file)
    in_file = open(map_file, "r")
    out_file = open(sorted_map_file, "w")
    for col, offset, length in index:
        in_file.seek(offset)
        out_file.write(in_file.read(length))
    in_file.close()
    out_file.close()
except IOError:
    print("error performing file operation")
```

Then the result "data_map_sorted.txt" contains:

```
1
1
1
1
1
1
...
```

#### Reducing
For the reduction step, we just need to count the number of values with the same key. Now that the different values are ordered by keys (i.e., the different words are listed in alphabetic order), it becomes easy to count the number of times they occur by summing values as long as they have the same key.

```python
previous = None
M = [None, 0]

def checkmax(key, sum):
    global m, M
    if M[1] < sum:
        M[1] = sum
        M[0] = key

try:
    in_file = open(sorted_map_file, "r")
    for line in in_file:
        key, value = line.split("\t")
        
        if key != previous:
            if previous is not None:
                checkmax(previous, sum)
            previous = key
            sum = 0
            
        sum += int(value)
        
    checkmax(previous, sum)
    in_file.close()
except IOError:
    print("error performing file operation")
    
print("max: %s = %d" % (M[0], M[1]))
```

```
>> max: the = 14620
```

#### Conclusion
Although these three steps seem like a complicated way to achieve the same result, there are a few key differences:

- In each of the three steps, the entire contents of the file never had to be held in memory. This means that the program is not affected by the same caching issues as the simple version.
- The mapping function can be be split into many independent parallel tasks, each generating separate files.
- The shuffing and reducing functions can also be split into many independent parallel tasks, with the final result being written to an output file.
  
The fact that the MapReduce algorithm can be parallelized easily and efficiently means that it is ideally suited for applications on very large data sets, as well as were resiliance is required.
