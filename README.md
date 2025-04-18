From Flow to Packet: A Unified Machine Learning Approach for Advanced Intrusion Detection
===
This project is the repository from our paper, in which we propose a unified machine learning approach that integrates flow-based and packet-based detection using Convolutional Neural Networks (CNNs) for advanced intrusion detection. Our method prioritizes flow-based detection for short flows as the first defense layer and selectively invokes packet-based detection for longer flows or uncertain cases. Uncertain predictions from the flow-based stage are identified using a confidence threshold and re-evaluated by the packet-based system.

## User Guide
For more detailed information and guidance on how to use, please read the user guide.

## Dataset
In this work, besides evaluating our model using a public dataset, we also train and test it using our own generated dataset collected from a microservices system. Unlike traditional monolithic systems where traffic collection at the router level is often sufficient, microservices require finer-grained traffic collection due to their distributed and dynamic nature. We captured traffic at the level of individual microservices to reveal variations in protocols, volumes, and unique communication patterns, enabling the construction of a dataset that accurately reflects the decentralized behavior of microservices. The dataset is publicly available [here]([https://shorturl.at/gmLTV](https://drive.google.com/drive/folders/1TU-hJmhac2oTjcB2IYI2rReBRMgGatSf?usp=sharing)).

## Attack Project Diagram

![](https://i.imgur.com/5D4JVtD.jpg)

###### tags: `flow and packet` `ML-based IDS`
