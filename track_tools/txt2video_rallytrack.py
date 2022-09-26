import os
import sys
import json
import cv2
import glob as gb
#from track_tools.colormap import colormap #origin
from colormap import colormap #hr

def txt2img(visual_path="visual_val_gt"):
    print("Starting txt2img")

    valid_labels = {1}
    ignore_labels = {2, 7, 8, 12}

    if not os.path.exists(visual_path):
        os.makedirs(visual_path)
    color_list = colormap()

    gt_json_path = 'rallytrack/annotations/val_half.json'
    img_path = 'rallytrack/train/'
    show_video_names = ['video_validation_0030003-FRCNN',
                    'video_validation_0050033-FRCNN']


    test_json_path = 'rallytrack/annotations/test.json'
    test_img_path = 'rallytrack/test/'
    test_show_video_names = ['video_test_0000003-FRCNN']
    if visual_path == "visual_test_predict":
        show_video_names = test_show_video_names
        img_path = test_img_path
        gt_json_path = test_json_path
    for show_video_name in show_video_names:
        img_dict = dict()
        
        if visual_path == "visual_val_gt":
            txt_path = 'mot/train/' + show_video_name + '/gt/gt_val_half.txt'
        elif visual_path == "visual_val_predict":
            txt_path = 'rallytrack_val/val/tracks/'+ show_video_name + '.txt'#hr
        elif visual_path == "visual_test_predict":
            txt_path = 'rallytrack_val/val/tracks/'+ show_video_name + '.txt'#hr
        else:
            raise NotImplementedError
        
        with open(gt_json_path, 'r') as f:
            gt_json = json.load(f)

        for ann in gt_json["images"]:
            file_name = ann['file_name']
            video_name = file_name.split('/')[0]
            if video_name == show_video_name:
                img_dict[ann['frame_id']] = img_path + file_name


        txt_dict = dict()    
        with open(txt_path, 'r') as f:
            for line in f.readlines():
                linelist = line.split(',')

                mark = int(float(linelist[6]))
                label = int(float(linelist[7]))
                vis_ratio = float(linelist[8])
                
                if visual_path == "visual_val_gt":
                    if mark == 0 or label not in valid_labels or label in ignore_labels or vis_ratio <= 0:
                        continue

                img_id = linelist[0]
                obj_id = linelist[1]
                bbox = [float(linelist[2]), float(linelist[3]), 
                        float(linelist[2]) + float(linelist[4]), 
                        float(linelist[3]) + float(linelist[5]), int(obj_id)]
                if int(img_id) in txt_dict:
                    txt_dict[int(img_id)].append(bbox)
                else:
                    txt_dict[int(img_id)] = list()
                    txt_dict[int(img_id)].append(bbox)

        for img_id in sorted(txt_dict.keys()):
            img = cv2.imread(img_dict[img_id])
            for bbox in txt_dict[img_id]:
                cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color_list[bbox[4]%79].tolist(), thickness=2)
                cv2.putText(img, "{}".format(int(bbox[4])), (int(bbox[0]), int(bbox[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_list[bbox[4]%79].tolist(), 2)
            cv2.imwrite(visual_path + "/" + show_video_name + "{:0>6d}.png".format(img_id), img)
        print(show_video_name, "Done")
    print("txt2img Done")

        
def img2video(visual_path="visual_val_gt"):
    print("Starting img2video")

    img_paths = gb.glob(visual_path + "/*.png") 
    fps = 16 
    size = (1920,1080) 
    videowriter = cv2.VideoWriter(visual_path + "_video.avi",cv2.VideoWriter_fourcc('M','J','P','G'), fps, size)

    for img_path in sorted(img_paths):
        img = cv2.imread(img_path)
        img = cv2.resize(img, size)
        videowriter.write(img)

    videowriter.release()
    print("img2video Done")


if __name__ == '__main__':
    visual_path="visual_val_predict"#origin
    #visual_path = "visual_test_predict" #hr
    if len(sys.argv) > 1:
        visual_path =sys.argv[1]
    txt2img(visual_path)
    img2video(visual_path)
