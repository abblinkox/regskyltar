# AI projekt Lindrit Koxha

Projektet består av fyra stora delar. 
Första delen är keras-yolo som används för att hitta registreringsskyltar, andra är openCV för bildredigering, 
tredje är tesseract-OCR som används för att läsa av text från bild och sista delen är webscraping för att få fram information om bilar.

## Mapparna och deras innehåll
### Model
- model.h5 - filen som innehåller den tränade modellen för registreringsskyltarna      
- classes.txt - textfil som innehåller klasserna till modellen       
- regskyltar.json – config fil till modellen    
### testing_images
- test1.mp4 - testvideon
### training
- labels - innehåller bilder och markeringar i textfiler
- annotationsXML - innehåller alla annotations i XML format
- images - innehåller datasetet som används för träningen av modellen
- annotations.py - program för att kunna skapa annotations på bilderna
- download.py - script för att ladda ner bilder från blocket
- label_tool.py - script för att konvertera yolo annotations till voc format
- renamer.py - script för att byta namn på filer
### yolo
- mappen till alla yolo filer
### evaluate.py
- Scriptet som kör programmet
## Installation och körning
### Installation
#### Program som måste installeras
- Python 3.7 64 bit med pip
- tesseract-ocr
#### Python bibliotek som måste installeras
- tensorflow 1.14.0 (pip install tensorflow == 1.14.0)
- pytesseract
- opencv-python 
- numpy 
- bs4  
- requests 
- keras 
- imgaug 
För att installera skriv pip install och namnet på biblioteket på terminalen
## Körning
- Starta evaluate.py och kör filen


