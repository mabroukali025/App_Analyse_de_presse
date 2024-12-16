import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import date
import time
import sys
import pandas as pd
import datetime
import re
from typing import Optional
from datetime import datetime, timedelta
import locale
import os
import threading
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from AppScraping.models import Article 
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException

url = 'https://www.liberation.fr/'
input_csv_file = "LiberationVF.csv"

from datetime import datetime
import pytz

# Define the French time zone
french_tz = pytz.timezone('Europe/Paris')

# Get the current date and time in the French time zone
now = datetime.now(french_tz)

# Format the date and time
#Date_Exportation = now.strftime('%Y-%m-%dT%H:%M:%S')
#date_exportation_obj = datetime.strptime(Date_Exportation, '%Y-%m-%dT%H:%M:%S')

from datetime import datetime

def obtenir_date_exportation():
    french_tz = pytz.timezone('Europe/Paris')

    # Get the current date and time in the French time zone
    now = datetime.now(french_tz)
    Date_Exportation = now.strftime('%Y-%m-%dT%H:%M:%S')
    date_exportation_obj = datetime.strptime(Date_Exportation, '%Y-%m-%dT%H:%M:%S')
    #now = datetime.now()  # Obtenir la date et l'heure actuelles
    return date_exportation_obj           

#################################################################### 
scraping_active = True

class WebDriverSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if WebDriverSingleton._instance is None or not WebDriverSingleton.is_session_valid():
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-features=NotificationPermissions")
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--headless")  # Optional: Headless mode for background scraping

            # Initialize WebDriver using ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            WebDriverSingleton._instance = webdriver.Chrome(service=service, options=chrome_options)

            # Setting locale for date parsing
            import locale
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        
        return WebDriverSingleton._instance

    @staticmethod
    def is_session_valid():
        """Vérifie si la session WebDriver est encore active et valide."""
        try:
            # Effectuer une action simple pour vérifier la validité de la session
            WebDriverSingleton._instance.title  # Vérifier si l'instance est active via une action légère
            return True
        except (InvalidSessionIdException, WebDriverException, AttributeError):
            return False

    @staticmethod
    def quit_instance():
        """Quitte proprement l'instance WebDriver et réinitialise le singleton."""
        if WebDriverSingleton._instance is not None:
            WebDriverSingleton._instance.quit()
            WebDriverSingleton._instance = None



#########################################  Created Article   ###############"
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
    print('')
    print('\033[92m' + '**************************************************** Save with success in Liberation ***********************************' + '\033[0m')
    print('')
    return article

##################################################### I,itialisations des variables ##################################################

title_page_Acceuil="Non Trouvee"
title="Non Trouvee"
link_page="Non Trouvee"
date_text="Non Trouvee"
auteur_name="Non Trouvee"
paragraphe="Non Trouvee"
has_image="Non Trouvee"
Sous_Actualite="Non Trouvee"
categorie="Non Trouvee"
order=""
#########################################################################  la fonction DE supprime au de but de chaine   ############"
def fonction_Supprime_au_debut(chaine):
    date_exportation_obj=obtenir_date_exportation()
    if '1er' in chaine:
        chaine=chaine.replace('1er','1')
    if chaine.startswith("publié aujourd'hui à"):
        x=len("publié aujourd'hui à")
        chaine_sans_debut=chaine[x+1:]
        
        date_publication=obtenir_date_publication(chaine_sans_debut)
        return date_publication
    elif chaine.startswith("publié le "):
        x_2=len("publié le ")
        chaine_sans_debut=chaine[x_2:].strip()
       

        date_publication=extraire_et_formater_date(chaine_sans_debut)
        return date_publication
    else:
        date_publication=date_exportation_obj
        return date_publication
########################################################################################################
from datetime import datetime, timedelta

def obtenir_date_publication(heure_publication):
    # Assurer que date_exportation est déjà un objet datetime
    from datetime import datetime
    date_exportation_obj=obtenir_date_exportation()
    date_sans_heure = date_exportation_obj.date()
    
    # Combiner date_sans_heure avec heure_publication pour obtenir la date de publication complète
    heure_publication_obj = datetime.strptime(heure_publication, '%Hh%M')
    date_publication = datetime.combine(date_sans_heure, heure_publication_obj.time())
    
    # Formater la date de publication selon le format souhaité
    date_publication_str = date_publication.strftime('%Y-%m-%dT%H:%M:%S')
    
    return date_publication_str




def extraire_et_formater_date(date_string):
    # Nettoyer la chaîne et enlever les parties non nécessaires
    cleaned_date_string = date_string.strip().replace('publié le ', '').replace('h', ' ').strip()

    

    # Séparer la partie date de la partie heure
    try:
        # Séparer la chaîne en deux parties autour de ' à '
        date_part, heure_part = cleaned_date_string.split(' à ')
        
    except ValueError:
        raise ValueError(f"Date string format is incorrect: '{date_string}'")

    # Extraire les composants de la date
    date_parts = date_part.split(' ')
    
    if len(date_parts) != 3:
        raise ValueError(f"Date part is not in the expected format: '{date_part}'")

    jour, mois, annee = date_parts[0], date_parts[1], date_parts[2]

    # Extraire les composants de l'heure
    heure_minute = heure_part.split(' ')
    
    if len(heure_minute) != 2:
        raise ValueError(f"Heure part is not in the expected format: '{heure_part}'")

    heure, minute = heure_minute[0], heure_minute[1]

    # Convertir les mois en nombres
    mois_mapping = {
        'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4, 'mai': 5, 'juin': 6,
        'juillet': 7, 'août': 8, 'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
    }

    mois_num = mois_mapping.get(mois.lower(), None)

    if mois_num is None:
        raise ValueError(f"Month '{mois}' is not recognized")

    # Créer un objet datetime avec les paramètres extraits
    dt = datetime(year=int(annee), month=mois_num, day=int(jour), hour=int(heure), minute=int(minute), second=0)
    
    # Retourner la date formatée selon le format spécifié
    return dt.strftime('%Y-%m-%dT%H:%M:%S')

###########################################################################
def supprimer_caracteres_debut(nombre, categoriex):
    # This is a placeholder function. Implement the actual logic as needed.
    # For example, this removes the first 'nombre' characters from 'categoriex'.
    return categoriex[nombre:]

###########################################################################
def supprimer_slashes(texte):
    # Supprimer les "/" au début et à la fin de la chaîne
    while texte.startswith("/"):
        texte = texte[1:]
    while texte.endswith("/"):
        texte = texte[:-1]
    return texte


###############################################################################  fonction extraire dans les divs card list  #######################
def extraire_card_List(div_card_list,actualite,order_Actualite,driver):
   if isinstance(div_card_list, list):
       #  teste que le parametre div_card_list est une liste ou nn
      i=0
      for art in div_card_list:
                      
                      if art:
                         if i>=1 and order_Actualite=="1":
                             actualite='Oui'
                             find_Article(art,actualite,order_Actualite,driver)
                         else:
                             find_Article(art,actualite,order_Actualite,driver) 
                         i=i+1 
   else:   
      if div_card_list:
         find_Article(div_card_list,actualite,order_Actualite,driver)  

########################################################################## fonction extraire des donnees dans div  ##################"
def extraire_donnees_div(div_1,driver):                                   
              div_princ_1=div_1.find('div',class_="flex-chain container-fluid")
              if div_princ_1:
                div_row=div_princ_1.find('div',class_="row")
                if div_row:                                                    
                  div_item_order_1 = div_row.find('div',{'order':'1'})# class_="ItemChainElement__ItemElementLayout-sc-1c74lbk-0 llbJf col-sm-12 col-md-xl-6 layout-section" )#in x or 'ItemChainElement__ItemElementLayout-sc-1c74lbk-0 keBuqV col-sm-12 col-md-xl-3 layout-section' in x or 'ItemChainElement__ItemElementLayout-sc-1c74lbk-0 bFpkGQ col-sm-12 col-md-xl-3 layout-section' in x))#lambda x: isinstance(x, str) and x.startswith("ItemChainElement__ItemElementLayout"))
                  div_item_order_2 = div_row.find('div', {'order':'2'})#class_="ItemChainElement__ItemElementLayout-sc-1c74lbk-0 keBuqV col-sm-12 col-md-xl-3 layout-section" )#in x or 'ItemChainElement__ItemElementLayout-sc-1c74lbk-0 keBuqV col-sm-12 col-md-xl-3 layout-section' in x or 'ItemChainElement__ItemElementLayout-sc-1c74lbk-0 bFpkGQ col-sm-12 col-md-xl-3 layout-section' in x))#lambda x: isinstance(x, str) and x.startswith("ItemChainElement__ItemElementLayout"))
                  div_item_order_3 = div_row.find('div', {'order':'3'})#class_="ItemChainElement__ItemElementLayout-sc-1c74lbk-0 bFpkGQ col-sm-12 col-md-xl-3 layout-section" )#in x or 'ItemChainElement__ItemElementLayout-sc-1c74lbk-0 keBuqV col-sm-12 col-md-xl-3 layout-section' in x or 'ItemChainElement__ItemElementLayout-sc-1c74lbk-0 bFpkGQ col-sm-12 col-md-xl-3 layout-section' in x))#lambda x: isinstance(x, str) and x.startswith("ItemChainElement__ItemElementLayout"))
                  
                  if div_item_order_1:                     
                   Sous_Actualite="Non"
                   order_Actualite="1"
                   div_card_list_1=div_item_order_1.find_all('div',{'class':lambda k:k and(k.startswith('custom-card-list'))})
                   if div_card_list_1:
                      extraire_card_List(div_card_list_1,Sous_Actualite,order_Actualite,driver)
                  
                  if div_item_order_2:                     
                   Sous_Actualite="Non"
                   order_Actualite="2"
                   div_card_list_2=div_item_order_2.find_all('div',class_="custom-card-list")
                   if div_card_list_2:
                    
                    extraire_card_List(div_card_list_2,Sous_Actualite,order_Actualite,driver)
                  
                  if div_item_order_3:                     
                   Sous_Actualite="Non"
                   order_Actualite="3"
                   div_card_list_3=div_item_order_3.find_all('div',class_="custom-card-list")
                   if div_card_list_3:
                    extraire_card_List(div_card_list_3,Sous_Actualite,order_Actualite,driver)
                  
##################################################################################################"
def extraire_donnees_div_2(div_2,driver):
   if div_2:                                       
              div_princ_1=div_2.find_all('div',class_="flex-chain container-fluid")
              for d in  div_princ_1:
                div_row=d.find('div',class_="row")
                if div_row:                                                
                  div_item_order_1 = div_row.find('div',{'order':'1'})# class_="ItemChainElement__ItemElementLayout-sc-1c74lbk-0 llbJf col-sm-12 col-md-xl-6 layout-section" )#in x or 'ItemChainElement__ItemElementLayout-sc-1c74lbk-0 keBuqV col-sm-12 col-md-xl-3 layout-section' in x or 'ItemChainElement__ItemElementLayout-sc-1c74lbk-0 bFpkGQ col-sm-12 col-md-xl-3 layout-section' in x))#lambda x: isinstance(x, str) and x.startswith("ItemChainElement__ItemElementLayout"))
                  div_item_order_2 = div_row.find('div', {'order':'2'})#class_="ItemChainElement__ItemElementLayout-sc-1c74lbk-0 bFpkGQ col-sm-12 col-md-xl-6 layout-section" )#in x or 'ItemChainElement__ItemElementLayout-sc-1c74lbk-0 keBuqV col-sm-12 col-md-xl-3 layout-section' in x or 'ItemChainElement__ItemElementLayout-sc-1c74lbk-0 bFpkGQ col-sm-12 col-md-xl-3 layout-section' in x))#lambda x: isinstance(x, str) and x.startswith("ItemChainElement__ItemElementLayout"))
                  div_item_order_3 = div_row.find('div', {'order':'3'})#class_="ItemChainElement__ItemElementLayout-sc-1c74lbk-0 llbJf col-sm-12 col-md-xl-4 layout-section" )#in x or 'ItemChainElement__ItemElementLayout-sc-1c74lbk-0 keBuqV col-sm-12 col-md-xl-3 layout-section' in x or 'ItemChainElement__ItemElementLayout-sc-1c74lbk-0 bFpkGQ col-sm-12 col-md-xl-3 layout-section' in x))#lambda x: isinstance(x, str) and x.startswith("ItemChainElement__ItemElementLayout"))
                  div_item_order_4= div_row.find('div',{'order':'4'})# class_="ItemChainElement__ItemElementLayout-sc-1c74lbk-0 keBuqV col-sm-12 col-md-xl-4 layout-section")
                  div_item_order_5= div_row.find('div',{'order':'5'})#class_='ItemChainElement__ItemElementLayout-sc-1c74lbk-0 bFpkGQ col-sm-12 col-md-xl-4 layout-section')
                  
                  actualite="oui"
                  order_Actualite="4"
                  if div_item_order_1:                     
                   div_card_list_1=div_item_order_1.find_all('div',class_="custom-card-list")
                   extraire_card_List(div_card_list_1,actualite,order_Actualite,driver)
                  if div_item_order_2:                     
                   div_card_list_2=div_item_order_2.find_all('div',class_="custom-card-list")
                   extraire_card_List(div_card_list_2,actualite,order_Actualite,driver) 
                  if div_item_order_3:                     
                   div_card_list_3=div_item_order_3.find_all('div',class_="custom-card-list")
                   extraire_card_List(div_card_list_3,actualite,order_Actualite,driver) 
                  if div_item_order_4:                     
                   div_card_list_4=div_item_order_4.find_all('div',class_="custom-card-list")
                   extraire_card_List(div_card_list_4,actualite,order_Actualite,driver) 
                  if div_item_order_5:                     
                   div_card_list_5=div_item_order_5.find_all('div',class_="custom-card-list")
                   extraire_card_List(div_card_list_5,actualite,order_Actualite,driver) 
############################################################################### 
def extraire_donnees_div_3(div_3,driver):
   actualite="oui"
   order_Actualite="5"
   if div_3:                                       
      div_princ_1=div_3.find_all('div',class_="flex-chain container-fluid")
      
      for d in  div_princ_1:
          if d:
            div_pere_row=d.find('div')
            
            if div_pere_row:
                div_row=div_pere_row.find('div',class_="row")
                if div_row:                                                
                  div_item_order_3= div_row.find_all('div',class_=lambda x:x and ( x.startswith('ItemChainElement__ItemElementLayout-sc-1c74lbk-0')))#llbJf col-sm-12 col-md-xl-3 layout-section')
                  
                  for  d in  div_item_order_3:                     
                   div_card_list=d.find_all('div',class_="custom-card-list")
                   
                   for x in div_card_list:
                     if x:
                      
                      extraire_card_List(x,actualite,order_Actualite,driver)
                       
                       
                  
###############################################################################  find Articles ###################################"
def find_Article(art, actualite, order_Actualite, driver):
    article_balise = art.find('article')
    if article_balise:
        title = 'non trouvée'
        auteur_name = 'non trouvée'
        paragraphe = 'non trouvée'
        has_image = 'non trouvée'
        categorie = 'non trouvée'
        date_text = None
        date_pub=None
        auteur_='Non Trouvee'
        div_text = article_balise.find('div', {'class': lambda f: f and f.startswith('row text-align_left')})
        if div_text:
            div_col = div_text.find('div', {'class': lambda g: g and g.startswith('col-sm-xl-12 flex-col margin-xs-bottom')})
            if div_col:
                div_a = div_col.find('a', class_=lambda x: x and x.startswith('Overline-sc-'))
                if div_a:
                    tt = div_a.getText()
                else:
                    tt = " "
                
                div_a_2 = div_col.find('a', class_="decoration_none color_grey_4")
                if div_a_2:
                    title_Acceuil = div_a_2.find('h2')
                    if title_Acceuil:
                        title_Acceuil2 = tt + " " + title_Acceuil.getText()
                    else:
                        title_Acceuil2 = "Titre Non Trouvé"
                    
                    link_element = div_a_2['href']
                    if link_element:
                        link = url + link_element
                        driver.get(link)
                        time.sleep(1)
                        
                        html_article = BeautifulSoup(driver.page_source, 'html.parser')
                        if html_article:
                            main_page = html_article.find('main', {'class': lambda c: c and c.startswith('sc')})
                            if main_page:                                                                   
                                article_div = main_page.find('div', {'class': lambda x: x and x.startswith('default__Main-sc')})                 
                                art_x_cate = main_page.find('div', {'data-coreads-cover-content': 'true', 'class': lambda x: x and x.startswith('default__FullWidth1-sc-')})

                                if article_div:                                                                    
                                    div_p_and_h1 = article_div.find('div', {'class': lambda k: k and k.startswith('TypologyArticle__BlockContainer-sc')})
                                    if div_p_and_h1:                                                                         
                                        article_title = div_p_and_h1.find_all('div', {'class': lambda c: c and c.startswith('TypologyArticle__BlockHeadline-sc-')})
                                        for art in article_title:                                                            
                                            if art:                                                            
                                                t_1 = art.find('span', {'class': lambda b: b and (b.startswith('TypologyArticle__BlockLabel-sc-') or b.startswith('TypologyArticle__BlockLabelChronique-sc-'))})
                                                if t_1:
                                                    t1 = t_1.getText()
                                                else:
                                                    t1 = ""                                                   
                                                t_2 = art.find('h1', {'class': lambda v: v and( v.startswith('TypologyArticle__BlockTitleHeadline') or v.startswith('TypologyArticle__BlockTitleHeadlineCheckNews-sc-'))})
                                                if t_2:
                                                    t_3 = t_2.getText()
                                                    if t_3:
                                                        title = t1 + " " + t_3
                                                    
                                    p = article_div.find('span', class_=lambda x: x.startswith('TypologyArticle__BlockSubHeadline-sc'))
                                    if p:
                                        paragraphe = p.getText()

                                    has_figure = article_div.findChild('figure')
                                    if has_figure:
                                        has_image = "Oui"

                                    date_article = article_div.find('div', {'class': lambda h: h and h.startswith('grid grid')})
                                    if date_article:
                                        d = date_article.find('div', {'class': lambda h: h and h.startswith('font_xs')})
                                        if d:
                                            date_pub = d.get_text()
                                            #date_text=gerer_date(date_pub)
                                    auteur_list_2=article_div.find('div',{'class':lambda f:f and (f.startswith('default__Container'))})
                                    auteur_list = article_div.find('span', {'class': lambda j: j and j.startswith('font_xs display_block link_primary-color')})
                                    if auteur_list:
                                        auteur_text = auteur_list.getText()
                                        nombre = len('par ')
                                        auteur_name = supprimer_caracteres_debut(nombre, auteur_text)
                                    if auteur_list_2:
                                        list_auteur_name=auteur_list_2.find_all('a',{'class':lambda g:g and g.startswith('sc-ksZaOG')})
                                        if list_auteur_name:
                                            auteur_name=''
                                            for a in list_auteur_name:
                                                auteur_name=auteur_name+' / '+a.getText()
                                                if auteur_name:
                                                    auteur_=auteur_name[2:]

                                if art_x_cate:
                                    article_categorie = art_x_cate.find('div', {'class': lambda v: v and v.startswith('font_xxs color_grey')})
                                    if article_categorie:
                                        categoriex = article_categorie.getText()
                                        nombre = len('  Accueil')
                                        categorie = supprimer_caracteres_debut(nombre, categoriex)
                                    else:
                                        categorie = "Catégorie non Trouvée"
        if date_pub is None:
            date_pub=obtenir_date_exportation()#Date_Exportation
       
        chaine_sans_debut=fonction_Supprime_au_debut(date_pub)
        Date_Exportation=obtenir_date_exportation()
        #save_in_file(title_Acceuil2, title, link, chaine_sans_debut, auteur_, paragraphe, has_image, actualite, Date_Exportation, categorie, order_Actualite)
        #print('************************************************************  la date dexportation est :',Date_Exportation)        
        
        creer_article(title_Acceuil2, title, link, chaine_sans_debut, auteur_, paragraphe, has_image, actualite, Date_Exportation, categorie, order_Actualite)
        
                              
    else:
        return None

###########################################################################  Fonction Principale   #####################################################
def findAllArticles(url):
  driver = WebDriverSingleton.get_instance()
    # Définir la localisation française
  locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
  driver.get(url)
  time.sleep(3)

  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

  time.sleep(5)
    # Utilisation de BeautifulSoup pour analyser le contenu de la page
  html = BeautifulSoup(driver.page_source, 'html.parser') # Recherche de toutes les sections contenant des articles
  body_page= html.find('body')
  
  if body_page:
    """
    princ_div=body_page.find('div',class_="layout-section") #  div principle est le grand div dans le code source
    if princ_div:
     sous_div=princ_div.find('div',{'class':lambda f:f and f.startswith('default__PrismaWrapper-s')})
     if sous_div:
     
      div_main=sous_div.find('main',{'class':lambda x:x and x.startswith('sc')})
      if div_main: 
        div_main_2=div_main.find('div',{'class':lambda x:x and x.startswith('sc')})#,class_="sc-epVeNg cOWDyY sc-ehmTmK dGmPpK")
        if div_main_2:
          print('hhh')
          main_in_div_2 = div_main_2.find('main', {'class': lambda g: g and g.startswith('sc-gFGZVQ jZmnsE sc-gSpBRe iyqtOG')})
          if main_in_div_2:
            print('hhh')                                     
            """
    div_1=body_page.find('div',class_=lambda h:h and h.startswith('default__FullWidth1-sc-sezp2u-1 bYNMjz'))# sc-lbOyJj kRdUvr'))#-sezp2u-1 dGhQWW sc-ehmTmK cOhApt")
    #div_2=body_page.find('div',class_=lambda h:h and h.startswith('default__Main-sc-sezp2u-2 kxxFcP sc-lbOyJj cobDa-D'))
    #div_3=body_page.find('div',class_=lambda h:h and h.startswith('default__FullWidth2-sc-sezp2u-4 crFABv sc-lbOyJj bMFUpk'))
    if div_1:
              
             extraire_donnees_div(div_1,driver)        
    
    #if div_2:
      # extraire_donnees_div_2(div_2,driver)
    #if div_3:
        #extraire_donnees_div_3(div_3,driver)
        
###################
def fonction_liberation(d):
    print('')
    print('  ********************************              LIBERATION            ******************')
    print('')
    global scraping_active
    if scraping_active==False:
        scraping_active=True
    i = 1
    #print(' ***************    scraping_active   ****************',scraping_active)
    while scraping_active:
     try:
        print('***'*30)
        print('')
        print(' le scrping de Liberation a commance Iteration numero : ',i)
        print('')
        print('***'*30)
        Date_Exportation=obtenir_date_exportation()
        print('la date dexportation est :',Date_Exportation)
        findAllArticles(url) 
        
        print('***'*30)
        print('')
        print(' le scrping de Liberation a Termine Iteration numero : ',i)
        print('')
        print('***'*30)
        i=i+1
         # Appeler la fonction pour trouver tous les articles
        time.sleep(d)  # Attendre 60 secondes avant de recommencer (ou ajuster selon vos besoins)
     except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        break 
  
def fonction_Arrete_Script():
    global scraping_active
    scraping_active = False
    WebDriverSingleton.quit_instance()
    print("****"*30)
    print("")
    print("Le scraping Sur Liberation est  arrêté avec succès.")
    print('')
    print('****'*30)



def start_scraping(d):
    global scraping_active
    scraping_active = True
    scraping_thread = threading.Thread(target=fonction_liberation, args=(d,))
    scraping_thread.start()
    
