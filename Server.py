import sounddevice as sd
import soundfile as sf
from tkinter import *
import socket
import cv2
import pickle
import struct
import imutils
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

root = Tk()
root.geometry("300x150")
root.title(" Exam ")

def Connect_to_Socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('HOST IP:', host_ip)
    port = 9999
    socket_address = (host_ip, port)

    # Socket Bind
    server_socket.bind(socket_address)

    # Socket Listen
    server_socket.listen(5)
    print("LISTENING AT:", socket_address)


    # Socket Accept
    while True:
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)
        if client_socket:
            vid = cv2.VideoCapture(0)

            while (vid.isOpened()):
                img, frame = vid.read()
                frame = imutils.resize(frame, width=320)
                a = pickle.dumps(frame) #serialize frame to bytes
                message = struct.pack("Q", len(a)) + a # pack the serialized data
                # print(message)
                try:
                    client_socket.sendall(message) #send message or data frames to client
                except Exception as e:
                    print(e)
                    raise Exception(e)


                cv2.imshow('TRANSMITTING VIDEO', frame) # will show video frame on server side.
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()

def Take_input(inputtxt):
	fs = 48000
	a = inputtxt.get("1.0", "end-1c")
	# seconds
    
	duration = 15
	myrecording = sd.rec(int(duration * fs),
						samplerate=fs, channels=2)
	sd.wait()
	
	# Save as FLAC file at correct sampling rate
	return sf.write(a + '.wav', myrecording, fs)

def emailsend(inputtxt):
    #send voice recorded as email
    a = inputtxt.get("1.0", "end-1c")
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = 'raspinv4b@gmail.com'

    # storing the receivers email address
    msg['To'] = 'v.sinha15821@gmail.com'

    # storing the subject
    msg['Subject'] = "Exam Voice Recording"

    # string to store the body of the mail
    body = "The following is the recording for student with C-number "+a

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = a+ ".wav"
    attachment = open(a+".wav", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("raspinv4b@gmail.com", "sryr ybqp kezg sqie")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail("raspinv4b@gmail.com", "v.sinha15821@gmail.com", text)

    # terminating the session
    s.quit()
    
def mainlp(inputtxt):
    Take_input(inputtxt)
    emailsend(inputtxt)
    Connect_to_Socket()

l = Label(text = "Enter your C-Number : ")
inputtxt = Text(root, height = 2,
				width = 25,
				bg = "light yellow")

# Output = Text(root, height = 5,
# 			width = 25,
# 			bg = "light cyan")

Display = Button(root, height = 2,
				width = 20,
				text ="Start",
				command = lambda:mainlp(inputtxt))

l.pack()
inputtxt.pack()
Display.pack()
# Output.pack()

mainloop()
