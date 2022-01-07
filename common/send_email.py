# coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header


class EmailSmtp:
    def __init__(self):
        pass

    def send(self, target_email='', content={}):
        if not target_email:
            return {
                'status': 2,
                'message': 'target_email is empty',
            }

        if not content:
            return {
                'status': 3,
                'message': 'content is empty',
            }

        if 'title' not in content:
            return {
                'status': 4,
                'message': 'content.title not exists',
            }

        if 'content' not in content:
            return {
                'status': 5,
                'message': 'content.content not exists',
            }

        if not content['title']:
            return {
                'status': 4,
                'message': 'content.title is empty',
            }

        print("config here")
        exit()
        from_addr = '123456789@qq.com'
        password = 'password'

        # 收信方邮箱
        to_addr = str(target_email)

        # 发信服务器
        smtp_server = 'smtp.qq.com'

        text = "From: EMailServer\r\n\r\n"+str(content['content'])
        msg = MIMEText(text, 'plain', 'utf-8')

        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header(str(content['title']))

        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, 465)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()

        return {
            'status': 1,
            'message': 'success',
        }


if __name__ == '__main__':
    pass

