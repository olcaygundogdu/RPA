import json
from readMails import read_mail
from sendMail import send_mail
from preProcessing import preProcessing
import joblib
import datetime

if __name__ == '__main__':
    unread_mail = json.loads(read_mail())
    model = joblib.load('model.pkl')
    with open('mail_replies.json', encoding='utf-8') as json_file:
        replies = json.load(json_file)
    for mail in unread_mail:
        try:
            test = preProcessing(mail['Body'])
            pred = model.predict(test)
            for reply in replies:
                if pred == reply['title']:
                    send_mail(body=reply['body'], subject=mail['Subject'], to=mail['From'])
                    kayit = {"Mail": str(mail['Body']),
                             "Subject": str(mail['Subject']),
                             "Customer": str(mail['From'].split('<')[1].rstrip('>')),
                             "Send": str(reply['body']),
                             "Mail Date": str(mail['Date']),
                             "Send Date": str(datetime.datetime.now())}
                    with open('kayit.json', encoding='utf-8') as kayit_json:
                        kayit_dosya = json.load(kayit_json)
                    kayit_dosya.append(kayit)
                    with open('kayit.json', 'w', encoding='utf-8') as json_dosya:
                        json.dump(kayit_dosya, json_dosya, ensure_ascii=False, indent=4)
                    print(f"{mail['From'].split('<')[1].rstrip('>')} kişisine mail gönderildi.")
        except:
            message = 'Üzgünüm, sistemsel bir sorundan kaynaklı şu anda e-postanıza cevap veremiyoruz. Lütfen daha sonra bizimle tekrar iletişime geçiniz. Anlayışınız için teşekkür ederiz. İyi günler.'
            send_mail(body=message, subject=mail['Subject'], to=mail['From'])
            print(f"{mail['From'].split('<')[1].rstrip('>')} kişisine mail gönderildi.")
        print('İşlem başarıyla tamamlandı.')
