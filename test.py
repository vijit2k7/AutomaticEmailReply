from send import send_email

def test1(email):
   print("here")
   print (email)
   print (email["id"])
   print (email["subject"])
   print (email["bodyPreview"])
   id = email["id"]
   sub = email["subject"]
   send_email(sub, "Your query has been acknowledged. Please be assured we are working on it. Thankyou for your patience.", id)
