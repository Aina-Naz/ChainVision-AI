import json
from web3 import Web3
from solcx import compile_standard, install_solc

# 1. Solidity Compiler Install Karna
print("Installing Solidity Compiler... (Wait)")
install_solc('0.8.0')

# 2. Solidity File Read Karna
with open("./Attendance.sol", "r") as file:
    attendance_file = file.read()

# 3. Compile Karna
print("Compiling Smart Contract...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Attendance.sol": {"content": attendance_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

bytecode = compiled_sol["contracts"]["Attendance.sol"]["AttendanceSystem"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["Attendance.sol"]["AttendanceSystem"]["abi"]

# 4. Ganache se Connect Karna
# Note: Ganache app mein "RPC SERVER" check karein, usually yehi hota hai:
ganache_url = "HTTP://127.0.0.1:7545" 
w3 = Web3(Web3.HTTPProvider(ganache_url))

if w3.is_connected():
    print("✅ Connected to Ganache Blockchain!")
else:
    print("❌ Failed to connect. Ganache open hai na?")
    exit()

# ---------------------------------------------------------
# 🔴 YAHAN APNI KEY DALEIN (Ganache se Copy karein) 🔴
my_private_key = "key"
# ---------------------------------------------------------

my_address = w3.eth.account.from_key(my_private_key).address

# 5. Contract Deploy Karna
print("Deploying Contract...")
AttendanceSystem = w3.eth.contract(abi=abi, bytecode=bytecode)

# Transaction banana
# Chain ID 1337 hota hai Ganache ka
transaction = AttendanceSystem.constructor().build_transaction({
    "chainId": 1337,
    "from": my_address,
    "nonce": w3.eth.get_transaction_count(my_address),
    "gasPrice": w3.eth.gas_price
})

# Transaction Sign karna
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=my_private_key)

# Network par bhejna
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("🎉 Contract Deployed!")
print(f"Contract Address: {tx_receipt.contractAddress}")

# 6. Address aur ABI save karna (Taake Main Project use kar sake)
data_to_save = {
    "contract_address": tx_receipt.contractAddress,
    "abi": abi
}

with open("contract_data.json", "w") as outfile:
    json.dump(data_to_save, outfile)
    print("💾 Data saved to contract_data.json")