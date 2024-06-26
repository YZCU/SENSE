# SENSE
### 📖**Paper**

PyTorch codes for "SENSE".

 
## 🧩 Install
```
git clone https://github.com/YZCU/SENSE.git
```

## Environment
 > * CUDA 11.8
 > * Python 3.9.18
 > * PyTorch 2.0.0
 > * Torchvision 0.15.0
 > * numpy 1.25.0 
 
## Prepare training and test datasets
- **RGB training datasets:**
 > * [GOT-10K](http://got-10k.aitestunion.com/downloads)
 > * [DET](http://image-net.org/challenges/LSVRC/2017/)
 > * [LaSOT](https://cis.temple.edu/lasot/)
 > * [COCO](http://cocodataset.org)
 > * [YOUTUBEBB](https://pan.baidu.com/s/1gQKmi7o7HCw954JriLXYvg) (code: v7s6)
 > * [VID](http://image-net.org/challenges/LSVRC/2017/)

-  **Hyperspectral training and test datasets:**
 > * [HOTC 2020](https://www.hsitracking.com/hot2020/)
 > * [HOTC 2022](https://www.hsitracking.com/hot2022/)

- **Note:** Please download these datasets and put them into train_dataset/dataset_name.

## 🧩 Usage
### Quick Start
- **Step I.**  Download the pretrained model: [pretrained model](https://pan.baidu.com/s/1ZW61I7tCe2KTaTwWzaxy0w) (code:) to `pretrained_models/`.
- **Step II.**  Run the `setup.py` to set the path.
```
python setup.py
```
- **Step III.**  To train a model, run `train.py` with the desired configs.
```
cd tools
python train.py
```
### Only Test
- **Step I.**  We will release the trained [sense model](https://) (code:) Please put it to the path of `tools/snapshot/`.
- **Step II.**  Run the `tools/test.py`.
```
cd tools
python test.py
```
- **Step III.**  The resulted files will be saved in the path of `tools/results/`.
### Evaluation
- **Step I.**  We will release the tracking [results](https://) (code: ).
- **Step II.**  Please download the evaluation benchmark [Toolkit](http://cvlab.hanyang.ac.kr/tracker_benchmark/) and [vlfeat](http://www.vlfeat.org/index.html) for performance evaluation.


## 🖼Results
- ### Comparison with SOTA RGB trackers
 ![image](/fig/table1.jpg)
 
- ### Comparison with SOTA hyperspectral trackers. (a) Precision plot. (b) Success plot
 ![image](/fig/fig17.jpg)

- ### Visual comparison
 ![image](/fig/fig20.jpg) 
 ![image](/fig/bus2.gif)
 ![image](/fig/student.gif)
 ![image](/fig/car3.gif)
## Contact
If you have any questions or suggestions, feel free to contact me.  
Email: yuzeng_chen@whu.edu.cn

## Citation
If you find our work helpful in your research, please consider citing it. We appreciate your support!
``` 
@article{CHEN2024102395,
title = {SENSE: Hyperspectral Video Object Tracker via Fusing Material and Motion Cues},
journal = {Information Fusion},
pages = {102395},
year = {2024},
issn = {1566-2535},
doi = {https://doi.org/10.1016/j.inffus.2024.102395},
url = {https://www.sciencedirect.com/science/article/pii/S1566253524001738},
author = {Yuzeng Chen and Qiangqiang Yuan and Yuqi Tang and Yi Xiao and Jiang He and Zhenqi Liu},
keywords = {Hyperspectral, Object tracking, Self-expression, False modality fusion, Motion awareness}
}
```
## Acknowledgement
The evaluation benchmark is implemented based on [OTB](http://cvlab.hanyang.ac.kr/tracker_benchmark/). We would like to express our sincere thanks to the contributors.

