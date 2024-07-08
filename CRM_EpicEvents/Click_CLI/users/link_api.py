import requests
from Click_CLI.constants import END_POINT, NULL_VALUE


def create_user(token, username, password, first_name, last_name, email, collaborator_type):
    params = {
        "username": username,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "collaborator_type": int(collaborator_type)
    }
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.post(END_POINT["URL"] + END_POINT["USERS"], json=params, headers=headers)
    return r.status_code, r.content


def delete_user(token, user_id):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.delete(END_POINT["URL"] + END_POINT["USERS"] + str(user_id) + "/", headers=headers)
    return r.status_code, r.content


def update_user(token, user_id, username, password, first_name, last_name, email, collaborator_type):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["USERS"] + str(user_id), headers=headers).json()
    params = {"username": r["username"] if username == NULL_VALUE else username,
              "password": r["password"] if password == NULL_VALUE else password,
              "first_name": r["first_name"] if first_name == NULL_VALUE else first_name,
              "last_name": r["last_name"] if last_name == NULL_VALUE else last_name,
              "email": r["email"] if email == NULL_VALUE else email,
              "collaborator_type":
                  r["collaborator_type"] if collaborator_type == NULL_VALUE else int(collaborator_type)}
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.put(END_POINT["URL"] + END_POINT["USERS"] + str(user_id) + "/", json=params, headers=headers)
    return r.status_code, r.content


def list_all_user(token):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["USERS"], headers=headers)
    return r.status_code, r.content


def list_one_user(token, user_id):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["USERS"] + str(user_id), headers=headers)
    return r.status_code, r.content


"""
def refresh_user(token):
    params = {
        "refresh": token
    }
    r = requests.post(END_POINT["URL"] + END_POINT["REFRESH"], data=params)
    return r.status_code, r.content
"""
