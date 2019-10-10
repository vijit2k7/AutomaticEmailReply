import sched
import time

import requests

from test import test1

base_url = "https://graph.microsoft.com/v1.0/me"
s = sched.scheduler(time.time, time.sleep)
access_token = "Bearer EwBwA8l6BAAUO9chh8cJscQLmU+LSWpbnr0vmwwAAQXQJDRHWQKPrW5Q7nX92thGY/+97ZIPn04L2d/e/Yr94ZWjFyT+0WLdmbOAb+cRtd3mrUJhRCQe+mNO1usqJVWlubtDME1p2CFxOLeuNwBWw85/e3CRhn5CzL3htPtuPlPjtn0pqDWA4WOBmuozYiFPBAOT4NKuVFhjEGGZydpOe5ukR4MWVzVmspQs9JHqVd3DXFQnqUfasiXzgLNNbbuLJmozln3LpMBSe7IIhVnMzbtJPfJx4GatFBuXPygUrE3YtXMNgzlDp+qVeU8zxlqQYpMtcieV721D9Cco0AivY6cJoGYvrA4ml1QwY1EmJ3tYBndhO8dCZxFXAURtCAoDZgAACDjkgkGX44bRQAIL+U/kuu4xdmVFvFJoqsck8WGKOq46zJRg8kiqj5xy31gTRu2vNtlKCho/N3KVPbpIcTD6r25RleUoAUnXwMWBbPAcgYkJjZmA6lTbhar3i5MDvJC/BEM/ES0EVwC2Eao4iqqTQZWKGAM3kIt/boq+0AosWIFyCFMK3mnsQOB3Zx7wen6tqBaKAJDE5acFiQoIJ6/k5sbOYqUNj8otrdk4VhyiOlvo2QnAlGtrbRjz9V7hnwtGMEmBSLEw3rTV0zJJXxDpnMK3VF250fQxtjNxjFr34UzE6ratfVLvBtMN64VijgfyU45qyEIHkre6YHa6y46Miy9x8ApeAJHMnh6ooh0GJQIJTf6wLGlcdy85eFVX6F8D1eaBrv+O/L9ANHfBPj0Rp5WCQCGsCIfyIuuMWqh3s/LR3WJ7K4Hgvmq7IQMI4Dkhwkr75kr9Zc6Fk60pa/+Dcws4U2jO8j0YfvyP408OJDxfE89bRzIivyOHxv8ebfmLDyjbk+ax+oWvf+3Pqa3lUw4kKwPSxkvZ8TtpOK52aJ3i09/Xd/j06XYU8w2VbJQthMoIrSMVM36aXeYrzIgwOYGIIehjJnO+dHO0NK0k5sHCej7n71PlkB4XfHec7qlJyTu+SnrXpquH4r4OGSGNUXXpUPDRpvZdgDkw+YPPaK6w384+M5b7rgafoujQklNwG+T8jP2Xyjzf77ITR1r122Y03/xEjLHihbyewI7f0jAwKBH6S00AQDYKUVwJ1rafA0FrBoFqGMYJWxuKAg=="
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
