# from .connect_w3 import connect_to_w3
# import bcrypt
# from rest_framework_simplejwt.tokens import AccessToken
# from backend_app.models import User , HistoryModel
# from rest_framework.response import Response
# from .functions import *


# def process_transaction(request):
#     w3 = connect_to_w3()
#     token = request.data.get('token')
#     to_address = request.data.get('to_address')
#     amount = request.data.get('amount')
#     pin = request.data.get('pin')
#     access_token = AccessToken(token)
#     username_from_token = access_token['username']
#     data = User.objects.get(username=username_from_token)

#     if not w3.is_address(to_address):
#         return Response({
#             'status': '400 Bad Request',
#             'message': 'Invalid to_address'
#         })

#     receiver = w3.to_checksum_address(to_address)

#     if not bcrypt.checkpw(pin.encode('utf-8'), data.pin):
#         return Response({
#             'status': '401 Unauthorized',
#             'message': 'Invalid PIN'
#         })

#     contract_address = read_contract_address()
#     abi, abi2 = open_transaction_factory()
#     contract_instance = w3.eth.contract(address=contract_address, abi=abi)
#     private_key = decrypt_private_key(w3, data.data, data.pin)
#     amount_in_wei = w3.to_wei(amount, 'ether')
#     transaction = transaction_json(w3, data.user_address, amount_in_wei)

#     if check_fee(w3, data.user_address, amount_in_wei):
#         return Response({
#             'status': '400',
#             'message': 'Not enough fee to transaction'
#         })

#     receipt, success = createTransaction(w3, contract_instance, receiver, private_key, amount_in_wei, transaction)
#     hash_block = receipt.blockHash.hex()
#     transaction_hash = receipt.transactionHash.hex()

#     if success:
#         balance = w3.from_wei(w3.eth.get_balance(data.user_address), "ether")
#         transaction_address = get_last_transaction(contract_instance)
#         history = HistoryModel(user_address=data.user_address, username=data.username, hash_block=hash_block,
#                                contract_address=transaction_address, transaction_hash=transaction_hash)
#         history.save()
#         return Response({
#             'status': '200 OK',
#             'message': 'Transaction was made successfully',
#             'data': {'balance': balance}
#         })
#     else:
#         return Response({
#             'status': '400',
#             'message': receipt
#         })
