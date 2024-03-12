# from web3 import Web3




# def create_and_encrypt_user(w3, encrypted_key):
#     created_account = w3.eth.account.create()
#     print("Account address:", created_account.address)
#     print("Account key:", created_account._private_key.hex())
#     keystore = created_account.encrypt(encrypted_key)
#     return keystore


# def decrypt_private_key(w3, keystore, encrypted_key):
#     private_key = w3.eth.account.decrypt(keystore, encrypted_key)
#     return private_key


