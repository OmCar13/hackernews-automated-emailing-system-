import requests
import smtplib
import datetime
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

now = datetime.datetime.now()

content = ''

def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt +=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')
    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+ '<a href="' + tag.a.get('href') + '">' + tag.text + '</a>' + "\n" + '<br>') if tag.text!='More' else '')
    return(cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content += ('<br><br>End of Message')

print('Composing Email...')

SERVER = 'smtp.gmail.com' 
PORT = 587 
FROM = #'your email address'
TO = 'moreomcar@gmail.com'
PASS = #'your password'

msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO 
msg.attach(MIMEText(content, 'html'))

print('Inititiating Server...')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()





