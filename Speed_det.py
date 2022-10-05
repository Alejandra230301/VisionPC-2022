#Ejecutar builds de c++ con herramientas para cmake
#Instalar cmake AÑADIR CMAKE A PATH 
#cmd: pip install cmake
#cmd: pip install dlib



import cv2
import dlib
import time
import math

#Importar detector de objetos hard cascade
#vech.xml pre trained model for vehicles detection
carCascade= cv2.CascadeClassifier('vech.xml')
video=cv2.VideoCapture('CCTVPrueba_480p.mp4')



# Read until video is completed
while(video.isOpened()):
  # Captura frame por frame
  ret, frame = video.read()
  if ret == True:
    # Muestra los frames hechos
    cv2.imshow('Frame',frame)

    # Q para salir
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
  else: 
    break


video.release()
cv2.destroyAllWindows()

WIDTH=586
HEIGHT=480

#Se escogen dos puntos y de 
def estimateSpeed(location1,location2):
    #El calculo de la distacia entre pixeles de las posiciones de los puntos de inicio y fin
    d_pixel=math.sqrt(math.pow(location2[0]-location1[0],2)+math.pow(location2[1]-location1[1],2))
    
    #El video del tutorial dura 1 min 30s
    #Pixeles por metro creo
    ppm=8.8
    #pasar de pixel a metro
    d_meters=d_pixel/ppm
    #frames por segundo
    fps=18
    #segun los fps se pone ese 3.65
    speed=d_meters*fps*3.65
    return speed

def seguirVariosObjetos():
    #Crear el bounding box
    colCaja=(0,255,0)
    contadorFrame=0
    CurrentautoID=0
    fps=0

    carTracker={}
    numCar={}
    carLoc1={}
    carLoc2={}

    vel=[None]*1000
    out=cv2.VideoWriter('outTraffic.avi',cv2.VideoWriter_fourcc('M','J','P','G'),(WIDTH,HEIGHT))

    while True:
        tiempo_inicio=time.time()
        rc, image=video.read()

        if type(image)== type(None):
            break
        image= cv2.resize(image,(WIDTH,HEIGHT))
        imagenResult=image.copy()

        frameCont=frameCont+1
        carIDBorrar=[]

        for autoID in carTracker.keys():
            calidadTrack= carTracker[autoID].update(image)

            if calidadTrack<7:
                carIDBorrar.append(autoID)
        for autoID in carIDBorrar:
            print("Borrando el ID del carro",str(autoID)+'de la lista de seguimiento.')
            print("Borrando el ID del carro",str(autoID)+'posicion previa.')
            print("Borrando el ID del carro",str(autoID)+'posicion actual.')
            carTracker.pop(autoID,None)
            carLoc1.pop(autoID,None)
            carLoc2.pop(autoID,None)

        if not (frameCont % 10):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cars = carCascade.detectectMultiScalr(gray, 1.1,13,18,(24,24))
            for(_x,_y,_w,_h) in cars:
                x = int (_x)
                y = int (_y)
                w = int (_w)
                h = int (_h)
                
                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h
                
                matchCarId = None
                
                for carId in carTracker.keys():
                    trackerPosition = carTracker[autoID].get_position()
                    
                    t_x = int(trackerPosition.left())
                    t_y = int(trackerPosition.top())
                    t_w = int(trackerPosition.width())
                    t_h = int(trackerPosition.height())
                    
                    t_x_bar = t_x + 0.5 *t_w
                    t_y_bar = t_x + 0.5 *t_w
                    
                    if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
                        matchCarId = autoID
                if matchCarId is None:
                    print("Creando nuevo tracker" + str(CurrentautoID))
                    
                    tracker = dlib.correlation.tracker()
                    tracker.start_track(image, dlib.rectangle(x,y,x+w,y+h))
                    
                    carTracker[CurrentautoID] = tracker
                    carLoc1[CurrentautoID] = x,y,w,h
                    
                    CurrentautoID = CurrentautoID + 1
        for autoID in carTracker.keys():
            trackedPosition = carTracker[autoID].get_position()
            t_x = int(trackerPosition.left())
            t_y = int(trackerPosition.top())
            t_w = int(trackerPosition.width())
            t_h = int(trackerPosition.height())
            
            cv2.rectangle(imagenResult, (t_x, t_y), (t_x + t_w, t_y + t_h), colCaja, 4)
            
            #Comenzar desde el 40:53 https://www.youtube.com/watch?v=QlMsuCL_bXs&t=1217s&ab_channel=HitanshuSoni
                    
                            
                       
                    
            
            




