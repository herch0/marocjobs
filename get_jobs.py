from bs4 import BeautifulSoup as bs4
import requests
import re
import datetime

today = datetime.date.today()

def emploi_ma(page = 0):
    if page != 0:
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
        href = lien_annonce['href']
        recruteur = annonce.find('h4', class_='recruiter-name').contents[0].string
        print(annonce_date.date().isoformat(), titre, recruteur.strip())
    emploi_ma(page+1)

def rekrute_ma(page = 1, url_redirect = '', cookies = None):
#POST data
# _STATE_:
# __EVENTARGUMENT:
# __EVENTTARGET:search
# jobOffer_Sector_2:
# jobOffer_Position[]:13
# jobOffer_Region[]:4
# searchquery:
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
        date_annonce = ''
        titre_annonce = ''
        recruteur = ''
        tds = tr.find_all('td')
        for td in tds:
            if len(td.contents) > 0 and td.contents[0].name == 'table':
                table = td.contents[0]
                colonnes = table.find('tr').find_all('td')
                date_annonce = colonnes[1].string.strip() + '/' + str(today.year)
                date_annonce = datetime.datetime.strptime(date_annonce, '%d/%m/%Y')
                if (date_annonce.date() < today):
                    return
                titre_annonce = colonnes[2].find('a').contents[0]
            elif len(td.contents) > 0 and td.contents[0].name == 'a':
                match = re.match(r'Voir toutes les offres de (.*?)$', td.contents[0]['title'])
                if match:
                    recruteur = match.group(1)
                #endif
            #end elif
        #end for
        print(date_annonce.date.isoformat(), titre_annonce + " / " + recruteur)
    #end for
    rekrute_ma(page + 1, url_redirect, cookies)

print('======== Annonces emploi.ma ========')
emploi_ma()
print('======== Annonces rekrute.ma ========')
rekrute_ma()
