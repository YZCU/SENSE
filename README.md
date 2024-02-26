# SENSE (Submission to Information Fusion )
### 📖**Paper**

PyTorch codes for "[SENSE: Hyperspectral Video Object Tracker via Fusing Material and Motion Cues](https://ieeexplore.ieee.org/document/10387229)".

- Authors: [Yuzeng Chen](https://github.com/YZCU/), [Qiangqiang Yuan*](http://qqyuan.users.sgg.whu.edu.cn/), [Yuqi Tang*](https://faculty.csu.edu.cn/yqtang/zh_CN/index.htm), [Yi Xiao](https://xy-boy.github.io/), and [Jiang He](https://jianghe96.github.io/)
- Wuhan University and Central South University


## Abstracts
> Hyperspectral video offers a wealth of material and motion cues about objects. This advantage proves invaluable in addressing the inherent limitations of generic RGB video tracking in complex scenarios such as illumination variation, background clutter, and fast motion. However, existing hyperspectral tracking methods often prioritize the material cue of objects while overlooking the motion cue contained in sequential frames, resulting in unsatisfactory tracking performance, especially in partial or full occlusion. To this end, this article proposes a novel hyperspectral video object tracker via fusing material and motion cues called SENSE that leverages both material and motion cues for hyperspectral object tracking. First, to fully exploit the material cue, we propose a spectral-spatial self-expression (SSSE) module that adaptively converts the hyperspectral image into complementary false modalities while effectively bridging the band gap. Second, we propose a cross-false modality fusion (CFMF) module that aggregates and enhances the differential-common material features derived from false modalities to arouse material awareness for robust object representations. Furthermore, a motion awareness (MA) module is designed, which consists of an awareness selector to determine the reliability of each cue and a motion prediction scheme to handle abnormal states. Extensive experiments are conducted to demonstrate the effectiveness of the proposed method over state-of-the-arts. The code will be available at https://github.com/YZCU/SENSE.

 
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
- **Step I.**  We will release the trained [sense model](https://pan.baidu.com/s/1dGNo27TjOxinpTD8Tpovsw) (code:) Please put it to the path of `tools/snapshot/`.
- **Step II.**  Run the `tools/test.py`.
```
cd tools
python test.py
```
- **Step III.**  The resulted files will be saved in the path of `tools/results/`.
### Evaluation
- **Step I.**  We will release the tracking [results](https://pan.baidu.com/s/19j-bbyl7DdmQ1dJAWRzmGQ) (code: ).
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
@ARTICLE{
  author={Yuzeng Chen, Qiangqiang Yuan, Yuqi Tang, Xiao Yi, and Jiang He},
  journal={}, 
  title={SENSE: Hyperspectral Video Object Tracker via Fusing Material and Motion Cues}, 
  year={},
  volume={},
  number={},
  pages={},
  doi={}
}
```
## Acknowledgement
The evaluation benchmark is implemented based on [OTB](http://cvlab.hanyang.ac.kr/tracker_benchmark/). We would like to express our sincere thanks to the contributors.

