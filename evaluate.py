import argparse
import json
import cv2
import numpy as np
from yolo.frontend import create_yolo
from yolo.backend.utils.annotation import parse_annotation
from yolo.backend.utils.eval.fscore import count_true_positives, calc_score
from PIL import Image 
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from pascal_voc_writer import Writer
from shutil import copyfile
import os
import yolo
import pytesseract
import math
import imutils
from bs4 import BeautifulSoup
import requests, time,json, re

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


DEFAULT_CONFIG_FILE = "model/regskyltar.json"
DEFAULT_WEIGHT_FILE = "model/model.h5"
DEFAULT_THRESHOLD = 0.3


argparser = argparse.ArgumentParser(
    description='Predict digits driver')

argparser.add_argument(
    '-c',
    '--conf',
    default=DEFAULT_CONFIG_FILE,
    help='path to configuration file')

argparser.add_argument(
    '-t',
    '--threshold',
    default=DEFAULT_THRESHOLD,
    help='detection threshold')

argparser.add_argument(
    '-w',
    '--weights',
    default=DEFAULT_WEIGHT_FILE,
    help='trained weight files')

argparser.add_argument(
    '-p',
    '--path',
    default='testing_images',
    help='path to images')

def create_ann(filename, image, boxes, right_label, label_list):
    copyfile(os.path.join(args.path,filename), 'test_img/'+filename)
    writer = Writer(os.path.join(args.path,filename), 224, 224)
    print(right_label)
    for i in range(len(right_label)):
    	writer.addObject(label_list[right_label[i]], boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3])
    name = filename.split('.')
    writer.save('test_ann/'+name[0]+'.xml')



def hittaskylt(skylt):
    r = requests.get("https://biluppgifter.se/fordon/" + skylt)

    soup = BeautifulSoup(r.text, "html.parser")
    data =soup.select_one("#box-data")
    name1 = data.find_all("span")
    carname=name1[3].text, name1[0].text, name1[1].text
    car = " ".join(carname)
    return car

def draw_scaled_boxes(image, boxes, car, desired_size=400):
    img_size = min(image.shape[:2])
    if img_size < desired_size:
        scale_factor = float(desired_size) / img_size
    else:
        scale_factor = 1.0
    
    h, w = image.shape[:2]
    img_scaled = cv2.resize(image, (int(w*scale_factor), int(h*scale_factor)))
    if boxes != []:
        boxes_scaled = boxes*scale_factor
        boxes_scaled = boxes_scaled.astype(np.int)
    else:
        boxes_scaled = boxes
    return draw_boxes(img_scaled, boxes_scaled, car)
        
def draw_boxes(image, boxes, car):
    for box, classes in zip(boxes, probs):
        x1, y1, x2, y2 = box
        cv2.rectangle(image, (x1,y1), (x2,y2), (0,255,0), 3)
        cv2.putText(image, 
                    car,
                    (x1, y1 - 13), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1e-3 * image.shape[0], 
                    (0,255,0), 2)
    return image 

if __name__ == '__main__':
    # 1. extract arguments
    args = argparser.parse_args()
    with open(args.conf) as config_buffer:
        config = json.loads(config_buffer.read())
    if config['train']['is_only_detect']:
        labels = ['']
    else:
        if config['model']['labels']:
            labels = config['model']['labels']
        else:
            labels = get_object_labels(config['train']['train_annot_folder'])
    print(labels)
    # 2. create yolo instance & predict
    yolo = create_yolo(config['model']['architecture'],
                       labels,
                       config['model']['input_size'],
                       config['model']['anchors'])
    yolo.load_weights(args.weights)

    # 3. read image
    write_dname = "detected"
    if not os.path.exists(write_dname): 
        os.makedirs(write_dname)
        annotations = parse_annotation(
            config['train']['valid_annot_folder'],
            config['train']['valid_image_folder'],
            config['model']['labels'],
            is_only_detect=config['train']['is_only_detect']
        )
    for filename in os.listdir(args.path):
        img_path = os.path.join(args.path,filename)
        img_fname = filename
        cap = cv2.VideoCapture(img_path)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                boxes, probs = yolo.predict(frame, float(args.threshold))
                if len(boxes)>0:
                    output_path = os.path.join(write_dname, os.path.split(img_fname)[-1])
                    label_list = config['model']['labels']
                    right_label = np.argmax(probs, axis=1) if len(probs) > 0 else [] 
                    x1= boxes[0][0]
                    x2= boxes[0][2]
                    y1= boxes[0][1]
                    y2= boxes[0][3]
                    cropped_img = frame[y1:y2, x1:x2]
                    text=pytesseract.image_to_string(cropped_img)
                    plate = re.search("^[A-Z]{3}.*[0-9]{2}([A-Z]|[0-9]){1}$",text)
                    text=text.replace(" ", "")
                    if plate and len(text)==6:
                        car = hittaskylt(text)
                        image1 = draw_scaled_boxes(frame, boxes, car)
                        cv2.imshow(text,image1)
                        cv2.waitKey(0)
                else:
                    continue
            else:
                break
