# RallyTrack
Our dataset can be download here: 

3 .zip files are included. rallytrack.zip only contains volleyball videos. basketball.zip and soccer.zip extend rallytrack on other sports.

All the videos are annotated following the format of MOT17.

We provide 3 related code or tools.

[[TransTrack]](https://github.com/PeizeSun/TransTrack) is the baseline. Our method is following TransTrack. We recommend you to reproduce TransTrack first.

[[denseflow]](https://github.com/open-mmlab/denseflow.git) extracts frames.

[[TrackEval]](https://github.com/JonathonLuiten/TrackEval) evaluates tracking results

## Usage

### Dataset preparation

Please download and organize RallyTrack as following: 

```
TransTrack
└── rallytrack/
    ├── train/
    ├── test/
    └── annotations/
```

Convert rallytrack to coco format.
```
python3 track_tools/convert_rallytrack_to_coco.py
```

## Citing

If you use RallyTrack in your research or wish to refer to the baseline results published here, please use the following BibTeX entries:

```BibTeX

@InProceedings{he2022rallytrack,
  title   =  {D$^3$: Duplicate Detection Decontaminator for Multiple Object Tracking on Sports Video},
  author  =  {Rui He and Zehua Fu and Qingjie Liu and Yunhong Wang and Xunxun Chen},
  journal =  {Asian Conference on Computer Vision},
  year    =  {2022}
}

```
