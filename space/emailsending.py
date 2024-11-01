import smtplib
def send_mail(message):
    email = "patrick.nuvvu@gmail.com"
    password = "rrcetpcbzhqsegmq"
    to_email = "harthik.cygnusx1@gmail.com"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(from_addr=email,
                            to_addrs=f"{to_email}",
                            msg=f'Subject:alert!!\n\n{message}')


