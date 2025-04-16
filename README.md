From Flow to Packet: A Unified Machine Learning Approach for Advanced Intrusion Detection
===
This project is the repository from our paper in which we propose a unified machine learning approach that integrates flow-based and packet-based detection using Convolutional Neural Networks (CNNs) for advanced intrusion detection. Our method prioritizes flow-based detection for short flows as the first defense layer and selectively invokes packet-based detection for longer flows or cases deemed uncertain. Uncertain predictions from the flow-based stage are identified using a confidence threshold and re-evaluated by the packet-based system.
 
## How to used
1. clone the repository `git clone https://github.com/nycu-hsl/unified-flow-packet-ids.git`
2. Move to the tool directory. 
    * [Attack Recorder Tools](https://github.com/nycu-hsl/unified-flow-packet-ids/tree/main/attack_recorder) 
    * [K8s Interface Reader](https://github.com/nycu-hsl/unified-flow-packet-ids/tree/main/Kubernetes_interface_reader)
    * [Attack Reproduction](https://github.com/nycu-hsl/unified-flow-packet-ids/tree/main/attack_reproduction)
    * [DVWA deployment](https://github.com/nycu-hsl/unified-flow-packet-ids/tree/main/dvwa_deployment)
    * [Kalilinux Deployment](https://github.com/nycu-hsl/unified-flow-packet-ids/tree/main/kalilinux_deployment)
    * [Miscellaneous](https://github.com/nycu-hsl/unified-flow-packet-ids/tree/main/miscellaneous)

## User Guide
For more detailed information, please read the user guide.

## Attack Project Diagram

![](https://i.imgur.com/5D4JVtD.jpg)

###### tags: `flow and packet` `ML-based IDS`
