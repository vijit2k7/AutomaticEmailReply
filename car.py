import sched
import time

import requests

from test import test1

base_url = "https://graph.microsoft.com/v1.0/me"
s = sched.scheduler(time.time, time.sleep)
access_token = "Bearer EwCAA8l6BAAUO9chh8cJscQLmU+LSWpbnr0vmwwAAQtybDEDVlX97QQckgl1OKW+ThEHNGb1LfdClsb2beb+TWQqwymWxkpWytQCdyqfqofM/RVZmZxAkOXR8xRwuzALLiES3bdpuFwZrABIXfXmCLCdpNoQ75iH2yunqna+E8Oa3MaynDi99eiInXY2dss019tiXCfDs98wLQ5PVao4jPE8L+CZbH0s+WjvmwfttnR+mgM3hAVwb3AsqTdCW8RuvONdGx2SKTtJYJvYEOn1iaJjtSnxzWdfm6j2IWuJzCHkuiTDoO9VBCgyddyTTJespDKA9urv51IsxE+OSBOi60GbxP13gpW9Yq1nWMC0D6OqyUr/zeOnlLOm3bBfu3cDZgAACCXAUT6ZCZ4IUAIdpqtd4sKVwvuX+95WtJoFYVL5vcHPnDsJvZT+IUQbXGDZ3uscYgwtWJBjNdY6YEV39WBNTQcdCvcOYRMreh6oxDCcIS0rIV3/EptWGECCLR75HsGVqJvQrlx9UIZLJhdw08lg3W0Kxfznt19MYL3lzLaXHaSGrirJPBqRe5p3TA2bHT5x/62RIFq+DA3BLmShhCBbrhzESdSOVFQQIC/b7hqRp5hUmReSVJbmWfN8l/esO8nG7eydqsjXRK5Jxhd2hnEoexNK19uZ9eitb5HU43uJjoncQsTVIa0ilp45yThaMtHyQZ7sTyFPMrgGZ8B13gWem4K3mDlGwIFggSpBEZ/a7DAPHHJuxyuhAPhFOs8i/YMZX1XDmNpyxmnjr5tk3qyWkbgtCIy0AS27fLWFek5Ok2Cm2r3DbVuzVGZfnpdf4TVyuxAaDOl2FRLBdVxIQf7WHsNJCGPjjLmu3QMzz2q24Z1FdnRAnOh7Pkd17VZs8ajooXlEolmg6F6ZmUiyZ8C5520j0t3x4I/Qvq73I0NMWPGLdz+iLN/W6e7sfvpvV0t5kQhU7X5Mhm4wycJgqWyvPkaPn8mDfNgaIvO7eqr10iPbCRpjST30zfVXlfkFHpx6wWCQg/QJQ6eG4OdI32G+uiqxrnN5+dmVjqpyg/Z83arPv8KuLCkOHIEdGD/rKR/t92UpG4b/VWmmO4a2pOH2X2/LUtV01awuZYyHj5Er4nbG0WubtM5QLk2WkJ6OHtQMO94O9PdueLAsvdhHx9abFaGPBN3cwSDrLvZwigI="
folderId = "AQMkADAwATM3ZmYAZS0yNjExAC0yN2VhLTAwAi0wMAoALgAAAzlBMbILYh1BncUUkoyetc4BAISTWp_TvDtNm2ZJDKdyLgcAAAABQn14AAAA"


def get_url(relative_path):
    return base_url + relative_path





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
            # send_email("test sub", "test body", email["id"])
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




if __name__ == '__main__':
    s.enter(2, 1, list_emails, (access_token, s))
    s.run()
