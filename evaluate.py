#importerar alla bibliotek
import json, cv2, re, os, yolo, pytesseract, math
import numpy as np
from yolo.frontend import create_yolo
from yolo.backend.utils.eval.fscore import count_true_positives, calc_score 
from bs4 import BeautifulSoup
import requests

#byt ut raden nedan till den path du har din tesseract nerladdad
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"   

folder="testing_images"
DEFAULT_CONFIG_FILE = "model/regskyltar.json"
DEFAULT_WEIGHT_FILE = "model/model.h5"
DEFAULT_THRESHOLD = 0.3

def initYolo(): # laddar in modellen och Konfigurerar yolo. 
    with open(DEFAULT_CONFIG_FILE) as config_buffer:
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
    yolo.load_weights(DEFAULT_WEIGHT_FILE)
    return yolo,labels

yolo,labels = initYolo()

def hittaskylt(skylt):     #funktion för att hitta information om bilen
    r = requests.get("https://biluppgifter.se/fordon/" + skylt)

    soup = BeautifulSoup(r.text, "html.parser")
    data =soup.select_one("#box-data")
    name1 = data.find_all("span")
    carname=name1[3].text, name1[0].text, name1[1].text #tar märke, modell och årsmodell 
    car = " ".join(carname)                             #sätter ihop dem
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
        
def draw_boxes(image, boxes, car): #funktion för att rita ut rutan och informationen på bilden
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

for filename in os.listdir(folder):  #går igenom alla filer i mappen
    img_path = os.path.join(folder,filename)
    cap = cv2.VideoCapture(img_path)
    while(cap.isOpened()):   #läser av videon för varje frame
        ret, frame = cap.read()
        if ret:
            boxes, probs = yolo.predict(frame, float(DEFAULT_THRESHOLD))  #bilden går igenom yolo modellen
            if len(boxes)>0:
                x1= int(int(boxes[0][0])*1.01)  #scalar upp kordinaterna från yolo med 1%
                x2= int(int(boxes[0][2])*0.99)
                y1= int(int(boxes[0][1])*1.01)
                y2= int(int(boxes[0][3])*0.99)
                cropped_img = frame[y1:y2, x1:x2] #beskär bilden till de koordinaterna
                text=pytesseract.image_to_string(cropped_img) #låter tesseract läsa av bilden
                characters=re.findall("[^A-Z0-9]+", text)  #regex hittar allt som inte är stora bokstäver och siffror
                for match in characters:
                    text=text.replace(match,"").replace(" ", "").replace("\n", "").replace("_", "") #rensar allt onödigt
                text = text.replace(" ", "").replace("\n", "").replace("_", "") 
                plate = re.match("^[A-Z]{3}.*[0-9]{2}([A-Z]|[0-9]){1}$",text) #den rena texten kontrolleras av regex igen för ett giltigt mönster
                if plate and len(text)==6: #om mönstret matchar och texen är 6 tecken
                    car = hittaskylt(text) #kan vi söka på skylten
                    image = draw_scaled_boxes(frame, boxes, car) #vi ritar ut resultatet
                    cv2.imshow(text,image) #och visar upp det
                    cv2.waitKey(0)
        else:
            break
