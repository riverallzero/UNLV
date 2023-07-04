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
In this paper, they propose a novel approach and formal analysis of the models that generated with the MapReduce based binary SVM training method

### Proposed
#### Cascade SVM
#### New parallel SVM training and classification algorithm
#### Strongly connected network based distributed support vector machine algorithm
#### Novel incremental learning with SVM algorithm
#### Novel method for parallelized SVM based on MapReduce(based on Cascade SVM)
