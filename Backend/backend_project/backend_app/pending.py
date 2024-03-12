from .functions import *
from backend_app.models import HistoryModel
def get_pending_transactions(w3, user_add):
    history = []
    id = 0
    user = HistoryModel.objects.filter(user_address=user_add)
    
    for his in user:
        if not his.is_send:
            id += 1
            abi, abi2 = open_transaction_factory()
            transaction_contract_instance = w3.eth.contract(address=his.contract_address, abi=abi2)
            contract_info = getTransactionInformation(w3, transaction_contract_instance)
            amount_eth = w3.from_wei(contract_info[2], 'ether')
            
            amount_decimal = "{:.50f}".format(amount_eth).rstrip('0')
            history_item = {
                'id': id,
                'transaction_hash': his.transaction_hash,
                'receiver': contract_info[1],
                'amount': amount_decimal,
                'contract_address': his.contract_address,
                'timestamp': convert_to_time(contract_info[4])
            }
            history.append(history_item)
    
    return history