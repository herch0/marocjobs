from bs4 import BeautifulSoup as bs4
import requests
import re

def emploi_ma():
# métiers
#     28 Achats, transport, logistique
#     29 Commercial, vente
#     30 Gestion, comptabilité, finance
#     31 Informatique, nouvelles technologies
#     32 Management, direction générale
#     33 Marketing, communication
#     34 Métiers de la santé et du social
#     35 Métiers des services
#     36 Métiers du BTP
#     37 Production, maintenance, qualité
#     39 R&D, gestion de projets
#     38 RH, juridique, formation
#     40 Secrétariat, assistanat
#     41 Tourisme, hôtellerie, restauration
# Villes
#     57 Agadir
#     58 Casablanca
#     59 Fès
#     60 Laâyoune
#     61 Marrakech
#     62 Meknès
#     63 Oujda
#     64 Rabat
#     65 Settat
#     66 Tanger

# le paramètre filter est composé ainsi: filter=tid:[id fonction] tid:[id ville]
#ici, on rechereche les métiers de l'Informatique, nouvelles technologies de Casablanca
    params = {'filters': 'tid:31 tid:58'}
    emploi_ma_url = 'http://www.emploi.ma/recherche-jobs-maroc'
    r = requests.get(emploi_ma_url, params=params)

    html = bs4(r.text, 'html.parser')

#les div qui contiennent les annonces ont les classes "emasearch-result" et "job-search-result"
#on passe donc ce sélecteur à la méthode select qui nous retource les éléments
#qui correspondent au sélecteur spécifié
    annonces = html.select('.emasearch-result.job-search-result')
    for annonce in annonces:
    #on récupère la date de l'annonce avec la méthode find, on lui passe
    # l'élément qu'on recherche (un div), qui a a l'attribut class égal à "date search-date"
        date = annonce.find('div', class_='date search-date').string
        print(date)
    #on récupère le titre de l'annonce, qui est un élément h3 avec les classes "title search-title"
    # puis on récupère le texte du premier descendant, qui est un élément "a"
        lien_annonce = annonce.find('h3', class_='title search-title').contents[1]
        titre = lien_annonce.string.strip()
        href = lien_annonce['href']
        print(titre, href)
    #on récupère le nom du recruteur, même principe que le titre de l'annonce,
    #on change juste l'élément qui est un h4 et la classe
        recruteur = annonce.find('h4', class_='recruiter-name').contents[0].string
        print(recruteur.strip())
    # les résultats affichés sont ceux de la première page, pour les autres pages
    # on peut ajouter le paramètre page
    # params = {'filters': 'tid:31 tid:58', 'page': 1}

def rekrute_ma():
# Fonction

# 1 Achats / Supply Chain
# 2 Administration des ventes / SAV
# 29 Agriculture (métiers de l')
# 22 Assistanat de Direction / Services Généraux
# 3 Assurance (métiers de l')
# 4 Audit / Conseil
# 8 Avocat / Juriste / Fiscaliste
# 37 Banque (métiers de la)
# 5 Caméraman / Monteur / Preneur de son
# 27 Commercial / Vente / Export
# 7 Communication / Publicité / RP
# 6 Coursier / Gardiennage / Propreté
# 36 Distribution (métiers de la)
# 10 Enseignement
# 35 Environnement (métiers de l')
# 12 Gestion / Comptabilité / Finance
# 11 Gestion projet / Etudes / R&D
# 28 Hôtellerie / Restauration (métiers de)
# 34 Immobilier / Promotion (métiers de)
# 33 Imprimerie (métiers de l')
# 13 Informatique
# 14 Journalisme / Traduction
# 15 Logistique / Transport (métiers de)
# 16 Marketing / EBusiness
# 17 Médical / Paramédical
# 18 Méthodes / Process / Industrialisation
# 24 Métiers du Call Center
# 19 Multimédia / Internet
# 20 Production / Qualité / Sécurité / Maintenance
# 9 Responsable de Département
# 21 RH / Personnel / Formation
# 32 Santé / Social (métiers de)
# 31 Sport / Loisirs (métiers de)
# 23 Télécoms / Réseaux
# 30 Tourisme (métiers du)
# 25 Travaux / Chantiers / BTP
# 26 Urbanisme / architecture

# villes

# -1 Tout le Maroc
# 1 Agadir et région
# 2 Al Hoceima et région
# 3 Béni Mellal et région
# 4 Casablanca et région
# 5 Fès et région
# 6 Kénitra et région
# 7 Laâyoune et région
# 8 Marrakech et région
# 9 Meknès et région
# 10 Ouad Ed Dahab et région
# 11 Oujda et région
# 12 Rabat et région
# 13 Safi et région
# 14 Settat et région
# 15 Tan tan et région
# 16 Tanger et région
# -2 International

#POST data
# _STATE_:
# __EVENTARGUMENT:
# __EVENTTARGET:search
# jobOffer_Sector_2:
# jobOffer_Position[]:13
# jobOffer_Region[]:4
# searchquery:

# l'url de la recherche
    url = 'http://www.rekrute.com/offres-recherche-avancee.html'
# les paramètres qu'on doit envoyer dans la requête POST
    post_data = {'_STATE_': '', '__EVENTARGUMENT': '', '__EVENTTARGET': 'search', 'jobOffer_Sector_2': '', 'jobOffer_Position[]': '13', 'jobOffer_Region[]': '4', 'searchquery': ''}
    r = requests.post(url, data = post_data)
    # les redirection HTTP sont pris en charge par le module requests, mais
    # ce site fait une redirection javascript dans la page résulta.
    # on doit donc récupérer l'url de redirection, puis faire une nouvelle requête GET
    content = r.text
    # on doit aussi récupérer les cookies de la réponse pour les passer
    # dans notre nouvelle requête, parce que les paramètre de recherche
    # y sont enregistrés
    old_cookies = r.cookies
    url_match = re.match("<script>document.location='(.*?)';</script>", content)
    url_redirect = url_match.group(1)
    r = requests.get('http://www.rekrute.com/'+url_redirect, cookies = old_cookies)
    # pour un site plus ou moins connu, le code de leur site paraît comme créé par un stagiare
    # ce qui fait qu'il est un peu plus compliqué à parser que emploi.ma
    # si on regarde le code, on remarque que la ligne qui contient la date et titre de l'annonce, et aussi le recruteur
    # est un élément tr. Mais puisque la page entière est rempli d'éléments tr, comme s'ils n'ont
    # jamais entendu parler de div, et pire encore, ils n'ont aucune class ou id.
    # les tr qui nous intéressent ont l'attribut height fixé à 32, on va donc utiliser
    # ce point pour récupérer les annonces de la page
    html = bs4(r.text, 'html.parser')
    # print(html.body)
    tr_annonces = html.find_all('tr', attrs={'height': '32'})
    for tr in tr_annonces:
        date_annonce = ''
        titre_annonce = ''
        recruteur = ''
        #on récupère les colonnes "td" de la ligne
        tds = tr.find_all('td')
        for td in tds:
            # le td qui contient la date et le titre de l'annonce contient un tableau,
            # on teste donc si le td contient un tableau
            if td.contents[0].name == 'table':
                table = td.contents[0]
                # le tableau contient un seule ligne,
                # on récupère donc les td de cette ligne
                colonnes = table.find('tr').find_all('td')
                # la deuxième colonne contient la date, et la troisième contient
                # le lien de l'annonce
                date_annonce = colonnes[1].string
                titre_annonce = colonnes[2].find('a').string
            elif td.contents[0].name == 'a':
                # le td qui contient le lien vers le recruteur a un élément "a" comme descendant,
                # on va extraire le nom  du recruteur depuis l'attribut title, puisqu'il
                # n'est cité nulle part d'autre
                match = re.match(r'Voir toutes les offres de (.*?)$', td.contents[0]['title'])
                if match:
                    recruteur = match.group(1)
        print(date_annonce, titre_annonce + " / " + recruteur)
        # POST data
        # _STATE_:
        # __EVENTARGUMENT:2
        # __EVENTTARGET:page
        # bDirigeants:
        # recruiterid:
        # hidSortOrder:DESC
        # hidSortBy:jobOffer_PublicationDate
        # hidPage:1

        # pour aller à une autree page, on doit envoyer une requête à la page qu'on
        # récupéré plus haut, avec les paramètres citès en commentaire. le numéro de
        # la page est passé au paramètre hidPage

print('======== Annonces emploi.ma ========')
emploi_ma()
print('======== Annonces rekrute.ma ========')
rekrute_ma()
