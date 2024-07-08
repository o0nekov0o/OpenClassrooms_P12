import requests
from Click_CLI.constants import END_POINT, NULL_VALUE


def create_customer(token, information, full_name, email, phone_number, enterprise_name, commercial_contact):
    params = {
        "information": information,
        "full_name": full_name,
        "email": email,
        "phone_number": phone_number,
        "enterprise_name": enterprise_name,
        "commercial_contact": int(commercial_contact)
    }
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.post(END_POINT["URL"] + END_POINT["CUSTOMERS"], json=params, headers=headers)
    return r.status_code, r.content


def delete_customer(token, customer_id):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.delete(END_POINT["URL"] + END_POINT["CUSTOMERS"] + str(customer_id) + "/", headers=headers)
    return r.status_code, r.content


def update_customer(token, customer_id, information, full_name, email, 
                    phone_number, enterprise_name, commercial_contact):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["CUSTOMERS"] + str(customer_id), headers=headers).json()
    params = {"information": r["information"] if information == NULL_VALUE else information,
              "full_name": r["full_name"] if full_name == NULL_VALUE else full_name,
              "email": r["email"] if email == NULL_VALUE else email,
              "phone_number": r["phone_number"] if phone_number == NULL_VALUE else phone_number,
              "enterprise_name": r["enterprise_name"] if enterprise_name == NULL_VALUE else enterprise_name,
              "commercial_contact":
                  r["commercial_contact"] if commercial_contact == NULL_VALUE else int(commercial_contact)}
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.put(END_POINT["URL"] + END_POINT["CUSTOMERS"]
                     + str(customer_id) + "/", json=params, headers=headers)
    return r.status_code, r.content


def list_all_customer(token):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["CUSTOMERS"], headers=headers)
    return r.status_code, r.content


def list_one_customer(token, customer_id):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["CUSTOMERS"] + str(customer_id), headers=headers)
    return r.status_code, r.content


"""
def refresh_customer(token):
    params = {
        "refresh": token
    }
    r = requests.post(END_POINT["URL"] + END_POINT["REFRESH"], data=params)
    return r.status_code, r.content
"""
