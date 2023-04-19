from os import path 
import cv2
import torch
from base64 import b64decode, decodebytes
from binascii import a2b_base64
from detector.detec.reconocedor import crear_diccionario_referencias, pipeline_deteccion_imagen
from PIL import Image
import io
import matplotlib.pyplot as plt

class ReconocedorFacial():
    def __init__(self) -> None:
        direction = path.dirname(path.abspath(__file__))
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        
        self.dic_referencias = crear_diccionario_referencias(
                    folder_path    = direction + "/images",
                    min_face_size  = 40,
                    min_confidence = 0.9,
                    device         = self.device,
                    verbose        = True
                  )
    
    def image_detected(self,ima):
        print(type(ima))
        print(len(ima))
        print(ima)
       
        #try:
        image = a2b_base64(ima)
        print(type(image))
        #except:
        #    print("fallo")
        #    return None
            
        fig, ax = plt.subplots(figsize=(12, 7))
        image = Image.open(io.BytesIO(image))

        detecciones = pipeline_deteccion_imagen(
        imagen = image,
        dic_referencia        = self.dic_referencias,
        min_face_size         = 20,
        thresholds            = [0.6, 0.7, 0.7],
        min_confidence        = 0.5,
        threshold_similaridad = 0.6,
        device                = self.device,
        ax                    = ax,
        verbose               = False
    )
        return detecciones
