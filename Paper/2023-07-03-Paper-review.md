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
