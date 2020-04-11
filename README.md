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
Klona denna github till din dator
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
### Körning
- Starta evaluate.py och kör filen
## Hur fungerar det?
Projektet kan delas upp i 4 delar:
- Tränade modellen 
- Bildhanteringen
- OCR
- Web Scraping
### Tränade modellen
Jag har använt denna [Google Colab](https://colab.research.google.com/drive/1UK3MejBT9bzFbgmBVmBEmUR7CyC9wqTk) fil för att träna min modell. Jag har tagit fram mitt dataset för träningen av modellen genom ett script som hämtade bilder från blocket.
### Bildhanteringen
Jag har använt openCV för att öppna och redigera bilder. OpenCV analyserar varje frame i en video. Varje frame i videon går igenom modellen, och om modellen hittar en registreringsskylt i bilden får vi ut koordinater där registreringsskylten är. Bilden kommer då att beskäras  till de koordinaterna. 
### OCR
När jag fått en bild på endast registreringsskylten kör jag tesseract-OCR på bilden för att få ut bilens registreringsnummer. Regex används också för att se till att texten jag får ut passar in i möstret (3 bokstäver + 2 siffror + siffra/bokstav). 
### Web Scraping 
När jag fått ut ett registreringsnummer som passar in i mönstret använder jag mig av bs4 för att hämta information om bilen från biluppgifter.se. Informationen ritas sedan ut på bilden.
### En förenklad bild av hela processen: 
Bild -> objektigenkänning -> bild beskärs -> OCR läser text -> Regex tittar om mönstret passar -> bs4 -> Bilens info ritas på bild 
## Problem under arbetet
Det uppstod flera problem under arbetet, här är några och hur jag löste dem:
- Texten som OCR hittade i bilderna stämde inte in i möstret av en vanlig registreringsskylt. För att kunna få ut information om bilar måste texten stämma in i möstret och därför använde jag regular expressions (Regex). Regex tittar om texten från OCR stämmer in i möstret och kan  på så sätt godkänna texten så att den kan användas för att söka upp information.
- Ett liknande problem var att även om texten stämde in på mönstret så kunde den vara för lång, tex. att det fanns en bokstav för mycket i mitten osv. En enkel IF-sats i koden löste detta problem då den tittade om texten matchade regex möstret och om den hade 6 st tecken.
## Förbättringsmöjligheter
Jag anser att detta projekt har förbättringsmöjligheter. Här är några:
- Då datasetet som modellen är tränad ifrån är ifrån bilar från blocket och inte bilar på trafiken är den inte så träffsäker som den behöver vara. Modellen skulle alltså kunna tränas på ett dataset från bilar i riktig trafik. Anledningen till att jag inte gjorde detta är at det är väldigt svårt att hitta ett så stort dataset från bilar i trafik.
- Tesseract-OCR fungerar inte optimalt då bokstäverna på registreringsskyltarna måste nästan alltid vara raka. Detta är något som nästan aldrig händer och därför får man inte bra avläsningar på många bilder. För att lösa detta måste bilderna manipuleras för att få bort vinklarna. Jag vet inte för tillfället hur man gör det men det är en ide för framtiden. 
- Prestandan på programmet är också en förbätrringsmöjlighet, då programmet nu tar lång tid för att få ut resultat samt att programmet kör på väldigt låga FPS.
## Utvecklingsmöjligheter
Detta projekt skulle kunna integreras i olika dashcams på bilar, något som skulle kunna vara användbart för tex. polisen. Detta förutsätter såklart att projektet utvecklas tills det blir väldigt träffsäkert och snabbt. Detta skulle också kunna integreras i hastighetskameror, genom att direkt kunna skicka böter till ägarna av fortkörande bilar. 
