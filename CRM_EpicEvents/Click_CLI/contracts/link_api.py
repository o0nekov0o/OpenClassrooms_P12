import requests
from Click_CLI.constants import END_POINT, NULL_VALUE


def create_contracts(token, customer, total_amount, unpaid_amount, contract_state):
    params = {
        "customer": int(customer),
        "total_amount": total_amount,
        "unpaid_amount": unpaid_amount,
        "contract_state": contract_state,
    }
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.post(END_POINT["URL"] + END_POINT["CONTRACTS"], json=params, headers=headers)
    return r.status_code, r.content


def delete_contracts(token, contract_id):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.delete(END_POINT["URL"] + END_POINT["CONTRACTS"] + str(contract_id) + "/", headers=headers)
    return r.status_code, r.content


def update_contracts(token, contract_id, customer, total_amount, unpaid_amount, contract_state):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["CONTRACTS"] + str(contract_id), headers=headers).json()
    params = {"customer": r["customer"] if customer == NULL_VALUE else int(customer),
              "total_amount": r["total_amount"] if total_amount == NULL_VALUE else total_amount,
              "unpaid_amount": r["unpaid_amount"] if unpaid_amount == NULL_VALUE else unpaid_amount,
              "contract_state": r["contract_state"] if contract_state == NULL_VALUE else contract_state}
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.put(END_POINT["URL"] + END_POINT["CONTRACTS"] +
                     str(contract_id) + "/", json=params, headers=headers)
    return r.status_code, r.content


def list_all_contracts(token):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["CONTRACTS"], headers=headers)
    return r.status_code, r.content


def list_one_contract(token, contract_id):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["CONTRACTS"] + str(contract_id), headers=headers)
    return r.status_code, r.content


"""
def refresh_contracts(token):
    params = {
        "refresh": token
    }
    r = requests.post(END_POINT["URL"] + END_POINT["REFRESH"], data=params)
    return r.status_code, r.content
"""
