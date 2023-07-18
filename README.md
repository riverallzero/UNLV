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
os.environ["CUDA_VISIBLE_DEVICES"]="2" #don't use 0 in DIONE
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
- Week 3: Develop MapReduce with python-multiprocessing [[code]](https://github.com/riverallzero/UNLV/blob/main/Project/mapreduce_multiprocessing.py)
- Week 4: Develop MapReduce with pyspark [[code]](https://github.com/riverallzero/UNLV/blob/main/Project/mapreduce_pyspark.py)
- Final: Write a paper [[paper]](https://github.com/riverallzero/UNLV/blob/main/Project/paper.pdf)
  
## 2. MapReduce
### 📑 Python-multiprocessing
#### What is Multiprocessing?

#### Compare with CPU

### 📑 Pyspark-RDD
#### What is RDD?
