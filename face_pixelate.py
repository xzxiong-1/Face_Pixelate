import cv2
import torch
from face_ssd_infer import SSD
#from utils import vis_detections
import numpy as np
import matplotlib.pyplot as plt

def vis_detections(im, dets, thresh=0.5, show_text=True):
    """Draw detected bounding boxes."""
    class_name = 'face'
    inds = np.where(dets[:, -1] >= thresh)[0] if dets is not None else []
    if len(inds) == 0:
        return im
    for i in inds:
        bbox = dets[i, :4]
        

        #对face打马赛克
        im = np.array(im)  #转化为numpy
        # print(im1.shape)
        depts=10
        #for i range(dest)
            for i in range(int(bbox[1]),int(bbox[3]), depts): #range(a,b,c)表示从a到b 每次增加c
                for j in range(int(bbox[0]),int(bbox[2]), depts):
                    if i<h and j<w:
                        im[i:i + depts, j:j + depts] = im[i][j]

        #cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)# 如果thickness为-1表示填满

    return im
        


device = torch.device("cuda")
conf_thresh = 0.3



net = SSD("test")
net.load_state_dict(torch.load('weights/WIDERFace_DSFD_RES152.pth'))
net.to(device).eval();

writeVideo_flag = True
path="./008.mp4"
cap = cv2.VideoCapture(path)



if writeVideo_flag:
    print("视频处理中，请稍后……")
    w = int(cap.get(3))
    h = int(cap.get(4))
    fps = int(cap.get(5))
    target_size = (w, h)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out= cv2.VideoWriter('./output008.mp4', fourcc, fps, (w, h))
    while cap.isOpened():

        ret,frame=cap.read()
        if ret == True:
            img=frame
            #print(type(img))

            detections = net.detect_on_image(img, target_size, device, is_pad=False, keep_thresh=conf_thresh)
            a=vis_detections(img, detections, conf_thresh, show_text=False)
            out.write(a)
        else:
            print("OK!")
            writeVideo_flag=False
            break
    out.release()
cv2.destroyAllWindows()


