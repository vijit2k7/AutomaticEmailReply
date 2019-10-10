import sched
import time

import requests

from request_response import test1

base_url = "https://graph.microsoft.com/v1.0/me"
s = sched.scheduler(time.time, time.sleep)
access_token = "Bearer EwBwA8l6BAAUO9chh8cJscQLmU+LSWpbnr0vmwwAAR88UDdF6vlLCgxNrK3tSzKMKg97NlNaL4n2jixViqnV+8erRXi++Cb888pxZeuLTv8VL5se5djGR2Z7/oVWueQ67V/uKT+W9oYUnpfZFIeqMnEQX8k5mbR2SVCpn5YSISqVKD3Shm5dbg08IS/mQtkAwLAg+eQrsQ3D7/1b21t7Dfri617ar/JFRk8siYiIIwrD0mDj71ZZoN52sGTbGMEafC7sTc5fY2U7xNwuMNM4Kp2KZHThTLL7WxeJiuIc8EOdNQCxLRnvaot0e5gT4V0AOt7fGsHi8rFBQDKEMMleOTxH3pGajLAw2CWrESVg0qQ/A9CWuy2qvQ97LPjHVpADZgAACEhH7qbu8naVQALuyH8GZphrPKVhZsoOHvAzrlGWd1ce3ysOT1vBEM+5ZlHTnGefN2mQ+UzmFDmVC5SxhRWC8DYE8I5qmj8Qu3mE93Rogt/dhWECw1rcSaY7PH4UytQHWF62ZlwXJ0d6eoOI6Zc11L3fYg2Dyy4R4u0oVZJ4FAqFpniB1JwKTaqPhmiMJ9hs2kK0zhVxINS1aLVpAFUG1z+tIoUMWOnVGwQsbqOVfIjcbsmR1kzzz3+f1v2wDDS4EJZi5k4TUZ3SJc9jAdhtHm5S8fJinyi1wJKp2lqqTqtJQrXraCsyKblB69ZlDr6/83HMRR7DjklJUHWPjG2xefm9ecLwb//Ec9MKGEffyTfodLqFFy5MK46HPShOaNxa2heorw7kxv7CaH/WDkxo8vPNZtOT96HETcLiFzCN50E+23A1spW/1LQJN9ipLmN3+wUepCYEJ61iNpllR5djSFe0GjKrGWB4UMp7QkezP9yr9N4BabheTTerfUfRE08Edc8YZrihcqSswFdMfPoZPQeiOedlU0JgS8nsQ+BjtKCfyaVyz/quzJ35I+BhkrMCXX20DyOCphcDdb6R4UwI19L8dLQz31/E4EiDO8W51/sCHex0qpJoAt9bFQmxpuhv29a0gepFDDfo028nTgTf8IBWESpfV2FBCTyWtiIc9tKQ7lu4izv/yRlBEyEm7qKsMxFYDq8sEUBfInlZ1asy3hJnkNCq2OyS2XbT4OweeQJX99b5YwtLbG/YuIwcUw7OPjZE0wkr1tB+wG+KAg=="
folderId = "AQMkADAwATM3ZmYAZS0yNjExAC0yN2VhLTAwAi0wMAoALgAAAzlBMbILYh1BncUUkoyetc4BAISTWp_TvDtNm2ZJDKdyLgcAAAABQn1vAAAA"


def get_url(relative_path):
    return base_url + relative_path


def create_folder():
    draft_response = requests.post(get_url('/mailFolders'), json={
        "displayName": "AutoReply"
    }, headers={"Authorization": access_token})

    if 200 <= draft_response.status_code < 300:
        json_response = draft_response.json()

        global folderId
        folderId = json_response["parentFolderId"]

        print (json_response["parentFolderId"])
    else:
        print (draft_response.content)
        print ("error in api call")


def list_emails(at, sc):
    resp = requests.get(get_url("/messages?$filter=isRead eq false"),
                        headers={"Authorization": at})
    if resp.status_code != 200:
        print (resp.content)
        print ("error in api call")
    else:
        json_response = resp.json()
        emails = json_response["value"]

        if len(emails) > 0:
            email = json_response["value"][0]

            print (email["id"])
            print (email["subject"])
            print (email["bodyPreview"])

            read_email(email["id"])

            test1(email)

            # Replace Static Values with actual ones from ML
            send_email("test sub", "test body", email["id"])
        else:
            print ("No Unread emails")

    s.enter(2, 1, list_emails, (at, sc))


def read_email(email_id):
    resp = requests.patch(get_url("/messages/" + email_id), json={"isRead": True},
                          headers={"Authorization": access_token, "Content-Type": "application/json"})
    if resp.status_code != 200:
        print ("error in api call")
        print (resp.content)
    else:
        json_response = resp.json()
        print (json_response)


def update_email(email_id, subject, body):
    resp = requests.patch(get_url("/messages/" + email_id),
                          json={"body": {"contentType": "HTML", "content": body}},
                          headers={"Authorization": access_token, "Content-Type": "application/json"})
    if resp.status_code != 200:
        print ("error in api call")
        print (resp.content)
    else:
        json_response = resp.json()
        print (json_response)

        return json_response["id"]


def send_email(subject, body, email_id):
    # create_folder()

    draft_response = requests.post(get_url('/messages/' + email_id + '/createReply'),
                                   headers={"Authorization": access_token})
    print (draft_response)
    if 200 <= draft_response.status_code < 300:
        json_response = draft_response.json()
        draft_id = json_response["id"]

        print ("draft_id => " + draft_id)

        emailid = update_email(draft_id, subject, body)

        move_email(emailid)

        print (json_response)
        # email = json_response["value"][0]
        #
        # print email["subject"]
        # print email["bodyPreview"]
    else:
        print ("error in api call")


def move_email(email_id):
    draft_response = requests.post(get_url('/messages/' + email_id + '/move'), json={"destinationId": folderId},
                                   headers={"Authorization": access_token})
    print (draft_response)
    if 200 <= draft_response.status_code < 300:
        json_response = draft_response.json()
        draft_id = json_response["id"]

        print ("draft_id => " + draft_id)

        print (json_response)
        # email = json_response["value"][0]
        #
        # print email["subject"]
        # print email["bodyPreview"]
    else:
        print (draft_response.content)
        print ("error in api call")


if __name__ == '__main__':
    s.enter(2, 1, list_emails, (access_token, s))
    s.run()
