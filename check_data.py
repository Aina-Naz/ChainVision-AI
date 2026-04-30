import json
from web3 import Web3

# 1. Connect
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

if not w3.is_connected():
    print("❌ Error: Ganache band hai.")
    exit()

# 2. Contract Load
try:
    with open("contract_data.json", "r") as f:
        data = json.load(f)
        contract = w3.eth.contract(address=data["contract_address"], abi=data["abi"])
except:
    print("❌ Error: Contract data nahi mila.")
    exit()

# ---------------------------------------------------------
# 📋 YAHAN APNE SAB STUDENTS KE NAAM LIKH DEIN
# (Spelling wohi honi chahiye jo Images folder mein hai)
all_students = ["AHSAN", "AINA", "SAIQA", "ALI", "FATIMA", "HARIS","JADAM"] 
# ---------------------------------------------------------

print(f"\n🏫 Checking Attendance for ALL Students...\n")

total_present = 0

for student in all_students:
    try:
        
        count = contract.functions.getAttendanceCount(student).call()
        
        if count > 0:
            print(f"✅ STUDENT: {student} (Total: {count})")
            print("-" * 30)
            
            
            for i in range(count):
                record = contract.functions.studentRecords(student, i).call()
                
                print(f"   🔹 {record[2]} | 📅 {record[3]} | ⏰ {record[1]}")
            
            print("-" * 30 + "\n")
            total_present += 1
        else:
            
            pass

    except Exception as e:
        print(f"⚠️ Error checking {student}: {e}")

print(f"🏁 Report Finished. Total Students Present: {total_present}")