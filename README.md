# FTMO
FTMO: Few-shot temporal knowledge graph completion based on meta-optimization.
This repository contains the implementation of the FTMO architectures described in the paper.
# Installation
 Install Pytorch (>= 1.1.0)
 ```
pip install pytorch
```
 Python 3.x (tested on Python 3.6)
  ```
pip install python 3.6
```
 Numpy
  ```
pip install numpy
```
 Pandas
  ```
pip install pandas
```
 tqdm
  ```
pip install tqdm
```
How to use
run the code:
```
python main.py --parameters
```
# Parameters setting
1) The embedding dimension of the two data sets is uniformly set to 100.  
 2) LSTM is used as the reference aggregator and matching processor. The hidden dimension of LSTM is consistently set to 200.   
 3) For two data sets, the maximum local neighborhood number of the heterogeneous neighborhood encoder species is 30.   
 4) In the process of updating model parameters, we choose Adam optimizer.   
 5) For both data sets, we set the number of steps in the matching cycle in the network to 2.  
 6) The initial learning rate is 0.001, and the weight attenuation is 0.25. 7 per 10k training step.  
 7) The edge distance in the objective function is set to 5.0 and the transaction factor is set to 0.0001.   
 8) In the construction of entity candidate sets, we set the maximum size of the two data sets to 1000.
# Dateprocess
To run our code, we need to divide the data set according to the data set partition file first, or divide it according to our own needs. If we want to get the best results, we need to use Complex to pre-train and then embed it into the model.


| Baselines   | Code                                                         | parameters                  |
| ----------- | ------------------------------------------------------------ | --------------------------- |
| TransE      | [Link](https://github.com/jimmywangheng/knowledge_representation_pytorch) | { lr=0.0001, dim=512,b=512} |
| TTransE     | [link](https://github.com/INK-USC/RE-Net)                    | { lr=0.001, dim=512,b=512}  |
| DE-SimplE   | [link](https://github.com/BorealisAI/DE-SimplE)              | { lr=0.001, dim=128,b=512}  |
| TA-DistMult | [link](https://github.com/INK-USC/RE-Net)                    | { lr=0.001, dim=512,b=1024} |
| Gamtching   | [link]                                                       |                             |
| MateR       | [link]                                                       |                             |
| FSRL        | [link]                                                       |                             |
