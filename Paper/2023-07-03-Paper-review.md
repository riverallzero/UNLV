# Paper Review 
- Title: A MapReduce based distributed SVM algorithm for binary classification
- Author: Ferhat Özgür Çatak, Mehmet Erdal Balaban

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
