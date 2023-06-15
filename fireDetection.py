import cv2         
import threading   
import playsound   
import smtplib     

fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml') 

vid = cv2.VideoCapture(0) 
runOnce = False 

def play_alarm_sound_function(): 
    playsound.playsound('fire_alarm.mp3',True) 
    print("Fire alarm sonu") 

def send_mail_function(): 
    
    recipientmail = "karabulutali643@gmail.com" 
    recipientmail = recipientmail.lower() 
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("muhammetalikarabulut02@gmail.com", 'ebkixfoxmkoqpgrg') 
        server.sendmail('karabulutali643@gmail.com', recipientmail, "Uyari yangit tespit edildi 112 arayin") 
        print("Uyari maili başariyla gonderildi {}".format(recipientmail)) 
        server.close()
        
    except Exception as e:
        print(e) 
		
while(True):
    Alarm_Status = False
    ret, frame = vid.read() 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) 

    
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        print("Yangin alarmi baslatildi")
        threading.Thread(target=play_alarm_sound_function).start() 

        if runOnce == False:
            print("Mail gonderme baslatildi")
            threading.Thread(target=send_mail_function).start() 
            runOnce = True
        if runOnce == True:
            print("Mail zaten bir kez gonderildi")
            runOnce = True

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
