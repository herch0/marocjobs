from bs4 import BeautifulSoup as bs4
import requests

# emploi.ma
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
#     39 R&amp;D, gestion de projets
#     38 RH, juridique, formation
#     40 Secrétariat, assistanat
#     41 Tourisme, hôtellerie, restauration
#
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
#     955
#
#     job_filter:
#     region_filter:
#     keywords:
#     op:Rechercher
#     form_build_id:form-aw8yTAUtagEHJYAEaiskCkkZfFQs6COGThC-FwWRxF8
#     form_id:_emasearch_home_search_form

# le paramètre filter est composé ainsi: filter=tid:[id fonction] tid:[id ville]
#ici, on rechereche les métiers de l'Informatique, nouvelles technologies de Casablanca
params = {'filters': 'tid:31 tid:58'}
emploi_ma_url = 'http://www.emploi.ma/recherche-jobs-maroc'
r = requests.get(emploi_ma_url, params=params)
print(r.url)
html = bs4(r.text, 'html.parser')

#les div qui contiennent les annonces ont les classes "emasearch-result" "job-search-result"
#à l'intérieur de ces div on a un div qui contient le titre de l'annonce qui a les classes title search-title
# et à l'intérieur de ce div, on a un élément a, ce qui nous donné le sélecteur CSS suivant
#.emasearch-result.job-search-result .title.search-title a
#on passe donc ce sélecteur à la méthode select qui nous retource les éléments
#qui correspondent au sélecteur spécifié
annonces = html.select('.emasearch-result.job-search-result .title.search-title a')
for annonce in annonces:
    print(annonce['href'])
