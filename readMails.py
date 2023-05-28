import imaplib
import email
import json

def read_mail():
    # IMAP sunucusuna bağlanma
    imap_server = imaplib.IMAP4_SSL('imap-mail.outlook.com', 993)

    # Kullanıcı girişi yapma
    username = 'mail'  # Hotmail (Outlook.com) e-posta adresinizi buraya girin
    password = 'password'  # E-posta hesabınızın şifresini buraya girin
    imap_server.login(username, password)

    # Posta kutusunu seçme
    imap_server.select('INBOX')  # Okunacak klasörü belirtin, genellikle 'INBOX' kullanılır

    # Okunmamış e-postaları arama
    status, messages = imap_server.search(None, 'UNSEEN')

    # Tüm e-postaları tutacak bir liste oluşturma
    emails = []

    # Her bir e-posta için bilgileri alma
    for message_id in messages[0].split():
        _, msg_data = imap_server.fetch(message_id, '(RFC822)')
        raw_email = msg_data[0][1]

        # E-postayı işleme
        msg = email.message_from_bytes(raw_email)

        # E-posta bilgilerini JSON formatına dönüştürme
        email_data = {
            'Subject': msg['Subject'],
            'From': msg['From'],
            'To': msg['To'],
            'Date': msg['Date'],
            'Body': ''
        }

        # E-posta içeriğini alma
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain' or content_type == 'text/html':
                    email_data['Body'] = part.get_payload(decode=True).decode()
                    break
        else:
            email_data['Body'] = msg.get_payload(decode=True).decode()

        # E-postayı listeye ekleme
        emails.append(email_data)

    # IMAP sunucusundan çıkma
    imap_server.logout()
    # E-postaları JSON formatında döndürme
    json_data = json.dumps(emails, indent=4, ensure_ascii=False)
    return json_data