import requests
from Click_CLI.constants import END_POINT, NULL_VALUE


def create_events(token, contract, event_start_date, event_end_date, support_contact, attendees, location, notes):
    params = {
        "contract": int(contract),
        "event_start_date": event_start_date,
        "event_end_date": event_end_date,
        "support_contact": int(support_contact),
        "attendees": attendees,
        "location": location,
        "notes": notes
    }
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.post(END_POINT["URL"] + END_POINT["EVENTS"], json=params, headers=headers)
    return r.status_code, r.content


def delete_events(token, event_id):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.delete(END_POINT["URL"] + END_POINT["EVENTS"] + str(event_id) + "/", headers=headers)
    return r.status_code, r.content


def update_events(token, event_id, contract, event_start_date,
                  event_end_date, support_contact, attendees, location, notes):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["EVENTS"] + str(event_id), headers=headers).json()
    params = {"contract": r["contract"] if contract == NULL_VALUE else int(contract),
              "event_start_date": r["event_start_date"] if event_start_date == NULL_VALUE else event_start_date,
              "event_end_date": r["event_end_date"] if event_end_date == NULL_VALUE else event_end_date,
              "support_contact": r["support_contact"] if support_contact == NULL_VALUE else support_contact,
              "location": r["location"] if location == NULL_VALUE else location,
              "attendees": r["attendees"] if attendees == NULL_VALUE else attendees,
              "notes": r["notes"] if notes == NULL_VALUE else notes}
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.put(END_POINT["URL"] + END_POINT["EVENTS"] + str(event_id) + "/", json=params, headers=headers)
    return r.status_code, r.content


def list_all_events(token):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["EVENTS"], headers=headers)
    return r.status_code, r.content


def list_one_event(token, event_id):
    headers = {'accept': 'application/json', 'Authorization': 'Token ' + token}
    r = requests.get(END_POINT["URL"] + END_POINT["EVENTS"] + str(event_id), headers=headers)
    return r.status_code, r.content


"""
def refresh_events(token):
    params = {
        "refresh": token
    }
    r = requests.post(END_POINT["URL"] + END_POINT["REFRESH"], data=params)
    return r.status_code, r.content
"""
