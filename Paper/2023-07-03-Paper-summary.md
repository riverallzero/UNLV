# Paper Summary 
- Title: A MapReduce based distributed SVM algorithm for binary classification
- Author: Ferhat Özgür Çatak, Mehmet Erdal Balaban
- Compared the single node SVM training algorithm with MapReduce based SVM training algorithm

## Feature selection methods
- Is a basic approach for reducing feature vector size
- This solve two main problems
  1. reducing the number of the feature set in the training set to effectively use of computing resources like memory and CPU
  2. to remove noisy features from the dataset in order to improve the classification algorithm performance

## Feature extraction methods
- high dimensional feature space is transformed into low dimensional feature space
- Ex) Principal Component Analysis (PCA), Singular Value Decomposition (SVD), Independent Component Analysis (ICA)
  
## SVM
In this paper, they propose a novel approach and formal analysis of the models that generated with the MapReduce based binary SVM training method. This algorithm is built on the LibSVM and implemented using the Hadoop implementation of MapReduce.

### Proposed
#### Cascade SVM[11]
- Dataset is split into parts in feature space. Non-support vectors of each sub dataset are filtered and only support vectors are transmitted. The margin optimization process uses only combined sub dataset to find out the support vectors.

#### New parallel SVM training and classification algorithm[12]
- Dataset is trained with SVM and then the classifiers are combined into a final single classifier function.

#### Strongly connected network based distributed support vector machine algorithm[13]
- Dataset is split into roughly equal part for each computer in a network then, support vectors are exchanged among these computers.

#### Novel incremental learning with SVM algorithm[14]
- A fusion center collects all support vectors from distributed computers
  
#### Novel method for parallelized SVM based on MapReduce(based on Cascade SVM)[17]
- Approach is based on iterative MapReduce model Twister which is different from our implementation of Hadoop based MapReduce.
- Their method is same with cascade SVM model.
- They use only support vectors of a sub dataset to find an optimal classifier function.

### About
SVM is deal with binary classification problems and aim to find a hyperplane that maximizes the margin between two classes. The data points are considered to find the hyperplane that separates the boundaries between the classes. For the generalization property, two parallel hyperplanes are defined, which form the boundary separating the classes. These two functions can be simplified into one and can be used in the optimization process.

![img](https://github.com/riverallzero/UNLV/assets/93754504/b8a4c954-c95e-47b6-ac95-bd680a46a942)

![](https://github.com/riverallzero/UNLV/assets/93754504/b2599501-02f6-4d61-a9f5-091cea1641c0)
This inequality takes into account the distance to the hyperplane to classify data point xi into the corresponding class yi. SVM is defined as an optimization problem of finding a hyperplane that satisfies this inequality. The goal is to minimize the percentage of misclassified data points while maximizing the margin.
- yi: a value indicating the class of the input vector xi, either -1 or 1.
- xi: an input vector, representing the characteristics of a data point.
- W: the normal vector of the hypersurface.
- WT: the transpose of W.
- b: the bias value of the hyperplane.

w.x + b = 1 & w.x + b = -1 are the expression used to define the margin in an SVM. SVM is an algorithm for finding a hyperplane to classify two classes, and the goal is to find a hyperplane that maximizes the distance between the classes. The wider the graph spacing between w.x + b = 1 and w.x + b = -1, the better the performance of the SVM generally tends to be.

## Map Reduce
Is a distributed computing framework for large-scale data processing that splits data into small pieces, called chunks, and stores them on multiple data nodes.

![](https://github.com/riverallzero/UNLV/assets/93754504/5d244a27-0694-45e3-9ee9-37e0c624f64d)

### Function
- **Map**: the first step in a MapReduce job, taking the key/value pairs of an input chunk and outputting them as a list of new key/value pairs, meaning that for each input key/value pair, the map function can generate one or more new key/value pairs.
- **Reduce**: the second step in a MapReduce operation and deals with grouping values that have the same key. It takes as input a key and a list of values for that key, and outputs a list of new values. In other words, the reduce function can take values for the same key and generate one or more new values.
  
### Example
  ```
  The data we have is the ages of people and the cities they live in, each represented as a key/value pair.
  
  map(key1, value1) => list(key2, value2)
  
  In this case, the map function can act as follows.
  For example, the key (key1) represents the age of a person and the value (value1) represents the city the person lives in.
  
  map(25, "Seoul") => list("20s", "Seoul")
  map(30, "Busan") => list("30s", "Busan")
  map(35, "Seoul") => list("30s", "Seoul")
  
  In the above example, the reduce function accepts values (value2) for the same key (key2).
  Here, the same key represents an age range ("20s", "30s", etc.) and the reduce function utilizes these values to perform an operation.
  
  For example, the reduce function can aggregate cities in the same age range to produce a statistic, or find cities that meet certain conditions.
  
  reduce("20s", ["Seoul"]) => list("Seoul")
  reduce("30s", ["Busan", "Seoul"]) => list("Busan", "Seoul")
  
  As a result, the reduce function creates a new list of values (value3) as a result of this operation.
  In the example above, we have returned a grouping of cities that fall within the same age range.
  ```

## System Model
The cloud computing based binary class support vector machine algorithm works as follows. The training set of the algorithm is split into subsets. Each node within a cloud computing system classifies sub dataset locally via SVM algorithm and gets α values (i.e. support vectors (SVs)), and then passes the calculated SVs to global SVs to merge them.

### Algorithm 1: Map
Repeat the updating process by adding the global support vector to each class-specific dataset.

### Algorithm 2: Reduce
For each class, apply the binary SVM algorithm and add the resulting support vectors to the global set of support vectors.

![](https://github.com/riverallzero/UNLV/assets/93754504/b31a2563-958b-41ed-bb81-126a89201571)

## Comparison
### Speedup
Calculation of the speedup is computation time with MapReduce divided by the single node training model computation time. 

![](https://github.com/riverallzero/UNLV/assets/93754504/682f01d7-5aaf-40f2-8c4c-2ae82e8ccb8c) | ![](https://github.com/riverallzero/UNLV/assets/93754504/edae9b35-4141-498f-9ed0-dd7ee74ed223)
---| ---|

## Result
![](https://github.com/riverallzero/UNLV/assets/93754504/0f1c03c2-8bf9-457f-ade8-1eaf98949bed)

![](https://github.com/riverallzero/UNLV/assets/93754504/86fde743-7726-46a5-a103-bb29e70bfb78)
