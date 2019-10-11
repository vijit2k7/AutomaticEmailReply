import requests


base_url = "https://graph.microsoft.com/v1.0/me"
access_token = "Bearer EwCAA8l6BAAUO9chh8cJscQLmU+LSWpbnr0vmwwAAQtybDEDVlX97QQckgl1OKW+ThEHNGb1LfdClsb2beb+TWQqwymWxkpWytQCdyqfqofM/RVZmZxAkOXR8xRwuzALLiES3bdpuFwZrABIXfXmCLCdpNoQ75iH2yunqna+E8Oa3MaynDi99eiInXY2dss019tiXCfDs98wLQ5PVao4jPE8L+CZbH0s+WjvmwfttnR+mgM3hAVwb3AsqTdCW8RuvONdGx2SKTtJYJvYEOn1iaJjtSnxzWdfm6j2IWuJzCHkuiTDoO9VBCgyddyTTJespDKA9urv51IsxE+OSBOi60GbxP13gpW9Yq1nWMC0D6OqyUr/zeOnlLOm3bBfu3cDZgAACCXAUT6ZCZ4IUAIdpqtd4sKVwvuX+95WtJoFYVL5vcHPnDsJvZT+IUQbXGDZ3uscYgwtWJBjNdY6YEV39WBNTQcdCvcOYRMreh6oxDCcIS0rIV3/EptWGECCLR75HsGVqJvQrlx9UIZLJhdw08lg3W0Kxfznt19MYL3lzLaXHaSGrirJPBqRe5p3TA2bHT5x/62RIFq+DA3BLmShhCBbrhzESdSOVFQQIC/b7hqRp5hUmReSVJbmWfN8l/esO8nG7eydqsjXRK5Jxhd2hnEoexNK19uZ9eitb5HU43uJjoncQsTVIa0ilp45yThaMtHyQZ7sTyFPMrgGZ8B13gWem4K3mDlGwIFggSpBEZ/a7DAPHHJuxyuhAPhFOs8i/YMZX1XDmNpyxmnjr5tk3qyWkbgtCIy0AS27fLWFek5Ok2Cm2r3DbVuzVGZfnpdf4TVyuxAaDOl2FRLBdVxIQf7WHsNJCGPjjLmu3QMzz2q24Z1FdnRAnOh7Pkd17VZs8ajooXlEolmg6F6ZmUiyZ8C5520j0t3x4I/Qvq73I0NMWPGLdz+iLN/W6e7sfvpvV0t5kQhU7X5Mhm4wycJgqWyvPkaPn8mDfNgaIvO7eqr10iPbCRpjST30zfVXlfkFHpx6wWCQg/QJQ6eG4OdI32G+uiqxrnN5+dmVjqpyg/Z83arPv8KuLCkOHIEdGD/rKR/t92UpG4b/VWmmO4a2pOH2X2/LUtV01awuZYyHj5Er4nbG0WubtM5QLk2WkJ6OHtQMO94O9PdueLAsvdhHx9abFaGPBN3cwSDrLvZwigI="
folderId = "AQMkADAwATM3ZmYAZS0yNjExAC0yN2VhLTAwAi0wMAoALgAAAzlBMbILYh1BncUUkoyetc4BAISTWp_TvDtNm2ZJDKdyLgcAAAABQn14AAAA"


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

def move_email(email_id):
    draft_response = requests.post(get_url('/messages/' + email_id + '/move'), json={"destinationId": folderId},
                                       headers={"Authorization": access_token})
    print(draft_response)
    if 200 <= draft_response.status_code < 300:
            json_response = draft_response.json()
            draft_id = json_response["id"]

            print("draft_id => " + draft_id)

            print(json_response)

    else:
            print(draft_response.content)
            print("error in api call")


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


