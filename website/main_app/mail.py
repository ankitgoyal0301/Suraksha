import re
import smtplib

def send_mail(dest, message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("suraksha.pec@gmail.com", "D_V_L_P_RS321")
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,dest)):
        s.sendmail("suraksha.pec@gmail.com", dest, message)
    else:
        print("invalid email")
    s.quit()

# print(send_mail("parikhgoyal13@gmail.com", "hi"))