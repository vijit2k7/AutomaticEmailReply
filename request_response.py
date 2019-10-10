from outlook_code import send_email

def test1(email):
   print("email is",email)
   id = email["id"]
   subject = email["subject"]
   body = email["bodyPreview"]
   send_email("same subject", "test body", id)
