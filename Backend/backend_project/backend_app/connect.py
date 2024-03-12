from web3 import Web3
from decouple import config
from functions import *
from decimal import Decimal
provided_link = 'https://sepolia.infura.io/v3/181747e4369542ea9234457068381e8b'
w3 = Web3(Web3.HTTPProvider(provided_link)) # create web3 object
print("Is connected: ",w3.is_connected())

abi , abi2 = open_transaction_factory()
contract_address = read_contract_address()
print("Contract address is valid: ",w3.is_address(contract_address))
user = "0xC127911a737a5fde71CA1Edd7eD44aEBf5182e6f"
private_key = "0x" + "585c90f7cfb10ffa1ca0a4f4b0b1e738103d4675472fd693085ee9fc1800a75d"
receiver = "0x03Fa6923DF1281947C4304b0A9E7aFE9eA1775E8"
# private_key = "0xcc8c02eb43328e5476afd790e06971e6b1b013714bbf77a7a39e243ee6b308a2"
get_user_info(w3, user)
contract_instance = w3.eth.contract(address=contract_address, abi=abi) # get contract instance from web3
# print_deployed_transactions(contract_instance)
chainId = w3.eth.chain_id
amount_in_wei = w3.to_wei(0.00001, 'ether')
transaction = transaction_json(w3, user, amount_in_wei)
### for creating sending transaction
# createTransaction(w3, contract_instance, receiver, private_key, amount_in_wei, transaction)
# print_deployed_transactions(contract_instance)

### for sending transaction
send_transaction = transaction_json(w3, user, 0)
transaction_contract_instance = w3.eth.contract(address=getTransactionContract(contract_instance,3), abi=abi2)
# executeTransaction(w3,transaction_contract_instance, private_key, send_transaction)
# getTransactionInformation( w3, transaction_contract_instance)
# get_all_event(w3, transaction_contract_instance) #only return first

### getting history
# get_transaction_history(w3, user)

### Get history of transactions send to other users

user = "0x08d624674C6A69587ACD2f9EDA146605B5A01015"
params = {
    'module': 'account',
    'action': 'txlist',
    'address': user,
    'startblock': 0,
    'endblock': 99999999,
    "page": 1,
    "offset": 10,
    'sort': 'asc',
    'apikey': config('API_KEY')
}

# history = []

# offset = 0
# while True:
#     params['offset'] = 10  # Set the offset
#     params['page'] = offset + 1  # Set the page number

#     data_result = get_data_api(params)
#     if not data_result:
#         break  # If the result is empty, break the loop

#     for each_result in data_result:
#         time = convert_to_time(int(each_result['timeStamp']))
#         amount_wei = int(each_result['value'])
#         amount_eth = w3.from_wei(amount_wei, "ether")
#         amount_eth = Decimal(amount_eth)
#         if user == w3.to_checksum_address(each_result['to']):
#             amount = f"+{amount_eth}"
#         else:
#             amount = f"-{amount_eth}"
#         if each_result['isError'] == "0":
#             valid = True
#         else:
#             valid = False
#         item = {
#             "timestamp": time,
#             "amount": amount,
#             "valid": valid,
#             "to": each_result['to']
#         }
#         print(item)
#         history.append(item)

#     offset += 1
print("\n")
block = w3.eth.get_block("0x1b48dd4099a989dd0f72625a21e74fdc1aa8be0f1a36213196f298ddaffee59d", True)
print("Block number: ",block.number)
print("Hash: ",block.hash.hex())
print("Parent Hash: ",block.parentHash.hex())
print("Nonce: ", int(block.nonce.hex(), 16))
print("Timestamp: ",block.timestamp)
print("\n")
transaction = block.transactions[1]
print("From: ", transaction['from'])
print("Hash: ", transaction['hash'].hex())
print("To: ", transaction['to'])
print("Value: ", w3.from_wei(transaction['value'], "ether"))
