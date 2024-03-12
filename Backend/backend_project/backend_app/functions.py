import json
import datetime
from web3.exceptions import ContractLogicError
import os
import requests
def get_user_info(w3, user_address):
    try:
        print("Address", user_address, "is valid: ", w3.is_address(user_address)) # check if the address is valid
        wallet = w3.to_checksum_address(user_address) # make sure address is in valid format
        print("Money in wallet:", w3.eth.get_balance(wallet)) # get balance of user
        print("Money in Ether:", w3.from_wei(w3.eth.get_balance(wallet), "ether")) # get balance in ether
    except Exception as e:
        print("Error:", e)
def check_fee(w3 ,user_address , amount):
    wallet = w3.to_checksum_address(user_address)
    balance = w3.from_wei(w3.eth.get_balance(wallet), "ether")
    if amount > balance :
        return False
    return True
def open_transaction_factory():
    blockchain_dir = os.path.join(os.path.dirname(__file__), 'blockchain')
    transaction_factory_path = os.path.join(blockchain_dir, 'build/TransactionFactory.json')
    transaction_path = os.path.join(blockchain_dir, 'build/Transaction.json')

    try:
        with open(transaction_factory_path, "r") as f:
            file = json.load(f)
        abi = file["abi"]

        with open(transaction_path, "r") as f2:
            file2 = json.load(f2)
        abi2 = file2["abi"]

        return abi, abi2
    except Exception as e:
        print("Error:", e)

def read_contract_address():
    try:
        current_dir = os.path.dirname(__file__)
        blockchain_dir = os.path.join(current_dir, 'blockchain')
        contract_address_file = os.path.join(blockchain_dir, 'contractAddress.txt')

        with open(contract_address_file, "r") as f:
            contract_address = f.read()

        print("Contract address:", contract_address)
        return contract_address
    except Exception as e:
        print("Error:", e)

def get_last_transaction(contract_instance):
    # print("Deployed Contracts: ",contract_instance.functions.getDeployedTransactions().call())
    return contract_instance.functions.getDeployedTransactions().call()[-1]


def get_deployed_transactions(contract_instance):
    print("Deployed Contracts: ",contract_instance.functions.getDeployedTransactions().call())
    return contract_instance.functions.getDeployedTransactions().call()


def getTransactionContract(contract_instance, index):
    try:
        return contract_instance.functions.getDeployedTransactions().call()[index]
    except Exception as e:
        print("Error:", e)

def createTransaction(w3, contract_instance, receiver, private_key, amount, transaction_detail = {}):
    success = False
    try:
        transaction = contract_instance.functions.createTransaction(amount, receiver).build_transaction(transaction_detail)
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        transaction_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
        # print("Transaction receipt: ", transaction_receipt, "\n\n")
        # print("Transaction hash: ", transaction_receipt.blockHash)
        success = True
        return transaction_receipt, success # return transaction receipt from web3
    except ContractLogicError as e:
        error_message = str(e)
        if "execution reverted: Transaction already completed" in error_message:
            print("Error: Transaction already completed.")
            return ("Error: Transaction already completed." , success)
        else:
            message = "Error:", error_message
            print("Error:", error_message)
            return (message, success)

def executeTransaction(w3, transaction_contract_instance, private_key, transaction_detail={}):
    success = False
    try:
        transaction = transaction_contract_instance.functions.send().build_transaction(transaction_detail)
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        transaction_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
        print("Transaction receipt: ", transaction_receipt)
        success = True
        return transaction_receipt,success
    except ContractLogicError as e:
        error_message = str(e)
        if "execution reverted: Transaction already completed" in error_message:
            print("Error: Transaction already completed.")
            return ("Error: Transaction already completed." , success)
        else:
            message = "Error:", error_message
            print("Error:", error_message)
            return (message, success)
def withdrawTransaction(w3, transaction_contract_instance, private_key, transaction_detail={}):
    success = False
    try:
        transaction = transaction_contract_instance.functions.withdraw().build_transaction(transaction_detail)
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        transaction_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
        print(f"Transaction receipt: , {transaction_receipt} \n \n ")

        success = True
        return transaction_receipt,success
    except ContractLogicError as e:
        error_message = str(e)
        if "execution reverted: Transaction already completed" in error_message:
            print("Error: Transaction already completed.")
            return ("Error: Transaction already completed." , success)
        else:
            message = "Error:", error_message
            print("Error:", error_message)
            return (message, success)
def getTransactionInformation( w3, transaction_contract_instance): # 
    # print(f"Contract's Information:")
    contract_info = transaction_contract_instance.functions.returnInformation().call()
    # print(f"Sender's address: {contract_info[0]}")
    # print(f"Receiver's address: {contract_info[1]}")
    # print(f"Transfer amount: {(w3.from_wei(contract_info[2], 'ether'))}")
    # print(f"Received: {contract_info[3]}") # True , false 
    # formatted_datetime = convert_to_time(contract_info[4])
    # print(f"Timestamp: {formatted_datetime}")
    # print(f"Balance of contract: {(w3.from_wei(contract_info[5], 'ether'))}")
    return contract_info

def get_all_event(w3, transaction_contract_instance):
    event_filter = transaction_contract_instance.events.TransactionCompleted.create_filter(fromBlock='latest')
    past_events = event_filter.get_all_entries()
    result = {"sender":"","receiver":"","amount":"","timestamp":""}
    for event in past_events:
        time = convert_to_time(event['args']['timestamp'])
        result["sender"] = event['args']['sender']
        result["receiver"] = event['args']['receiver']
        result["amount"] = w3.from_wei(event['args']['amount'], 'ether')
        result["timestamp"] = time
        print("Result: ", result)
    return result
def create_user(w3):
    created_account = w3.eth.account.create()
    print("Account address:", created_account.address)
    print("Account key:", created_account._private_key.hex())
    return created_account , created_account.address
def encrypt_private_key(account, encrypted_key):
    keystore = account.encrypt(encrypted_key)
    return keystore
def decrypt_private_key(w3, keystore, encrypted_key):
    key_store = w3.eth.account.decrypt(keystore, encrypted_key)
    return key_store
def convert_to_time(time):
    dt_object = datetime.datetime.fromtimestamp(time)
    formatted_datetime = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_datetime
def transaction_json( w3, sender, value):
    return {
        "from": sender,
        "value": value,
        "gasPrice": w3.eth.gas_price,
        "chainId": w3.eth.chain_id,
        "nonce": w3.eth.get_transaction_count(sender)
    }
def get_transaction_history(w3, user_address):
    print("Transaction History: ", w3.eth.get_transaction_count(user_address))
    try:
        transactions = w3.eth.get_transaction_count(user_address)
        for i in range(transactions):
            transaction = w3.eth.get_transaction_by_index(user_address, i)
            print("Transaction Hash:", transaction.hash.hex())
            print("From:", transaction['from'])
            print("To:", transaction['to'])
            print("Value (in Wei):", transaction['value'])
            print("Gas Used:", transaction['gas'])
            print("Gas Price (in Wei):", transaction['gasPrice'])
            print("Timestamp:", w3.eth.get_block(transaction['blockNumber']).timestamp)
            print("\n")
    except Exception as e:
        print("Error:", e)

def get_data_api(params):
    url = 'https://api-sepolia.etherscan.io/api'
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['result']
    else:
        print("Error:", response.status_code)
        return response.status_code

# def run(w3 , contract_address) : 
#     abi , abi2 = open_transaction_factory()
#     transaction_contract_instance = w3.eth.contract(address= contract_address, abi=abi2)
#     contract_info = getTransactionInformation(w3 , transaction_contract_instance)
#     return contract_info