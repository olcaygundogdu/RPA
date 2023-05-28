import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(body, subject, to):
    # Gönderici ve alıcı bilgilerini tanımlama
    sender_email = 'mail'
    sender_password = 'password'
    # Multipart mesaj oluşturma
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to
    message['Subject'] = subject
    # Mesajın gövdesini oluşturma ve eklenmesi
    message.attach(MIMEText(body, 'plain'))
    # SMTP sunucusuna bağlanma
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.starttls()
    # Gönderici hesaba giriş yapma
    smtp_connection.login(sender_email, sender_password)
    # E-postayı gönderme
    smtp_connection.sendmail(sender_email, to, message.as_string())
    # SMTP sunucusuyla bağlantıyı sonlandırma
    smtp_connection.quit()