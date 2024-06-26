# SENSE
### 📖**Paper**

PyTorch codes for "[SENSE: Hyperspectral Video Object Tracker via Fusing Material and Motion Cues](https://ieeexplore.ieee.org/document/10387229)".

## Abstracts
> Hyperspectral video offers a wealth of material and motion cues about objects. This advantage proves invaluable in addressing the inherent limitations of generic RGB video tracking in complex scenarios such as illumination variation, background clutter, and fast motion. However, existing hyperspectral tracking methods often prioritize the material cue of objects while overlooking the motion cue contained in sequential frames, resulting in unsatisfactory tracking performance, especially in partial or full occlusion. To this end, this article proposes a novel hyperspectral video object tracker via fusing material and motion cues called SENSE that leverages both material and motion cues for hyperspectral object tracking. First, to fully exploit the material cue, we propose a spectral-spatial self-expression (SSSE) module that adaptively converts the hyperspectral image into complementary false modalities while effectively bridging the band gap. Second, we propose a cross-false modality fusion (CFMF) module that aggregates and enhances the differential-common material features derived from false modalities to arouse material awareness for robust object representations. Furthermore, a motion awareness (MA) module is designed, which consists of an awareness selector to determine the reliability of each cue and a motion prediction scheme to handle abnormal states. Extensive experiments are conducted to demonstrate the effectiveness of the proposed method over state-of-the-arts. The code will be available at https://github.com/YZCU/SENSE.

 
##  Install
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
We would like to express our sincere thanks to the excellent projects, e.g., [OTB](http://cvlab.hanyang.ac.kr/tracker_benchmark/)
The evaluation benchmark is implemented based on [OTB](http://cvlab.hanyang.ac.kr/tracker_benchmark/). We would like to express our sincere thanks to the contributors.

