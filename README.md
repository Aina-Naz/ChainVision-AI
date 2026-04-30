# 🏛️ChainVision-AI
# Project Description
This project is a modern AI Attendance System that uses Face Recognition to identify students and Blockchain Technology to securely store attendance records.When a student's face is detected by the camera, the system automatically marks their attendance on a local blockchain (Ganache). Using blockchain ensures that the attendance data is permanent, transparent, and cannot be tampered with.
# 🚀 How to Setup and Run
Follow these simple steps to run the project on your laptop:
# STEPS
Step 1: Install Required Libraries
Open your terminal or command prompt and run this command to install everything you need:
pip install face-recognition opencv-python web3 customtkinter Pillow numpy<2 solcx-python bitarray ckzg regex
Step 2: Setup Ganache
Open the Ganache application on your computer.
Click on "Quickstart".
Copy the RPC Server URL (usually it is [http://127.0.0.1:7545](http://127.0.0.1:7545)).
Copy the Private Key of the first account in the list.
Step 3: Add Your Private Key
Open deploy.py and main.py in VS Code. Find the line my_private_key = "..." and paste your Ganache Private Key inside the quotes.
Step 4: Add Student Images
Put the photos of students in the Images folder.
Note: Save the photo with the person's name (Example: Ahsan.jpg, Hassan.jpg).
Step 5: Deploy the Smart Contract
Before running the main app, you must upload the smart contract to your blockchain. Run this command:
python deploy.py
This will create a contract_data.json file automatically with the new contract address.
Step 6: Run the Attendance System
Now, start the AI camera system by running:
python main.py
The camera window will open. Once it recognizes a face, it will send the data to the blockchain.
Step 7: Check Attendance Records
To see the list of all attendances stored on the blockchain, run the data checker script:
python check_data.py
🛠️ Key Libraries Used
face-recognition: To detect and identify faces.
opencv-python: To handle the camera feed.
web3: To connect Python with the Blockchain.
customtkinter: To create the modern Dark Mode user interface.
solcx-python: To compile the Solidity Smart Contract.
Pillow: To process images for the UI.
Project Features
✅ Real-time Face Detection: High accuracy identification.
✅ Secure Records: Attendance is saved on a decentralized ledger.
✅ Modern UI: Easy-to-use dashboard with live logs.
✅ Anti-Duplicate: Only marks attendance once per minute to avoid spam.
