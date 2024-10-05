This project was developed as part of my work at Prodigy InfoTech for my Cybersecurity Internship.

## Project Overview

This KeyLogger project is designed to capture and log various activities on a system, including keystrokes, system information, clipboard contents, screenshots, and microphone recordings. Additionally, it retrieves browser history, monitors live website visits using DNS traffic, encrypts the collected data, and sends it via email. The tool uses industry-standard encryption for data security and follows best practices in handling sensitive information.

### Features
- **Keystroke Logging:** Captures and logs all keys pressed on the system.
- **System Information Retrieval:** Logs system details such as processor, IP addresses, operating system, and more.
- **Clipboard Monitoring:** Captures and logs clipboard contents.
- **Microphone Recording:** Records audio from the system’s microphone.
- **Screenshot Capture:** Periodically captures and saves screenshots.
- **Browser History Retrieval:** Logs browsing history from Chrome and stores the visited URLs, titles, and visit times.
- **Website Monitoring:** Monitors live website visits by sniffing DNS traffic.
- **Data Encryption:** Encrypts all sensitive data (keystrokes, system information, clipboard contents) using the **AES** (Advanced Encryption Standard) algorithm.
- **Email Reporting:** Sends the captured data (screenshots and logs) via email.

## Requirements

- Python 3.x
- Required Libraries:
  - `pynput`
  - `smtplib`
  - `socket`
  - `platform`
  - `win32clipboard`
  - `sounddevice`
  - `scipy`
  - `PIL`
  - `cryptography`
  - `requests`
  - `sqlite3`
  - `scapy`

You can install the required libraries using pip:

`pip install pynput sounddevice scipy Pillow cryptography requests scapy`


### How It Works

1. **Keystroke Logging:** 
   - Uses the `pynput` library to capture every keystroke pressed and stores it in a log file.
   
2. **System Information Retrieval:**
   - Captures system information such as hostname, public IP, and system details using the `socket` and `platform` libraries.

3. **Clipboard Monitoring:**
   - Retrieves the clipboard data using `win32clipboard` and saves it to a log file.

4. **Microphone Recording:**
   - Records audio using the `sounddevice` library and saves it as a `.wav` file.

5. **Screenshot Capture:**
   - Takes screenshots of the screen using the `PIL.ImageGrab` module and stores them as `.png` files.

6. **Browser History Retrieval:**
   - Extracts browser history from Chrome by accessing the `History` database and logs visited URLs.

7. **Website Monitoring (DNS Traffic Sniffing):**
   - Sniffs DNS queries to monitor live website visits using `scapy`.

8. **Encryption:** 
   - The sensitive data is encrypted using **AES** encryption before being sent or stored.
   - A generated encryption key is stored in a file and is used for both encryption and decryption.

9. **Email Reporting:**
   - The logs and captured data are sent to a configured email address using the `smtplib` library.

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/UzoukwuEricIyke/PRODIGY_CS_04.git
   cd PRODIGY_CS_04
   ```

2. Install the necessary dependencies:

3. Update the following variables in the script:
   - Email credentials: **Use environment variables** for storing the email address and password securely. Replace the your_email@gmail.com and your_password in the `.env` to your credentilas.
   - File paths: Ensure the file paths are correctly set for your system.

4. Generate an encryption key:
   ```bash
   python GenerateKey.py
   ```

5. Run the keylogger:
   ```bash
   python KeyLogger.py
   ```

### Security Considerations

- **Email Credentials:** Use environment variables for storing sensitive credentials like email addresses and passwords.
- **Encryption:** All sensitive data is encrypted using AES-256 before being saved or transmitted.
- **Data Deletion:** The tool automatically deletes sensitive files after encryption.

### Legal Disclaimer

This project is intended for educational purposes only. Unauthorized use of this software to capture information from other individuals without their consent is illegal and unethical. Please use this tool responsibly and in compliance with local laws.

## Contact
For questions or suggestions, please contact Uzoukwu Eric Ikenna
## Email
uzoukwuericiyke@yahoo.com
## LinkedIn
https://www.linkedin.com/in/uzoukwu-eric-ikenna/
