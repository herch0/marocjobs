from bs4 import BeautifulSoup as bs4
import requests
import re
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

today = datetime.date.today()

body = "<html><meta charset='utf-8'><body>"

def menara(page = 0):
    global body
    body += "<h2>Menara</h2>"
    url = 'http://www.m-job.ma/menarajob/site/structure.jsp'
    params = {'corps': 'liste_offres', 'codeFonction': 36, 'codeRemuneration': 0, 'nbresultat': 50, 'class': 2, 'Submit': 'Chercher', 'numpage': page}
    r = requests.get(url, params=params)
    html = bs4(r.text, 'html.parser')

    match = re.search('nb=(\d+)', html.select_one('.pagination').select_one('a[href^="structure"]')['href'])
    nb = 0
    par_page = 50
    
    nb_pages = 1
    if match:
        nb = int(match.group(1))
        nb_pages = nb // par_page + 1
    annonces = html.select('.recherche .block')
    for annonce in annonces:
        titre = annonce.select_one('.result-ent-ttre').string.strip()
        lien = "http://www.m-job.ma/menarajob/site/" + annonce.find('a')['href']
        details = annonce.select_one('.result-ent-detail')
        societe = details.select_one('ul li strong').string.strip()
        date = details.select_one('span.num').string.strip()
        date_annonce = datetime.datetime.strptime(date, '%d/%m/%Y')
        body += "<h4><a href='{}'>{}</a> <small>{} - {}</small></h4>".format(lien, titre, societe, date)
        if (date_annonce.date() < today):
            return
        
    menara(page+1)

def emploi_ma(page = 0):
    global body
    body += "<h2>Emploi.ma</h2>"
    if page == 0:
        params = {'filters': 'tid:31 tid:58'}
    else:
        params = {'filters': 'tid:31 tid:58', 'page': page}
    emploi_ma_url = 'http://www.emploi.ma/recherche-jobs-maroc'
    r = requests.get(emploi_ma_url, params=params)

    html = bs4(r.text, 'html.parser')

    annonces = html.select('.emasearch-result.job-search-result')
    for annonce in annonces:
        annonce_date = annonce.find('div', class_='date search-date').string
        annonce_date = datetime.datetime.strptime(annonce_date, '%d.%m.%Y')
        if (annonce_date.date() < today):
            return
        lien_annonce = annonce.find('h3', class_='title search-title').contents[1]
        titre = lien_annonce.string.strip()
        href = 'http://www.emploi.ma' + lien_annonce['href']
        recruteur = annonce.find('h4', class_='recruiter-name').contents[0].string
        #print(annonce_date.date().isoformat(), titre, recruteur.strip())
        body += "<h4><a href='{}'>{}</a> <small>{} - {}</small></h4>".format(href, titre, recruteur, annonce_date.date().isoformat())
    emploi_ma(page+1)
# end emploi_ma

def rekrute_ma(page = 1, url_redirect = '', cookies = None):
    global body
    body += "<h2>Rekrute</h2>"
    url = 'http://www.rekrute.com/offres-recherche-avancee.html'
    if (page == 1):
        post_data = {'_STATE_': '', '__EVENTARGUMENT': '', '__EVENTTARGET': 'search', 'jobOffer_Sector_2': '', 'jobOffer_Position[]': '13', 'jobOffer_Region[]': '4', 'searchquery': ''}
        r = requests.post(url, data = post_data)
        content = r.text
        cookies = r.cookies
        url_match = re.match("<script>document.location='(.*?)';</script>", content)
        url_redirect = url_match.group(1)
        r = requests.get('http://www.rekrute.com/'+url_redirect, cookies = cookies)
    else:
        post_data = {'_STATE_': '', '__EVENTARGUMENT': page, '__EVENTTARGET': 'page', 'bDirigeants': '', 'recruiterid': '', 'hidSortOrder': 'DESC', 'hidSortBy': 'jobOffer_PublicationDate', 'hidPage': (page-1)}
        r = requests.post('http://www.rekrute.com/'+url_redirect, data = post_data, cookies = cookies)

    html = bs4(r.text, 'html.parser')

    tr_annonces = html.find_all('tr', attrs={'height': '32'})
    for tr in tr_annonces:
        if (tr.has_attr('bgcolor')):
            continue
        date_annonce = ''
        titre_annonce = ''
        recruteur = ''
        tds = tr.find_all('td')
        for td in tds:
            if len(td.contents) > 0 and td.contents[0].name == 'table':
                table = td.contents[0]
                colonnes = table.find('tr').find_all('td')
#date_annonce = colonnes[1].string.strip() + '/' + str(today.year)
                date_annonce = colonnes[1].string.strip()
                date_annonce = datetime.datetime.strptime(date_annonce, '%d/%m/%y')
                if (date_annonce.date() < today):
                    return
                titre_annonce = colonnes[2].find('a').contents[0]
                lien_annonce = 'http://www.rekrute.com/'+colonnes[2].find('a')['href']
            elif len(td.contents) > 0 and td.contents[0].name == 'a':
                match = re.match(r'Voir toutes les offres de (.*?)$', td.contents[0]['title'])
                if match:
                    recruteur = match.group(1)
                #endif
            #end elif
        #end for
        #print(date_annonce.date().isoformat(), titre_annonce + " / " + recruteur)
        body += "<h4><a href='{}'>{}</a> <small>{} - {}</small></h4>".format(lien_annonce, titre_annonce, recruteur, date_annonce.date().isoformat())
    #end for
    rekrute_ma(page + 1, url_redirect, cookies)
# end rekrute_ma

def send_mail(): 
    global body
    adr_from = "XXXXXXXXX@gmail.com"
    adr_to = "XXXXXXXX@gmail.com"
    msg = MIMEMultipart()
    msg['Subject'] = "Annonces d'emploi d'aujourd'hui"
    msg['From'] = adr_from
    msg['To'] = adr_to
    
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("XXXX@gmail.com", "XXXXXXXX")
    
    server.sendmail(adr_from, adr_to, msg.as_string())
    server.quit()
# end send_mail

emploi_ma()
rekrute_ma()

menara()

body += "</body></html>"

send_mail()
