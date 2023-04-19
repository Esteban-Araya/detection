import cv2
import numpy as np
from base64 import b64decode
from PIL import Image
import io


def eliminar_puntos_cercanos(approx):
    RANGO = 20
    #approx = list(approx)
    eliminar= []
    send = []
    for i in range(len(approx)):
        # print(i)
        
        for j in range(i+1,len(approx)):
            if approx[i][0][0] + RANGO > approx[j][0][0] > approx[i][0][0] - RANGO:
                # print("approx[i][0][0] + RANGO > approx[j][0][0] > approx[i][0][0] - RANGO")
                # print(f"{approx[i][0][0] + RANGO}\t{ approx[j][0][0]}\t{approx[i][0][0] - RANGO}")
                if approx[i][0][1] + RANGO > approx[j][0][1]  > approx[i][0][1] - RANGO:
                    eliminar.append(i)
                    #print("se elimino:", approx[i][0] )
    # print("eliminar: ", eliminar)
    # print("approx1: ",approx)
    # print("wwwwwwwwwwwwww")
    approx = np.delete(approx,eliminar,axis=0)
    #print("approx2: ",approx)
    return approx

def isFlecha2(appr,image):
    
    RAN_ATRAS = 40
    RAN_ADELANTE = 50
    kernel = np.ones((5,5),np.uint8)
    #print(appr)
    puntos = len(appr)
   
    if 6 > puntos < 10:
        print("no es una flecha, por los lados")
        return False
    
    x,y,w,h = cv2.boundingRect(appr)
    flecha = image[y-17:y+h+17,x-17:x+w+17]
    
    flecha = cv2.resize(flecha,(300,300))
    
    try:
        gray = cv2.cvtColor(flecha, cv2.COLOR_BGR2GRAY)
    except:
        gray = flecha
    
    gray = cv2.bitwise_not(gray)
    difuminado = cv2.GaussianBlur(gray,(5,5),0)
    difuminado = cv2.medianBlur(difuminado,5)
    
    _,th = cv2.threshold(difuminado,150,255,cv2.THRESH_BINARY)
    th = cv2.dilate(th, kernel, iterations=5)
    th = cv2.erode(th, kernel, iterations=3)
    

    cnts,_ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# OpenCV 4
    cv2.drawContours(flecha, cnts, -1, (255,0,0), 2)
    #cv2.putText(flecha, f"cantidad: {len(approx)}",(100,100),2,0.5,(0,0,255),1,cv2.LINE_AA)
    
    
    xval = 0
    
    # print("PASE LA PRUEBA")
    for c in cnts:
        epsilon = 0.01*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        x,y,w,h = cv2.boundingRect(approx)
        
        approx = eliminar_puntos_cercanos(approx)
        # print(type(approx))
        #cv2.rectangle(flecha,(x,y),(x+w,y+h),(250,250,0),2)
        #print("largo: ", len(approx))
        pos = 1 
        # print(w,h)
        
        if (w > h):
            pos = 0

        # print("achu2") 
        xval = sorted(list(approx[:, 0, pos]))
        # print("achu")
        #abajo o izquierda
        if(xval[0] + RAN_ATRAS > xval[1]):
            
            

            if xval[-1] - RAN_ADELANTE > xval[-2]:
                
                if pos == 0:
                    print("Derecha")
                    direction = "Derecha"
                else:
                    print("abajo")
                    direction = "abajo"
                # cv2.imshow(f"flechaPro",flecha)
                # print("PASE LA PRUEBA3")
                # cv2.imshow("cannyFlecha",canny)
                return direction

        #arriba o derecha 
        if(xval[-1] - RAN_ATRAS < xval[-2]):
            
            if xval[0] + RAN_ADELANTE < xval[1]:
                if pos == 0:
                    print("Izquierda")
                    direction = "Izquierda"

                else:
                    print("arribda")
                    direction = "arribda"
                   
                # cv2.imshow(f"flechaPro",flecha)
                # print("PASE LA PRUEBA2")
                # # cv2.imshow("cannyFlecha",canny)
                return direction
        

    #cv2.imshow(f"noFlecha",flecha)     
    
    # cv2.imshow("cannyFlecha",canny)
    print("no es una flecha")
   
    return False
    
    

    


def detectArroWeb3():
    cap=cv2.VideoCapture(0)

    #image = cv2.resize(image,(500,500))
    #image = cv2.flip(image,0)
    
    #ancho = image.shape[1] #columnas
    #alto = image.shape[0] # filas
    #M = cv2.getRotationMatrix2D((ancho//2,alto//2),90,1)
    #image = cv2.warpAffine(image,M,(ancho,alto))
    k = 0
    while(True):
        vi, image = cap.read()
        ima = image.copy()
        if k == ord("s"):
            print("--------------------------------------------------------------------")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.bitwise_not(gray)
            difuminado = cv2.GaussianBlur(gray,(5,5),0)
            difuminado = cv2.medianBlur(difuminado,5)
            _,th = cv2.threshold(difuminado,150,255,cv2.THRESH_BINARY)
            th = cv2.dilate(th, None, iterations=4)
            th = cv2.erode(th, None, iterations=3)
            

            
            
            cnts,_ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# OpenCV 4
            
            # 
            # 
            cv2.drawContours(image, cnts, -1, (0,0,0), 2)
            cv2.imshow("aaa")
            for c in cnts:
                try:
                    print("a")
                    epsilon = 0.01*cv2.arcLength(c,True)
                    approx = cv2.approxPolyDP(c,epsilon,True)
                    x,y,w,h = cv2.boundingRect(approx)
                    color = (0,0,255)
                    #   if (len(approx) > 6):
                        # cv2.putText(image, f"cantidad: {len(approx)}",(x,y-25),2,1.3,(0,0,255),1,cv2.LINE_AA)
                    #cv2.rectangle(image,(x,y),(x+w,y+h),color,2)
                    if isFlecha2(approx,ima):
                        
                        color = (0,255,0)
                     
                except:
                    
                    pass
                #cv2.ellipse(image,center,axes,angle, (255,255,0))
                cv2.imshow("th",th)
                cv2.imshow("image",image)

                cv2.imshow("gray",gray)

        cv2.imshow("ima",ima)
        k = cv2.waitKey(1)
        
        if k== 27 or not vi:#27 es el ascil para esc
            break
    cap.release()
    cv2.destroyAllWindows()

def devolver_flecha(img):

    image = b64decode(img)
    
    
    image = Image.open(io.BytesIO(image))
    image = np.asarray(image)
    ima = image.copy()
    
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except:
        gray = image
    gray = cv2.bitwise_not(gray)
    difuminado = cv2.GaussianBlur(gray,(5,5),0)
    difuminado = cv2.medianBlur(difuminado,5)
    _,th = cv2.threshold(difuminado,150,255,cv2.THRESH_BINARY)
    th = cv2.dilate(th, None, iterations=4)
    th = cv2.erode(th, None, iterations=3)
    
    
    cnts,_ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# OpenCV 4
    # 
    # 
    
    #cv2.drawContours(image, cnts, -1, (255,255,0), 20 )
    
    
    

    for c in cnts:
        
        try:
            epsilon = 0.01*cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,epsilon,True)
            x,y,w,h = cv2.boundingRect(approx)
            color = (0,0,255)
            #   if (len(approx) > 6):
                # cv2.putText(image, f"cantidad: {len(approx)}",(x,y-25),2,1.3,(0,0,255),1,cv2.LINE_AA)
            
            direction = isFlecha2(approx,ima)
            cv2.rectangle(image,(x,y),(x+w,y+h),color,2)
            if direction is not False:
                cv2.destroyAllWindows()
                return direction
                
        except:
            print("se quebro tu jabru")
            pass
    cv2.destroyAllWindows()
    return "nada"
