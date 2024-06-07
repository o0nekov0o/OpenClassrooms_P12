import requests
from Click_CLI.constants import END_POINT, NULL_VALUE


def create_user(token, pseudo, first_name, last_name, email, role, password):
    params = {
        "pseudo": pseudo,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "role": role,
        "password": password
    }
    headers = {'accept': 'application/json', 'Authorization': 'Bearer ' + token}
    r = requests.post(END_POINT["URL"] + END_POINT["SIGNUP"], json=params, headers=headers)
    return r.status_code, r.content


def delete_user(token, user_id):
    headers = {'accept': 'application/json', 'Authorization': 'Bearer ' + token}
    r = requests.delete(END_POINT["URL"] + END_POINT["SIGNUP"] + str(user_id) + "/", headers=headers)
    return r.status_code, r.content


def update_user(token, user_id, pseudo, first_name, last_name, email, role, password):
    headers = {'accept': 'application/json', 'Authorization': 'Bearer ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["SIGNUP"] + str(user_id), headers=headers).json()
    params = {}
    params["pseudo"] = r["pseudo"] if pseudo == NULL_VALUE else pseudo
    params["first_name"] = r["first_name"] if first_name == NULL_VALUE else first_name
    params["last_name"] = r["last_name"] if last_name == NULL_VALUE else last_name
    params["email"] = r["email"] if email == NULL_VALUE else email
    params["role"] = r["role"] if role == NULL_VALUE else role
    params["password"] = password
    headers = {'accept': 'application/json', 'Authorization': 'Bearer ' + token}
    r = requests.put(END_POINT["URL"] + END_POINT["SIGNUP"] + str(user_id) + "/", json=params, headers=headers)
    return r.status_code, r.content


def list_all_user(token):
    headers = {'accept': 'application/json', 'Authorization': 'Bearer ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["SIGNUP"], headers=headers)
    return r.status_code, r.content


def list_one_user(token, user_id):
    headers = {'accept': 'application/json', 'Authorization': 'Bearer ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["SIGNUP"] + str(user_id), headers=headers)
    return r.status_code, r.content


"""
def refresh_user(token):
    params = {
        "refresh": token
    }
    r = requests.post(END_POINT["URL"] + END_POINT["REFRESH"], data=params)
    return r.status_code, r.content
"""
