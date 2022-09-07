import cv2 as cv
import numpy as np
import pyautogui as pg

cam = cv.VideoCapture(0)

#Objetos na cor laranja move o mouse
lower_laranja = np.array([5,100,100])
upper_laranja = np.array([15,255,255])

#Objetos na cor verde são usados para clicar com o botão esquerdo
lower_verde = np.array([50,100,100])
upper_verde = np.array([80,255,255])

#Objetos na cor amarela são usados para clicar com o botão direito
lower_amarelo = np.array([100,100,20])
upper_amarelo = np.array([40,255,255])

while(True):
        #Ativa a câmera        
        ret,frame = cam.read()
        #Espelha a imagem
        frame = cv.flip(frame,1)

        #Técnica para "suavizar" a imagem
        image_smooth = cv.GaussianBlur(frame,(7,7),0)

        #Define ROI
        marcara = np.zeros_like(frame)
        marcara[100:350,100:350] = [255,255,255]
        image_roi = cv.bitwise_and(image_smooth,marcara)

        #Cria o retângulo onde controlamos o mouse
        cv.rectangle(frame,(0,50),(600,400),(0,0,255),2)

        #Limita imagem para cor laranja entre lower e upper
        image_hsv = cv.cvtColor(image_roi,cv.COLOR_BGR2HSV)
        image_threshold = cv.inRange(image_hsv,lower_laranja,upper_laranja)

        #Encontra os contornos
        contours,heirarchy = cv.findContours(image_threshold, \
                                                           cv.RETR_TREE, \
                                                           cv.CHAIN_APPROX_NONE)

        #Encontra o índice do contorno mais largo
        if(len(contours)!=0):
                areas = [cv.contourArea(c)  for c in contours]
                max_index = np.argmax(areas)
                cnt = contours[max_index]
 
                
                M = cv.moments(cnt)
                if(M['m00']!=0):
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        #Cria o ponteiro verde com radius = 8 
                        cv.circle(frame, (cx,cy),8,(0,255,0),-1)

                        # Movimento do cursor
                        if cx < 150:
                                dist_x = -20
                        elif cx > 250:
                                dist_x = 20
                        else:
                                dist_x = 0

                        if cy < 150:
                                dist_y = -20
                        elif cy > 250:
                                dist_y = 20
                        else:
                                dist_y = 0
                        pg.FAILSAFE = False

                        #Move o ponteiro do mouse para um ponto da tela relativa a atual posição
                        pg.moveRel(dist_x,dist_y,duration=0.25)

                # Verifica o botão esquerdo do mouse
                image_threshold_verde = cv.inRange(image_hsv, lower_verde, upper_verde)
                contours_verde,heirarchy = cv.findContours(image_threshold_verde,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)                                         

                if(len(contours_verde)!=0):
                        pg.click()
                        cv.waitKey(1000)


                # Verifica o botão direito do mouse
                image_threshold_amarelo = cv.inRange(image_hsv, lower_amarelo, upper_amarelo)
                contours_amarelo,heirarchy = cv.findContours(image_threshold_amarelo,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)

                if(len(contours_amarelo)!=0):
                        pg.click(button='right')
                        cv.waitKey(1000)                                                    

        cv.imshow('Frame',frame)

        #Tecla ESC para finalizar o programa
        if cv.waitKey(10) == 27:
                break

cam.release()
cv.destroyAllWindows()