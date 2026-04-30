import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time
import json
from web3 import Web3
import customtkinter as ctk
from PIL import Image, ImageTk

# --- THEME SETTINGS ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue") 

# --- 1. BLOCKCHAIN SETUP ---
print("🚀 Initializing System...")
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# 🔴 APNI KEY 🔴
my_private_key = "key"
# ---------------------------

try:
    with open("contract_data.json", "r") as f:
        data = json.load(f)
        contract = w3.eth.contract(address=data["contract_address"], abi=data["abi"])
    my_address = w3.eth.account.from_key(my_private_key).address
except:
    print("⚠️ Warning: Demo Mode (Blockchain not connected)")
    my_address = "0x0000"

# --- 2. AI SETUP (UPDATED FOR DEBUGGING) ---
path = 'Images'
images = []
classNames = []
last_attendance_time = {}

print(f"📂 Reading Images from folder: '{path}'...")

# Folder Check
if not os.path.exists(path):
    print(f"❌ Error: '{path}' folder nahi mila! Folder banayein.")
    exit()

myList = os.listdir(path)
print(f"📄 Files Found: {myList}") 

for cl in myList:
    if not (cl.lower().endswith(('.png', '.jpg', '.jpeg'))):
        print(f"⚠️ Skipping (Not an Image): {cl}")
        continue

    curImg = cv2.imread(f'{path}/{cl}')
    
    if curImg is None:
        print(f"❌ Error: '{cl}' ko read nahi kar pa raha. File corrupt hai!")
        continue

    curImg = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(f"👍 File Read: {cl}")

def findEncodings(images):
    encodeList = []
    print("\n🔍 Checking Images Quality & Encoding...")
    for img, name in zip(images, classNames):
        try:
            encodes = face_recognition.face_encodings(img)
            if len(encodes) > 0:
                encode = encodes[0]
                encodeList.append(encode)
                print(f"✅ Loaded & Encoded: {name}")
            else:
                print(f"⚠️ Error: '{name}' ki photo mein chehra nazar nahi aaya! (Change Photo)")
        except Exception as e:
            print(f"❌ Error loading {name}: {e}")
    print("-" * 30)
    return encodeList

encodeListKnown = findEncodings(images)
print("✅ AI Ready!")

# --- 3. MODERN UI CLASS ---
class ModernAttendanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("AI Blockchain Attendance - PRO Ver")
        self.geometry("1100x650")
        
        # Grid Layout
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=0) 
        self.grid_rowconfigure(0, weight=1)

        # --- LEFT: CAMERA SECTION ---
        self.camera_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.camera_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self.title_label = ctk.CTkLabel(self.camera_frame, text="🔒 LIVE SURVEILLANCE FEED", 
                                        font=("Roboto Medium", 16), text_color="#00E5FF")
        self.title_label.pack(anchor="w", pady=(0, 10))

        self.video_label = ctk.CTkLabel(self.camera_frame, text="", corner_radius=10)
        self.video_label.pack(expand=True, fill="both")

        self.status_bar = ctk.CTkProgressBar(self.camera_frame, height=5, progress_color="#00E5FF")
        self.status_bar.pack(fill="x", pady=10)
        self.status_bar.set(0) 

        # --- RIGHT: DASHBOARD SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=350, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar.grid(row=0, column=1, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar, text="🛡️ BLOCKCHAIN\nSECURE ATTENDANCE", 
                                       font=("Impact", 24), text_color="white")
        self.logo_label.pack(pady=30)

        self.card_frame = ctk.CTkFrame(self.sidebar, fg_color="#2b2b2b", corner_radius=15, border_width=2, border_color="#444")
        self.card_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(self.card_frame, text="IDENTIFIED STUDENT", font=("Arial", 12, "bold"), text_color="gray").pack(pady=5)
        
        self.lbl_name = ctk.CTkLabel(self.card_frame, text="Waiting...", font=("Arial", 22, "bold"), text_color="#00E5FF")
        self.lbl_name.pack(pady=5)
        
        self.lbl_status = ctk.CTkLabel(self.card_frame, text="SCANNING...", font=("Arial", 14), text_color="orange")
        self.lbl_status.pack(pady=(0, 15))

        ctk.CTkLabel(self.sidebar, text="📜 Transaction Logs", font=("Arial", 14, "bold")).pack(pady=(20, 5), anchor="w", padx=20)
        self.log_box = ctk.CTkTextbox(self.sidebar, height=200, fg_color="#222", text_color="#ccc")
        self.log_box.pack(padx=20, fill="x")

        self.btn_exit = ctk.CTkButton(self.sidebar, text="SHUTDOWN SYSTEM", fg_color="#D32F2F", hover_color="#B71C1C", command=self.close_app)
        self.btn_exit.pack(side="bottom", pady=30, padx=20, fill="x")

        self.cap = cv2.VideoCapture(0)
        self.update_camera()

    def update_camera(self):
        success, img = self.cap.read()
        if success:
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            self.status_bar.set((time.time() % 2) / 2) 
            face_detected = False

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                # --- 🛑 STRICT CHECKING ADDED HERE 🛑 ---
                # Agar match hai AUR distance 0.50 se kam hai tab hi maano
                if matches[matchIndex] and faceDis[matchIndex] < 0.50:
                    face_detected = True
                    name = classNames[matchIndex].upper()
                    
                    # Modern Box Design (Green/Cyan for Success)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 229, 255), 2)
                    
                    self.process_attendance(name)
                else:
                    # Agar shakal milti hai lekin confirm nahi hai (Unknown)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    
                    # Red Box (Warning)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2) 
                    
                    self.lbl_name.configure(text="UNKNOWN", text_color="red")
                    self.lbl_status.configure(text="NO MATCH FOUND", text_color="red")

            if not face_detected:
                self.lbl_name.configure(text="Waiting...", text_color="#00E5FF")
                self.lbl_status.configure(text="SCANNING AREA...", text_color="gray")
                self.card_frame.configure(border_color="#444")

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(700, 500))
            self.video_label.configure(image=img_tk)
            self.video_label.image = img_tk
        
        self.after(10, self.update_camera)

    def process_attendance(self, name):
        current_time = time.time()
        
        self.lbl_name.configure(text=name, text_color="#00E5FF")
        self.card_frame.configure(border_color="#00E5FF") 

        if name not in last_attendance_time or (current_time - last_attendance_time[name] > 60):
            self.lbl_status.configure(text="VERIFYING ON CHAIN...", text_color="yellow")
            self.update()

            try:
                now = datetime.now()
                date_str = now.strftime("%d-%m-%Y")
                time_str = now.strftime("%I:%M %p")

                count = contract.functions.getAttendanceCount(name).call()
                lecture_num = f"Lecture {count + 1}"

                txn = contract.functions.markAttendance(name, time_str, lecture_num, date_str).build_transaction({
                    'chainId': 1337,
                    'from': my_address,
                    'nonce': w3.eth.get_transaction_count(my_address),
                    'gasPrice': w3.eth.gas_price
                })
                signed_txn = w3.eth.account.sign_transaction(txn, private_key=my_private_key)
                tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
                
                last_attendance_time[name] = current_time
                self.lbl_status.configure(text=f"MARKED: {lecture_num}", text_color="#00FF00")
                
                self.log_box.insert("0.0", f"✅ {time_str} | {name}\n")

            except Exception as e:
                print(e)
                self.lbl_status.configure(text="BLOCKCHAIN ERROR", text_color="red")
        else:
            self.lbl_status.configure(text="ALREADY MARKED", text_color="#00FF00")

    def close_app(self):
        self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = ModernAttendanceApp()
    app.mainloop()