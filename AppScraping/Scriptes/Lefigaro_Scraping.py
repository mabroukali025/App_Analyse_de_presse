import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import locale
import pandas as pd
import time
import re
from typing import Optional
from datetime import datetime, timedelta
import locale
import os
from AppScraping.models import Article 
import threading

url = 'https://www.lefigaro.fr/'

input_csv_file = "LefigaroVF.csv"
output_file="Lefigaro.xlsx"
output_excel_file = "LefigaroSansDoub.xlsx"
#date_exportation_f = datetime.datetime.today().strftime("%d %B %Y , %H:%M:%S") 



def fonction_date_exportation():
 import locale
 locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
 from datetime import datetime
 Date_Exportation = datetime.now()
 return Date_Exportation

scraping_active = True
date_exportation=fonction_date_exportation().strftime("%Y-%m-%d %H:%M:%S")
class WebDriverSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if WebDriverSingleton._instance is None:
            chrome_options = Options()
            chrome_options.add_argument("--disable-features=NotificationPermissions")
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("start-maximized")
            chrome_options.add_argument("--headless")
            
            
            import locale
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
            
            WebDriverSingleton._instance = webdriver.Chrome(options=chrome_options)
        return WebDriverSingleton._instance

    @staticmethod
    def quit_instance():
        if WebDriverSingleton._instance is not None:
            WebDriverSingleton._instance.quit()
            WebDriverSingleton._instance = None






################################################ Initailisation des variables   ########################"
title_accueil='Non Trouvee'
title='Non Trouvee'
link_element='Non Trouvee'
date_publication='Non Trouvee'
auteur_name='Non Trouvee'
p='Non Trouvee'
has_figure='Non'
Sous_Actualite='Non Trouvee'
categorie_text='Non Trouvee'
duree='Non Trouvee'

#date_str = datetime.today().strftime("%d %B %Y , %H:%M:%S") 

################################################################"  Create de Article #######################"
def creer_article(titre_page_accueil, titre, lien, date_text, auteur_name, paragraphe, has_image, Actualite, Date_Exportation, categorie, order):

    article = Article(
        titre_page_accueil=titre_page_accueil,
        titre=titre,
        lien=lien,
        date_publication=date_text,
        nom_auteur=auteur_name,
        description_article=paragraphe,
        statut_image=has_image,
        actualite=Actualite,
        date_exportation=Date_Exportation,
        categorie=categorie,
        ordre_actualite=order,
    )
    article.save()

    return article
################################################# convert string to date #############################
import datetime
import locale




def convert_string_to_datetime(date_str):
    try:
        # Liste de formats de date possibles en français
        date_formats_fr = [
            '%d %B %Y , %H:%M:%S',   # Format comme '12 juillet 2024 , 13:46:03'
            '%d %B %Y , %H:%M'       # Format comme '12 juillet 2024 , 13:46'
            # Ajoutez d'autres formats au besoin
        ]

        # Définir la locale en français
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

        # Essayer chaque format jusqu'à ce que la conversion réussisse
        for fmt in date_formats_fr:
            try:
                date_obj = datetime.datetime.strptime(date_str, fmt)
                # Si le format contient des secondes, les retirer
                date_obj = date_obj.replace(second=0, microsecond=0)
                # Convertir l'objet datetime en chaîne au format ISO 8601
                return date_obj.strftime('%Y-%m-%dT%H:%M:%S')
            except ValueError:
                pass
        
        # Si aucun format ne correspond
        raise ValueError(f"Chaîne de date '{date_str}' ne correspond à aucun format attendu.")

    except ValueError as e:
        # Gérer les erreurs de conversion ici
        print(f"Erreur lors de la conversion de la chaîne de date : {e}")
        return None       
####################################################################################################################################
def supprimer_caracteres_debut(nombre, chaine):
    if nombre >= len(chaine):
        return ""  # Retourner une chaîne vide si le nombre de caractères à supprimer est supérieur ou égal à la longueur de la chaîne
    
    return chaine[nombre:]
#####################################################################################################################################
def supprimer_espaces_debut(phrase):
    return phrase.lstrip()
#######################################  Extraire la duree de publication d'un article d'apres la date de pub il y a 4 heures  sen############################################################################"
def extraire_secondes(chaine: str) -> int:
    import re
    from typing import Optional
    # Initialiser les variables pour les heures et minutes
    heures = 0
    minutes = 0

    # Expression régulière pour extraire les heures et les minutes
    regex = r"(\d+)\s*(heure|heures|minute|minutes)"
    
    matches = re.findall(regex, chaine)

    # Parcourir les correspondances trouvées
    for match in matches:
        nombre, unite = match
        nombre = int(nombre)
        if unite in ["heure", "heures"]:
            heures += nombre
        elif unite in ["minute", "minutes"]:
            minutes += nombre

    # Convertir heures et minutes en secondes
    total_secondes = (heures * 3600) + (minutes * 60)
    
    return total_secondes

############################################################# convertir un nombre des secondes a une dateTime ##############################

################################################# cree une date complet d'apres la chaine "hier a 07:00" #######################"
def joindre_date_et_partie_heure(chaine: str) -> str:
    import datetime 
    # Obtenir la date d'aujourd'hui
    date_aujourdhui = datetime.datetime.today()
    # Si la chaîne contient 'hier', obtenir la date d'hier
    if 'hier' in chaine:
        date_aujourdhui -= timedelta(days=1)
    # Séparer la partie de l'heure de la chaîne
    partie_heure = chaine.split('à')[-1].strip()
    # Formater la date et la partie de l'heure
    date_formatee = date_aujourdhui.strftime("%Y %B %d") + " , " + partie_heure + ":00"
    return date_formatee
############################################## convertir la forme date : le 07/05/2024 a le 07 may 2024   ######################


def convertir_format_date(chaine: str) -> str:
    import re
    from datetime import datetime
    # Expression régulière pour extraire la date et l'heure
    regex_date_heure = r"(\d{2}/\d{2}/\d{4}) à (\d{2}:\d{2})"
    match = re.match(regex_date_heure, chaine)
    
    if match:
        # Extraire la date et l'heure à partir du match
        date_str, heure_str = match.groups()
        # Convertir la date en objet datetime
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        
        # Extraire les heures et les minutes de l'heure
        heure, minute = heure_str.split(':')
        # Construire la chaîne au format souhaité
        date_formatee = date_obj.strftime(f"%Y-%m-%d") + f"T{heure}:{minute}:00"
        
        return date_formatee
    else:
        # Si la chaîne ne correspond pas au format attendu, retourner la chaîne originale
        return chaine

############################################################# reforme la date ###########################################
def extraire_nombre_heures(chaine: str) -> int:
    # Extraction des heures à partir de la chaîne, par exemple "il y a 4 heures"
    mots = chaine.split()
    for i, mot in enumerate(mots):
        if mot.isdigit():
            if i + 1 < len(mots) and mots[i + 1] in ["heure", "heures"]:
                return int(mot)
    return 0

# Fonction pour extraire les minutes de la chaîne
def extraire_nombre_minutes(chaine: str) -> int:
    # Extraction des minutes à partir de la chaîne, par exemple "il y a 30 minutes"
    mots = chaine.split()
    for i, mot in enumerate(mots):
        if mot.isdigit():
            if i + 1 < len(mots) and mots[i + 1] in ["minute", "minutes"]:
                return int(mot)
    return 0

# Fonction pour extraire la durée totale en secondes
def extraire_nombre_seconde(chaine: str) -> int:
    heures = extraire_nombre_heures(chaine)
    minutes = extraire_nombre_minutes(chaine)
    return (heures * 3600) + (minutes * 60)


#######################################################################""
from datetime import datetime

def reformulate_date(chaine: str) -> str:
    # Dictionnaire pour mapper les mois en français aux mois numériques
    mois_en_fr = {
        'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04',
        'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08',
        'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
    }

    try:
        # Exemple de chaîne d'entrée : '29 juillet 2024, 16:57:00'
        # Extraire la date et l'heure
        date_part, time_part = chaine.split(', ')
        day, month_name, year = date_part.split()
        hour, minute, second = time_part.split(':')

        # Convertir le mois en format numérique
        month_num = mois_en_fr.get(month_name.lower(), '01')  # Par défaut '01' si mois non trouvé

        # Créer la chaîne au format souhaité
        formatted_date = f"{day.zfill(2)}-{month_num}-{year}T{hour}:{minute}:{second}"

        # Convertir en objet datetime pour vérification (optionnel)
        datetime_object = datetime.strptime(formatted_date, '%Y-%m-%dT%H:%M:%S')

        return formatted_date

    except (IndexError, ValueError) as e:
        # En cas d'erreur, renvoyer la chaîne d'entrée originale
        print(f"Erreur de traitement de la date: {e}")
        return chaine
############################################################################
def convertir_secondes_en_date(secondes: int) -> str:
    from datetime import datetime, timedelta
    # Obtenir la date et l'heure actuelles
    maintenant = fonction_date_exportation()
    # Soustraire le nombre de secondes de la date actuelle
    nouvelle_date = maintenant - timedelta(seconds=secondes)
    
    # Convertir la nouvelle date en chaîne au format souhaité
    date_formatee = nouvelle_date.strftime("%Y-%m-%dT%H:%M:%S")
    
    return date_formatee


############################################################ calculer_date_publication ################################
def calculer_date_publication(chaine_duree: str) -> str:
    nbr_secondes=extraire_secondes(chaine_duree)
    date_publication_obj=convertir_secondes_en_date(nbr_secondes)
    return date_publication_obj

################################## convert date startswith le   #####################""






def convertir_chaine_en_date(chaine_2: str) -> str:
    # Liste des formats de date à tester
    chaine=chaine_2[3:]
    formats = [
        "%d/%m/%Y à %H:%M",
        "%d-%m-%Y à %H:%M",
        "%d %B %Y à %H:%M",
        "%d/%m/%Y %H:%M",
        "%d-%m-%Y %H:%M",
        "%d %B %Y %H:%M",
        "%d %B %Y à %H:%M",
        '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M', '%Y-%m-%d', '%d/%m/%Y', '%d/%m/%Y %H:%M',"%d %b %Y, %Hh%M", "%d %B %Y, %H:%M", "%d %b %Y, %H:%M:%S",
        "%d %B %Y, %H:%M:%S", "%d %B %Y , %H:%M:%S", "%d %B %Y, %H:%M,:%S",
        "%d %b %Y ,%Hh%M:%S", "%Y-%m-%dT%H:%M", "%d %b %Y ,%Hh%M):%S",
        "%d %b %Y ,%Hh%M,:%S","%d %B %Y à %Hh%M",
        "%d/%m/%Y à %H:%M",
        "le %d-%m-%Y à %H:%M",
        "le %d %B %Y à %H:%M",
        "%d/%m/%Y %H:%M",
        "%d-%m-%Y %H:%M",
        "%d %B %Y %H:%M"
    ]
    
    # Expression régulière pour extraire la date et l'heure
    regex_date_heure = r"(\d{2}/\d{2}/\d{4}) à (\d{2}:\d{2})|(\d{2}-\d{2}-\d{4}) à (\d{2}:\d{2})|(\d{2} \w+ \d{4}) à (\d{2}:\d{2})|(\d{2} \w+ \d{4}) (\d{2}:\d{2})"
    match = re.match(regex_date_heure, chaine)
    
    if match:
        # Récupère toutes les captures
        date_strs = match.groups()
        
        # Essayer chaque combinaison de date et heure capturées
        for i in range(0, len(date_strs), 2):
            date_str = date_strs[i]
            heure_str = date_strs[i+1]
            if date_str and heure_str:
                # Concaténer date et heure
                date_heure_str = f"{date_str} {heure_str}"
                
                # Essayer chaque format de date
                for format_str in formats:
                    try:
                        # Convertir la chaîne de date en objet datetime
                        date_obj = datetime.strptime(date_heure_str, format_str)
                        # Convertir en chaîne au format souhaité
                        date_formatee = date_obj.strftime("%Y-%m-%dT%H:%M:%S")
                        return date_formatee
                    except ValueError:
                        continue
        print("Erreur: Aucune correspondance de format trouvée.")
        return None
    else:
        print("La chaîne ne correspond pas au format attendu.")
        return None




########################################################### fonction date publication #########################################*
def date_publication_article(chaine: str) -> str:
    date_expo=fonction_date_exportation()
    
    # Votre logique existante pour formater la date en fonction des préfixes
    if chaine.startswith("il y a"):
        # Calculer la date de publication
        date_publication = calculer_date_publication(chaine)
        return date_publication
    elif chaine.startswith("le"):
        
        date_publication=convertir_chaine_en_date(chaine)
    elif chaine.startswith("hier"):
        date_publication_A = joindre_date_et_partie_heure(chaine)
        date_publication=reformulate_date(date_publication_A)
    elif chaine.startswith("à l’instant"):
        date_publication = date_expo.strftime('%Y-%m-%dT%H:%M:%S') 
    else:
        date_publication = date_expo.strftime('%Y-%m-%dT%H:%M:%S') 
    return date_publication
######################################################################################

##################################################################""  Fonction findArticle   ##########################################
def Find_Article(article_section_order_1,driver,Sous_Actualite,order):
      title_accueil='Non Trouvee'
      title='Non Trouvee'
      link_element='Non Trouvee'
      date_publication=None
      auteur_name='Non Trouvee'
      p='Non Trouvee'
      has_figure='Non'
      categorie_text='Non Trouvee'
      duree='Non Trouvee'
    
      #article_1=article_section_order_1.find('article',{'class':lambda b:b and(b.startswith('fig-'))})
      if article_section_order_1:
         links=article_section_order_1.find('a',href=True)
         if links :
            link_element=links['href']
            h2=links.find('h2')
            h1=links.find('h1')
            if h2:
               title_accueil=h2.get_text()
            elif h1:
               title_accueil=h1.get_text()
            
            if link_element.startswith(url): 
              driver.get(link_element)
              html_article = BeautifulSoup(driver.page_source, 'html.parser') 
              div_princ=html_article.find('div',{'class':lambda b:b and(b.startswith('fig-page'))})
              if div_princ:
            
                sous_div_princ=div_princ.find('div',{'class':lambda j:j and(j.startswith('fig-main-wrapper fig-layout fig-layout--wrapped'))})
                sous_div_princ_live=div_princ.find('div',{'class':lambda j:j and(j.startswith('fig-top'))})
                if sous_div_princ:
                   div1=sous_div_princ.find('div',{'class':lambda k:k and (k.startswith('fig-main-col'))})
                   
                   if div1:
                      div2=div1.find('div',{'class':lambda k:k and (k.startswith('fig'))})#class='fig-main'
                      
                      if div2:
                                                                                              
                         nav_categorie=div2.find('nav',{'class':lambda k:k and (k.startswith('fig-breadcrumb fig-pagination__hidden'))})
                         #################################################
                         categorie_text=""
                         if nav_categorie:
                                                                              
                          cat=nav_categorie.find('ol',{'class':lambda k:k and (k.startswith('fig-breadcrumb__list'))})
                          if cat:                                                        
                           catLi=cat.find_all('li',{'class':lambda k:k and (k.startswith('fig-breadcrumb__item'))})
                           for x in catLi:
                            y=x.find('a',{'class':lambda k:k and (k.startswith('fig-breadcrumb__link'))})
                            if y:
                              s=y.find('span',{'class':lambda k:k and (k.startswith('fig-breadcrumb__text'))})
                              if s:
                               text=s.getText()
                               categorie_textA=categorie_text+" "+text
                               sanEspace=supprimer_espaces_debut(categorie_textA)
                               if sanEspace.startswith("Accueil"):
                                 x = len("Accueil")
                                 categorie_text=supprimer_caracteres_debut(x,sanEspace)
                               else:
                                 categorie_text=categorie_textA 
                          #######################################################################
                         article=div2.find('article')
                         if article:
                            title=''                                                      
                            titre=article.find('h1',{'class':lambda f:f and (f.startswith('fig-headline fig-pagination__hidden'))})
                            paragraphe=article.find('p')        
                            #div_figure=article.find('div',class_=lambda x:x and 'fig-wrapper fig-zone-main fig-heading-article etx-relative' in x or 'fig-wrapper fig-zone-main fig-heading-article' in x)# fig-zone-main fig-heading-article etx-relative')
                            div_figure = article.find('div', class_=lambda x: x and (
                               x.startswith('fig-wrapper fig-zone-main fig-heading-article etx-relative') or
                               x.startswith('fig-wrapper fig-zone-main fig-heading-article')
                                     ))
                            auteur=article.find('span',class_='fig-content-metas__authors')
                            date_article=article.find('div',class_="fig-content-metas__pub")
                            if titre:
                              title=titre.getText()
                            if paragraphe:
                               p=paragraphe.getText()
                            if div_figure:
                             f=div_figure.find('figure')
                             if f:
                               has_figure="Oui"
                            else:
                               has_figure='Non'
                            if auteur:
                               s= supprimer_caracteres_debut(4, auteur.getText())# Len("par ")=4
                               auteur_name=s
                            if date_article:
                               d = date_article.find('span', class_=lambda x: x.startswith("fig-content-metas__pub-date"))
                                                                                           #fig-content-metas__pub-date--hide-small")
                               if d:
                                d_d=d.find('time')
                                date_text=d_d.getText()
                                if date_text:
                                 date_pub=supprimer_espaces_debut(date_text)
                                 if date_pub is None:
                                    date_publication=fonction_date_exportation()
                                 else:
                                    date_publication=date_publication_article(date_pub)

                            duree=''
                            if title is None:
                               title="Non Trouvee"
                            if date_publication is None:
                               date_publication=fonction_date_exportation()
                            
                            creer_article(title_accueil, title, link_element, date_publication, auteur_name, p, has_figure, Sous_Actualite, date_exportation, categorie_text, order)
                            

                if sous_div_princ_live:
                   article_live=sous_div_princ_live.find('article')#,{'class':lambda g:g and(g.startswith(''))})
                                                                                                   
                   article_live_2=sous_div_princ_live.find('div',{'class':lambda f:f and(f.startswith('fig-wrapper fig-zone-top fig-heading-topic'))})
                   nav_categorie=sous_div_princ_live.find('nav',{'class':lambda f:f and(f.startswith('fig-breadcrumb fig-pagination__hidden'))})
                                                                        
                   if nav_categorie:
                         #################################################
                         categorie_text=""
                         cat=nav_categorie.find('ol',class_="fig-breadcrumb__list")
                         if cat:
                           catLi=cat.find_all('li',class_="fig-breadcrumb__item")
                           for x in catLi:
                            y=x.find('a',class_="fig-breadcrumb__link")
                            if y:
                              s=y.find('span',class_='fig-breadcrumb__text')
                              if s:
                               text=s.getText()
                               categorie_textA=categorie_text+" "+text
                               sanEspace=supprimer_espaces_debut(categorie_textA)
                               if sanEspace.startswith("Accueil"):
                                 x = len("Accueil")
                                 categorie_text=supprimer_caracteres_debut(x,sanEspace)
                               else:
                                 categorie_text=categorie_textA 
                          #######################################################################
                   
                   
                   if article_live:
                            titre=article_live.find('h1',class_="fig-headline fig-pagination__hidden")
                            paragraphe=article_live.find('p')        
                            #div_figure=article.find('div',class_=lambda x:x and 'fig-wrapper fig-zone-main fig-heading-article etx-relative' in x or 'fig-wrapper fig-zone-main fig-heading-article' in x)# fig-zone-main fig-heading-article etx-relative')
                            div_figure = article_live.find('div', {'class':lambda x: x and (x.startswith('fig-wrapper fig-zone-top fig-live-wrapper'))})
                            auteur=article_live.find('span',class_='fig-content-metas__authors')
                            date_article=article_live.find('div',class_="fig-content-metas__pub")
                            if titre:
                              title=titre.getText()
                            if paragraphe:
                               p=paragraphe.getText()
                            if div_figure:
                             
                             f=div_figure.find('figure')
                             if f:
                               
                               has_figure="Oui"
                            else:
                               has_figure="Non"
                            if auteur:
                               s= supprimer_caracteres_debut(4, auteur.getText())# Len("par ")=4
                               auteur_name=s
                            if date_article:
                               d = date_article.find('span', class_=lambda x: x.startswith("fig-content-metas__pub-date"))
                                                                                           #fig-content-metas__pub-date--hide-small")
                               if d:
                                d_d=d.find('time')
                                date_text=d_d.getText()
                                if date_text:
                                 date_pub=supprimer_espaces_debut(date_text)
                                 if date_pub is None:
                                    date_publication=fonction_date_exportation()
                                 else:
                                    date_publication=date_publication_article(date_pub)
                                 

                            fonction_date_exportation().strftime('%d-%m-%YT%H:%M:%S')
                            creer_article(title_accueil, title, link_element, date_publication, auteur_name, p, has_figure, Sous_Actualite, date_exportation, categorie_text, order)
                    
                            
                   
                      
                   if article_live_2: 
                                                                                                 
                            titre=article_live_2.find('h1',{'class':lambda h:h and(h.startswith('fig-headline fig-pagination__hidden'))})
                            paragraphe=article_live_2.find('p')        
                            #div_figure=article.find('div',class_=lambda x:x and 'fig-wrapper fig-zone-main fig-heading-article etx-relative' in x or 'fig-wrapper fig-zone-main fig-heading-article' in x)# fig-zone-main fig-heading-article etx-relative')
                            div_figure = article_live_2.find('div', {'class':lambda x: x and (x.startswith('fig-wrapper fig-zone-top fig-live-wrapper'))})
                            auteur=article_live_2.find('span',class_='fig-content-metas__authors')
                            date_article=article_live_2.find('div',class_="fig-content-metas__pub")
                            if titre:
                              title=titre.getText()
                            if paragraphe:
                               p=paragraphe.getText()
                            if div_figure:
                             
                             f=div_figure.find('figure')
                             if f:
                               
                               has_figure="Oui"
                            else:
                               has_figure="Non"
                            if auteur:
                               s= supprimer_caracteres_debut(4, auteur.getText())# Len("par ")=4
                               auteur_name=s
                            if date_article:
                               d = date_article.find('span', class_=lambda x: x.startswith("fig-content-metas__pub-date"))
                                                                                           #fig-content-metas__pub-date--hide-small")
                               if d:
                                d_d=d.find('time')
                                date_text=d_d.getText()
                                if date_text:
                                 date_pub=supprimer_espaces_debut(date_text)
                                 if date_pub is None:
                                    date_publication=fonction_date_exportation()
                                 else:
                                    date_publication=date_publication_article(date_pub)
                                 
                            if nav_categorie:
                             #################################################
                             categorie_text=""
                             cat=nav_categorie.find('ol',class_="fig-breadcrumb__list")
                             if cat:
                              catLi=cat.find_all('li',class_="fig-breadcrumb__item")
                              for x in catLi:
                               y=x.find('a',class_="fig-breadcrumb__link")
                               if y:
                                s=y.find('span',class_='fig-breadcrumb__text')
                                if s:
                                 text=s.getText()
                                 categorie_textA=categorie_text+" "+text
                                 sanEspace=supprimer_espaces_debut(categorie_textA)
                                 if sanEspace.startswith("Accueil"):
                                  x = len("Accueil")
                                  categorie_text=supprimer_caracteres_debut(x,sanEspace)
                                 else:
                                  categorie_text=categorie_textA 
                          #######################################################################
                            duree=''
                            if title is None:
                               title="Non Trouvee"
                            
                            
                            creer_article(title_accueil, title, link_element, date_publication, auteur_name, p, has_figure, Sous_Actualite, date_exportation, categorie_text, order)
                            


########################################################### fonction principale #####################################################"
def findAllArticles(url):
    driver = WebDriverSingleton.get_instance()  
    # Définir la localisation française
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    driver.get(url)
    time.sleep(2)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # Utilisation de BeautifulSoup pour analyser le contenu de la page
    html = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Recherche de toutes les sections contenant des articles
    div_princ=html.find('div',{'class':lambda c:c and (c.startswith('fig-page'))})
    if div_princ:
     sous_div_princ=div_princ.find('div',{'class':lambda c:c and(c.startswith('fig-main-wrapper'))})
     if sous_div_princ:    
      sous_div2=sous_div_princ.find('div',{'class':lambda f:f and(f.startswith('fig-main-col'))}) 
      article_aside_left=sous_div_princ.find('aside',{'class':lambda n:n and(n.startswith('fig-left'))})
      if sous_div2:  
       sous_div3=sous_div2.find('div',{'class':lambda c:c and(c.startswith('fig-main'))})
       
       if sous_div3:
        article_section_order_1=sous_div3.find('article',{'class':lambda x: x and (x.startswith('fig-ranking-profile-container'))})# or x.startswith('fig-ensemble')or x.startswith('fig-ensemble__first-article'))})
        article_section_order_2=sous_div3.find('section',{'class':lambda x : x.startswith('fig-')})
        article_section_order_2_2=sous_div3.find('article',{'class':lambda x : x.startswith('fig-')})                                                                        
        
        #div_article_left=article_aside.find_all('div',class_="fig-list-articles")
        

        ####################""
        if article_section_order_1:
           order='1'
           Sous_Actualite='Non'
        
           Find_Article(article_section_order_1,driver,Sous_Actualite,order)
        if article_section_order_2:
           article_order_2=article_section_order_2.find('article',{'class':lambda x: x and (x.startswith('fig'))})
           if article_order_2:
             order='2'
             Sous_Actualite='Non'
            
             Find_Article(article_order_2,driver,Sous_Actualite,order)
        if article_section_order_2_2:
           order='2'
           Sous_Actualite='Non'
          
           Find_Article(article_section_order_2_2,driver,Sous_Actualite,order)
        if article_aside_left:
           div_articles_left=article_aside_left.find_all('div',{'class':lambda h:h and (h.startswith('fig-list-articles'))})
           for x in div_articles_left:
            order='3'
            Sous_Actualite='Non'
            
            Find_Article(x,driver,Sous_Actualite,order)
def fonction_Lefigaro(d):
    global scraping_active
    i = 0
    while scraping_active:
     try:
        print('***'*23)
        print('')
        print("Le scraping de Lefigaro a commencé à l'itération numéro :",i)
        print('')
        print('***'*23)
        findAllArticles(url) 
        i=i+1
        
        print('***'*23)
        print('')
        print(' le scrping de Lefigaro a Termine en Iteration numero : ',i)
        print('')
        print('***'*23)
        
         # Appeler la fonction pour trouver tous les articles
        time.sleep(d)  # Attendre 60 secondes avant de recommencer (ou ajuster selon vos besoins)
     except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        break 
  
def fonction_Arrete_Script():
    global scraping_active
    scraping_active = False
    WebDriverSingleton.quit_instance()
    """print("***"*24)
    print("")
    print("Le scraping sur Lefigaro s'est arrêté avec succès.")
    print('')
    print('***'*24)"""



def start_scraping(d):
    global scraping_active
    scraping_active = True
    scraping_thread = threading.Thread(target=fonction_Lefigaro, args=(d,))
    scraping_thread.start()

findAllArticles(url) 