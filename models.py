# files and system
import os
import sys
import time
import random

import numpy as np
import matplotlib.pyplot as plt

# working with images
import cv2

import torchvision.transforms as transforms

import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F

from model.FCBformer.FCBmodels import FCBFormer


sys.path.insert(0, '..')

global checkpoint
checkpoint = None

def checkpointLoad():
    global checkpoint
    if checkpoint == None:
        checkpoint = torch.load("weights/ckpt_FCBFormer_CVC.pth")
        
        
    

def modeling(file_num):
    global checkpoint
    # DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") # select device for training, i.e. gpu or cp
    DEVICE = torch.device("cpu")

    # file path load
    file_name = f"source{file_num}.png"
    path_img = os.path.join("./static/uploads", file_name)
    
    # model load
    model = FCBFormer(size = 224)
    model = model.to(DEVICE)
    
    checkpointLoad()
    # checkpoint = torch.load("weights/ckpt_FCBFormer_CVC.pth")
    
    model.load_state_dict(checkpoint['net'])
    
    size = (224, 224)
    
    # eval 전 이미지 전처리
    img = cv2.imread(path_img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # 양성형 이웃 보간 (2x2 픽셀 참조하여 보간함.)
    img = cv2.resize(img, size, interpolation = cv2.INTER_LINEAR)
    
    # resize된 이미지 다시 저장
    cv2.imwrite(f"static/uploads/{file_name}", img)


    model.eval()
    eval_image = img / 255.0
    eval_image = eval_image.astype(np.float32)
    eval_image = eval_image.transpose((2,0,1))
    eval_image = torch.from_numpy(eval_image).unsqueeze(0) # Batch 채널 추가 -> (1, 3, 256, 256)
    eval_image = eval_image.to( device=DEVICE, dtype = torch.float32 )

    # we do not need to calculate gradients
    with torch.no_grad():
        # Prediction
        pred = model(eval_image)
    
    # dict형태로 데이터가 들어오는 경우가 있음 ######################################################################
    
    if isinstance(pred, dict):
        pred = torch.sigmoid(pred['out'])
        
    else:
        pred = torch.sigmoid(pred)  
    
    mask = pred.clone()
    
    # 0.5를 기준으로 마스크 만들기.
    mask[mask >= 0.5 ] = 1
    mask[mask < 0.5 ] = 0
    mask = mask.squeeze() # (256, 256)
    mask = mask.to(device = 'cpu', dtype = torch.int64).numpy() # tensor to numpy (반드시 디바이스도 변경)
    mask = np.stack( (mask,)*3, axis=-1 ) # (256,256,3)
    
    # 마스킹을 보여주기 위해 흰색처리
    real_mask = mask.copy()
    real_mask[real_mask == 1] = 255
    
    
    
    # background 투명하게 만들기
    alpha_channel = np.zeros(real_mask.shape[:2], dtype=np.uint8)

    object_pixels = np.all(real_mask == [255, 255, 255], axis=-1)

    alpha_channel[object_pixels] = 255

    transparent_img = np.dstack([real_mask, alpha_channel])
    
    cv2.imwrite(f"static/uploads/result{file_num}.png", transparent_img)
