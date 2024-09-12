import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import date
import pandas as pd
from datetime import  timedelta
import requests
import os
from AppScraping.models import Article 
import datetime
import datetime
from datetime import datetime, date, timedelta
import threading
import pytz

url="https://www.lemonde.fr/"

def fonction_date_exportation():
 import locale
 locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
 from datetime import datetime
 Date_Exportation = datetime.now()
 return Date_Exportation
Date_Exportation=fonction_date_exportation().strftime('%Y-%m-%dT%H:%M:%S') 
######################################################## fonction principle  ##########################################
scraping_active = True

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









########################################################################

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
#################################################################################


from datetime import datetime
import pytz

TIME_ZONE = 'Europe/Paris'
tz = pytz.timezone(TIME_ZONE)


# Dictionnaire pour mapper les mois français à leur équivalent en anglais
mois_mapping = {
    'janvier': 'January', 'février': 'February', 'mars': 'March', 'avril': 'April',
    'mai': 'May', 'juin': 'June', 'juillet': 'July', 'août': 'August',
    'septembre': 'September', 'octobre': 'October', 'novembre': 'November', 'décembre': 'December'
}

def date_publier_le(chaine):
 if chaine.startswith('Publié le '):
    x=len("Publié le ")
    chaine=chaine[x:]
    # Nettoyer la chaîne en enlevant les espaces superflus et les virgules
    chaine = chaine.strip().replace(',', '')
    
    # Trouver la partie date
    date_partie = chaine.split('à')[0].strip()
    
    # Trouver la partie heure
    heure_partie = chaine.split('à')[1].strip()
    
    # Remplacer les mois français par leurs équivalents anglais
    for mois_fr, mois_en in mois_mapping.items():
        if mois_fr in date_partie:
            date_partie = date_partie.replace(mois_fr, mois_en)
            break
    
    # Convertir la partie date en format utilisable
    try:
        date_obj = datetime.strptime(date_partie, '%d %B %Y') # Date sans heure
    except ValueError:
        print(f"Erreur de format de date : {date_partie}")
        return None
    
    # Combiner la date et l'heure
    date_heure_str = date_obj.strftime('%Y-%m-%d') + ' ' + heure_partie.replace('h', ':') + ':00'
    
    # Convertir en objet datetime
    try:
        # Assumer que la chaîne fournie est en heure locale (Europe/Paris)
        date_publication_obj = datetime.strptime(date_heure_str, '%Y-%m-%dT%H:%M:%S')
        date_publication_obj = tz.localize(date_publication_obj)  # Localiser en Europe/Paris
        return date_publication_obj.strftime('%Y-%m-%dT%H:%M:%S')
    except ValueError as e:
        print(f"Erreur de conversion pour la chaîne : {date_heure_str}. Détails : {e}")
        return None


######################################################""
def extraire_date(chaine):
    formats = [
        '%d %b %Y, %Hh%M',
        '%d %B %Y, %H:%M',
        '%d %b %Y, %H:%M:%S',
        '%d %B %Y, %H:%M:%S',
        '%d %B %Y , %H:%M:%S',
        '%d %m %Y à %H:%M:%S',
        "%d %b %Y, %Hh%M",        # '12 juil. 2024, 16h00'
        "%d %B %Y, %H:%M",        # '13 juillet 2024, 00:25'
        "%d %b %Y, %H:%M:%S",     # '12 juil. 2024, 22:17:00'
        "%d %B %Y, %H:%M:%S",     # '12 juillet 2024, 22:17:00'
        "%d %B %Y , %H:%M:%S",    # '13 juillet 2024 , 23:46:39'
        "%d %B %Y à %Hh%M",
        "%d %B %Y, %H:%M,:%S",    # '13 juillet 2024, 00:33,:00'
        "%d %b %Y ,%Hh%M:%S",     # '13 juil. 2024 ,21h28:00'
        "%Y-%m-%dT%H:%M",         # '2024-07-13T21:59'
        "%d %b %Y ,%Hh%M):%S",    # '13 juil. 2024 ,21h59):00'
        "%d %b %Y ,%Hh%M,:%S" ,    # '13 juil. 2024 ,21h59,:00'
        '%d %b %Y à %Hh%M',        # '30 juil. 2024 à 06h00'
        '%d %B %Y à %Hh%M',        # '30 juillet 2024 à 06h00'
        '%d %B %Y à %H:%M',        # '30 juillet 2024 à 06:00'
        '%d %B %Y à %H:%M:%S',     # '30 juillet 2024 à 06:00:00'
        '%d %m %Y à %H:%M:%S',     # '30 07 2024 à 06:00:00'
        "%Y-%m-%dT%H:%M",
    ]
    
    # Nettoyer la chaîne
    chaine = chaine.replace("Publié le ", "").strip()
    chaine = chaine.split(", modifié")[0].strip()
    
    # Essayer de convertir en date avec chaque format
    for fmt in formats:
        try:
            date_obj = datetime.strptime(chaine, fmt)
            return date_obj.astimezone(tz).strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
    
    print(f"Erreur d'extraction de date pour la chaîne : {chaine}")
    return None
###############################################################################
def gerer_date(chaine):
    if chaine.startswith("Publié aujourd’hui à"):
        return convertir_chaine_en_date_Lemonde(chaine)
    elif chaine.startswith("Publié hier à"):
        return date_publiee_hier(chaine)
    elif chaine.startswith("Publié le"):
        return date_publier_le(chaine) # A implémenter si nécessaire
    else:
        return fonction_date_exportation().strftime('%Y-%m-%dT%H:%M:%S')

def extraire_heure_Lemonde(chaine: str) -> str:
    import re
    # Expression régulière pour extraire l'heure de la chaîne
    regex_heure = r"à (\d{2}h\d{2})"
    match = re.search(regex_heure, chaine)
    
    if match:
        return match.group(1)
    else:
        raise ValueError("La chaîne ne contient pas l'heure au format attendu.")
####################################################################################################
def convertir_chaine_en_date_Lemonde(chaine: str) -> str:
    try:
        # Extraire l'heure de la chaîne
        
        heure_str = extraire_heure_Lemonde(chaine)
        # Convertir l'heure au format HH:MM
        heure_formatee = heure_str.replace('h', ':')
        date_exportation = fonction_date_exportation()
        # Combiner la date d'exportation avec l'heure extraite
        date_heure_str = date_exportation.strftime("%Y-%m-%d") + 'T' + heure_formatee + ':00'
        
        # Convertir en objet datetime
        date_publication_obj = datetime.strptime(date_heure_str, "%Y-%m-%dT%H:%M:%S")
        
        # Convertir en chaîne au format souhaité
        date_formatee = date_publication_obj.strftime("%Y-%m-%dT%H:%M:%S")
        
        return date_formatee
    except Exception as e:
        print(f"Erreur : {e}")
        return None
####################################################################################
def extraire_partie_publication(chaine: str) -> str:
    import re
    try:
        # Expression régulière pour trouver la position du mot "modifié à"
        regex_modifie = r"(modifié à)"
        match = re.search(regex_modifie, chaine)
        
        if match:
            # Extraire la partie de la chaîne avant "modifié à"
            return chaine[:match.start()].strip()
        else:
            return chaine
    except Exception as e:
        print(f"Erreur : {e}")
        return None

def date_publiee_hier(chaine):
    if chaine.startswith("Publié hier à "):
        chaine = extraire_partie_publication(chaine)
       
        
        # Nettoyer la chaîne pour enlever les caractères indésirables
        chaine = chaine.replace(',', '').strip()
        
        date_hier = datetime.now(tz) - timedelta(days=1)
        heure_chaine = chaine.split(" ")[-1].replace("h", ":").strip()
        date_formattee = date_hier.strftime("%Y-%m-%d") + "T"+ f'{heure_chaine}:00'
        
        # Convertir la chaîne en datetime
        try:
            date_obj = datetime.strptime(date_formattee, "%Y-%m-%dT%H:%M:%S")
            return date_obj.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError as e:
            print(f"Erreur de conversion pour la chaîne 'Publié hier': {e}")
            return None
    else:
        return None

    
    ############################################################"
def initialisation_varialbes(title,date_publication,auteur_name,p,has_figure,Actualite_A,categorie_text,order):
    title="Titre non Trouve"
    p="Paragraphe non Trouve"
    has_figure="Image non trouvee"
    auteur_name="Auteur non trouve"
    date_publication ="date non trouvee"     
    Actualite_A=" Actualite non trouvee"
    categorie_text='Categorie non trouvee'
    order=' order non trouvee'
    return title,date_publication,auteur_name,p,has_figure,Actualite_A,categorie_text,order      


######################################################################"
def supprimer_slashes(texte):
    # Supprimer les "/" au début et à la fin de la chaîne
    while texte.startswith("/"):
        texte = texte[1:]
    while texte.endswith("/"):
        texte = texte[:-1]
    return texte

##############################################################################################
def remove_characters(text, num_characters):
   
    if num_characters < 0:
        raise ValueError("Le nombre de caractères à supprimer doit être positif")
    return text[num_characters:]


##############################################################################################################################
def supprimer_modification(chaine):
    # Vérifier si la chaîne contient "modifié à"
    if "modifié à" in chaine:
        # Supprimer la partie "modifié à" et tout ce qui suit
        chaine = chaine.split("modifié à")[0].strip()
    return chaine
############################################################### chak classe de body      ##########################################
def check_classes(classes):
    # Ensembles des classes cibles
    target_classes_1 = {'main', 'LeMondeMain', 'main--free'}
    target_classes_2 = {'main', 'LeMondeMain', 'main--free', 'main--with-contextual-nav'}
    
    # Convertit la liste des classes en ensemble
    class_set = set(classes)
    
    # Vérifie si l'ensemble des classes correspond à l'un des ensembles cibles
    return target_classes_1.issubset(class_set) or target_classes_2.issubset(class_set)

# Trouver l'élément <main> avec les classes spécifiées
######################################################################## fonction find Article ####################################
def fonction_find_Article(divs_in_section,driver,Sous_Actualite,order):
            
             title_page_Acceuil='Non Trouvee'
             title='Non Trouvee'
             link_page='Non Trouvee'
             date_publication=None
             auteur_name='Non Trouvee'
             paragraphe='Non Trouvee'
             has_img='Non'
             categorie='Non Trouvee'
             date_text=None
             date_pub=None


             link=divs_in_section.find('a')
             has_img='Non'
             if link:
              link_page=link['href']
              t=link.find(['h1','h3','p'],{'class':lambda d:d and(d.startswith('article__title'))})
              if t:
                title_page_Acceuil=t.getText()
              if link_page.startswith(url):
                driver.get(link_page)
                html_article = BeautifulSoup(driver.page_source, 'html.parser')
                body_page_2=html_article.find('body')
                if body_page_2:
                   main_page=body_page_2.find('main')
                   if main_page:
                      section=main_page.find('section',class_=lambda x:x and (x.startswith('article')))
                      section_live=main_page.find('section',{'class':lambda d:d and (d.startswith('sirius-live'))})
                      article_art=main_page.find('article',{'class':lambda v:v and (v.startswith('article'))})
                      if section_live:
                          s_1_live=section_live.find('section',class_='live__hero')
                          if s_1_live:
                              article_info=s_1_live.find('section',class_=lambda c:c and(c.startswith('hero__live-info')))
                              s_2_live=s_1_live.find('section',class_=('hero__live-content'))
                              if s_2_live:
                                  img_live=s_2_live.find('picture')
                                  if img_live:
                                      has_img='Oui'
                                  else:
                                      has_img='Non'
                              if article_info:
                                  section_h_p=article_info.find('section',class_=lambda l:l and(l.startswith('title')) )
                                  if section_h_p:
                                      title_art=section_h_p.find('h1',class_=lambda h:h and(h.startswith('title__sirius-live')))
                                      if title_art:
                                          title=title_art.getText()
                                      else:
                                          title='Non trouvee'
                                      pp=section_h_p.find('p',class_=lambda j:j and ( j.startswith('summary__sirius-live')))
                                      if pp:
                                          paragraphe=pp.getText()
                                      else:
                                          paragraphe='Non trouvee'
                                      
                                      categorie='Non trouvee'
                                      auteur_name='Non trouvee'
                                       
                              if title is None:
                                  title='Non Trouvee'
                              if title_page_Acceuil is None:
                                  title_page_Acceuil='Non Trouvee' 
                              
                              if date_text is None:
                                  date_text=fonction_date_exportation().strftime('%Y-%m-%d %H:%M:%S')
                              
                              creer_article(title_page_Acceuil,title, link_page,date_text,auteur_name,paragraphe,has_img,Sous_Actualite,Date_Exportation,categorie,order)
                              initialisation_varialbes(title,date_text,auteur_name,paragraphe,has_img,Sous_Actualite,categorie,order)
                      
                      if section:                                      
                           sous_section=section.find('section',{'class':lambda g:g and(g.startswith('zone'))})#,'zone--article','zone--article-premium' ,'old__zone'])
                           if sous_section:
                               header = sous_section.find(['header', 'section'], class_=lambda x: x and x.startswith('article__header'))
                                                                                                    
                               if header:
                                   
                                   div_t_p=header.find('div',{'class':lambda g:g and (g.startswith('article__header-wrap'))})
                                   if div_t_p:
                                      title1 = div_t_p.find('h1', class_=lambda x: x.startswith('article__title') or x.startswith('title'))
                                      if title1:
                                         title = title1.getText()
                                      else:
                                           title = "Titre non trouvé"
                                      p= div_t_p.find('p', class_=lambda x: x.startswith('article__desc') or x.startswith('summary__sirius-live'))
                                      if p:
                                           paragraphe= p.getText()
                                      else:
                                            paragraphe="Paragraphe non trouve"
                                      ul_article=div_t_p.find('ul')
                                      if ul_article:
                                         li=ul_article.find_all('li', class_=lambda x: x.startswith('breadcrumb'))
                                         if li:
                                            categorie=" "
                                            for i in li:
                                             if i:
                                               cat=i.find('a')
                                               textcat = cat.get_text(strip=True)
                                               categorie=categorie+" "+textcat
                                             else:
                                               categorie=" Categorie non Trouvee "  
                                      p_auteur=div_t_p.find(['p','span'],{'class':lambda x:x and(x.startswith('meta'))})
                                                                        
                                      if p_auteur: 
                                         auteur1=p_auteur.find('span',class_="meta__author meta__author--no-after")
                                         auteur2=p_auteur.find_all('a',class_=lambda x: x.startswith('article__author-link'))
                                         if auteur2:
                                             auteur_name=""
                                             for a in auteur2:
                                              if a:
                                                 auteur_name1=a.get_text(strip=True)
                                                 auteur_n=auteur_name+"/ "+auteur_name1
                                                 auteur_name=supprimer_slashes(auteur_n)
                            
                                         elif auteur1:
                                               auteur_name=auteur1.get_text(strip=True)
                                         else :
                                               auteur_name="Auteur non Trouve"
                                      date_article=div_t_p.find('section',class_="meta__date-reading")
                                      if date_article:                             
                                         date_element = date_article.find('span', class_=lambda x: x.startswith('meta__date meta__date--header') or  x.startswith('meta__date') or x.startswith('meta__publisher'))
                                         if date_element:
                                            date_pub=date_element.get_text()
                                            date_publication=gerer_date(date_pub)
                                            
                                      image=div_t_p.find('img')
                                      if image:
                                          has_img='Oui'
                                      else:
                                         has_img='Non'                             
                                      if date_publication is None or date_element is None:
                                         date_publication=fonction_date_exportation().strftime("%Y-%m-%d %H:%M:%S")

                                      creer_article(title_page_Acceuil,title, link_page,date_publication,auteur_name,paragraphe,has_img,Sous_Actualite,Date_Exportation,categorie,order)
                                      
                                          
                                      initialisation_varialbes(title,date_text,auteur_name,p,has_img,Sous_Actualite,categorie,order)
                                   else:
                                      title1 = header.find('h1', class_=lambda x: x.startswith('article__title') or x.startswith('title'))
                                      if title1:
                                         title = title1.getText()
                                      else:
                                           title = "Titre non trouvé"
                                      p= header.find('p', class_=lambda x: x.startswith('article__desc') or x.startswith('summary__sirius-live'))
                                      if p:
                                           paragraphe= p.getText()
                                      else:
                                            paragraphe="Paragraphe non trouve"
                                      ul_article=header.find('ul')
                                      if ul_article:
                                         li=ul_article.find_all('li', class_=lambda x: x.startswith('breadcrumb'))
                                         if li:
                                            categorie=" "
                                            for i in li:
                                             if i:
                                               cat=i.find('a')
                                               textcat = cat.get_text(strip=True)
                                               categorie=categorie+" "+textcat
                                             else:
                                               categorie=" Categorie non Trouvee "  
                                      p_auteur=header.find(['p','span','section'],{'class':lambda x:x and(x.startswith('meta') or x.startswith('article__authors') )})
                                                                        
                                      if p_auteur: 
                                         auteur1=p_auteur.find('span',class_="meta__author meta__author--no-after")
                                         auteur2=p_auteur.find_all('a',class_=lambda x:x and(x.startswith('article__author-link') or x.startswith('article__author')))
                                         if auteur2:
                                             auteur_name=""
                                             for a in auteur2:
                                              if a:
                                                 auteur_name1=a.get_text(strip=True)
                                                 auteur_n=auteur_name+"/ "+auteur_name1
                                                 auteur_name=supprimer_slashes(auteur_n)
                            
                                         elif auteur1:
                                               auteur_name=auteur1.get_text(strip=True)
                                         else :
                                               auteur_name="Auteur non Trouve"
                                      date_article=header.find(['section','p'],{'class':lambda c:c and(c.startswith('meta'))})
                                      if date_article:                             
                                         date_element = date_article.find('span', class_=lambda x: x.startswith('meta__date meta__date--header') or  x.startswith('meta__date') or x.startswith('meta__publisher'))
                                         if date_element:
                                            date_pub=date_element.get_text()
                                            date_publication=gerer_date(date_pub)
                                            
                                      image=header.find('img')
                                      if image:
                                          has_img='Oui'
                                      else:
                                         has_img='Non'                             
                                      
                                      if date_publication is None or date_element is None:
                                          date_publication=fonction_date_exportation().strftime("%Y-%m-%d %H:%M:%S")
                                      creer_article(title_page_Acceuil,title, link_page,date_publication,auteur_name,paragraphe,has_img,Sous_Actualite,Date_Exportation,categorie,order)
                                     
                                      initialisation_varialbes(title,date_text,auteur_name,p,has_img,Sous_Actualite,categorie,order)
                      if article_art:
                          section_imag=article_art.find('section',{'class':lambda f:f and(f.startswith('article__cover'))})
                          section_info=article_art.find('section',{'class':lambda f:f and(f.startswith('article__head'))})
                          if section_info:
                                   
                                   div_t_p=section_info.find('div',{'class':lambda g:g and (g.startswith('article__header-wrap'))})
                                   if div_t_p:
                                      title1 = div_t_p.find('h1', class_=lambda x: x.startswith('article__title') or x.startswith('title'))
                                      if title1:
                                         title = title1.getText()
                                      else:
                                           title = "Titre non trouvé"
                                      p= div_t_p.find('p', class_=lambda x: x.startswith('article__desc') or x.startswith('summary__sirius-live'))
                                      if p:
                                           paragraphe= p.getText()
                                      else:
                                            paragraphe="Paragraphe non trouve"
                                      ul_article=div_t_p.find('ul')
                                      if ul_article:
                                         li=ul_article.find_all('li', class_=lambda x: x.startswith('breadcrumb'))
                                         if li:
                                            categorie=" "
                                            for i in li:
                                             if i:
                                               cat=i.find('a')
                                               textcat = cat.get_text(strip=True)
                                               categorie=categorie+" "+textcat
                                             else:
                                               categorie=" Categorie non Trouvee "  
                                      p_auteur=div_t_p.find(['p','span'],{'class':lambda x:x and(x.startswith('meta'))})
                                                                        
                                      if p_auteur: 
                                         auteur1=p_auteur.find('span',class_="meta__author meta__author--no-after")
                                         auteur2=p_auteur.find_all('a',class_=lambda x: x.startswith('article__author-link'))
                                         if auteur2:
                                             auteur_name=""
                                             for a in auteur2:
                                              if a:
                                                 auteur_name1=a.get_text(strip=True)
                                                 auteur_n=auteur_name+"/ "+auteur_name1
                                                 auteur_name=supprimer_slashes(auteur_n)
                            
                                         elif auteur1:
                                               auteur_name=auteur1.get_text(strip=True)
                                         else :
                                               auteur_name="Auteur non Trouve"
                                      date_article=div_t_p.find('section',class_="meta__date-reading")
                                      if date_article:                             
                                         date_element = date_article.find('span', class_=lambda x: x.startswith('meta__date meta__date--header') or  x.startswith('meta__date') or x.startswith('meta__publisher'))
                                         if date_element:
                                            date_pub=date_element.get_text()
                                            
                                            date_publication=gerer_date(date_pub)
                                            
                                      if section_imag:
                                       image=section_imag.find(['img','picture','figure'])
                                       if image:
                                          has_img='Oui'
                                
                                      if date_publication is None or date_element is None:
                                        date_publication=fonction_date_exportation().strftime("%Y-%m-%d %H:%M:%S")
                                     
                                      creer_article(title_page_Acceuil,title, link_page,date_publication,auteur_name,paragraphe,has_img,Sous_Actualite,Date_Exportation,categorie,order)
                                      
                                      initialisation_varialbes(title,date_publication,auteur_name,p,has_img,Sous_Actualite,categorie,order)
                                  
                          





                      
################################################################ fonction_extraire donnee section d'order                   ################################################################
def fonction_exportation_articles_order_1(section_order_1,driver,Sous_Actualite,order):
    if section_order_1:
        divs_in_section=section_order_1.find('div',class_=('article article--main'))
        if divs_in_section:
             sous_divs=divs_in_section.find('div',{'class':lambda f:f and(f.startswith('article__re'))})
             
             fonction_find_Article(divs_in_section,driver,'Non',order)
             if sous_divs:
                 list_divs=sous_divs.find_all('div',{'class':lambda x:x and(x.startswith('article article--related'))})
                 if list_divs:
                     
                     for i in list_divs:
                         if i:
                             fonction_find_Article(i,driver,Sous_Actualite,order)
             
            
################################################################ fonction_extraire donnee section d'order                   ################################################################
def fonction_exportation_articles_order_2(section_order_2,driver,Sous_Actualite,order) :
    if section_order_2:
        for i_2 in section_order_2:
            fonction_find_Article(i_2,driver,Sous_Actualite,order)

            
################################################################ fonction_extraire donnee section d'order 3                  ################################################################
def fonction_exportation_articles_order_3(section_order_3,driver,Sous_Actualite,order):
    if section_order_3:
        for i_3 in section_order_3:
            fonction_find_Article(i_3,driver,Sous_Actualite,order)
################################################################ fonction_extraire donnee section d'order 4                  ################################################################

################################################################# save in file CSV   ###########################################


###############################################################################  fonction extraire dans les divs card list  #######################

def findAllArticles(url):
    import locale
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    # Configuration des options de Chrome pour désactiver les notifications et les publicités
    driver = WebDriverSingleton.get_instance()
        
        # Définir la localisation française
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    
    driver.get(url)
    time.sleep(2)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    html = BeautifulSoup(driver.page_source, 'html.parser') 
    body_page=html.find('body')
    if body_page:  
                                          
     main_page=body_page.find('main')#balise main de la page 
     if main_page: 
      
      div_princ=main_page.find('div',id='habillagepub') #le premiere div apres le main
      if div_princ:
       zone_1=div_princ.find('section',{'class':lambda k:k and(k.startswith('zone zone--homepage'))})
       zone_2=div_princ.find('section',{'class':lambda c:c and(c.startswith('area area--runner'))})
       zone_3=div_princ.find('section',{'class':lambda j:j and(j.startswith('area area--river'))})
       if zone_1:
           section_order_1=zone_1.find('section',{'class':lambda j:j and(j.startswith('area area--m'))})# or j.startswith('area area--r'))})
           if section_order_1: 
                   order = "1"
                   Sous_Actualite="Oui"
                   fonction_exportation_articles_order_1(section_order_1,driver,Sous_Actualite,order) 
       if zone_2:
           section_order_2=zone_2.find_all('div',{'class':lambda j:j and(j.startswith('article'))})# or j.startswith('area area--r'))})
           if section_order_2:
                   
                   order = "2"
                   Sous_Actualite="Non"
                   fonction_exportation_articles_order_2(section_order_2,driver,Sous_Actualite,order)   
       if zone_3:
           section_order_3=zone_3.find_all('div',{'class':lambda j:j and(j.startswith('article article--river'))})# or j.startswith('area area--r'))})
           if section_order_3:
                  
                   order = "3"
                   Sous_Actualite="Non"
                   fonction_exportation_articles_order_3(section_order_3,driver,Sous_Actualite,order) 
         




def Lemonde_Find_All_Article(d):
    global scraping_active
    i = 0
    while scraping_active:
     try:
        print('***'*30)
        print('')
        print(" Le scraping de Lemonde a commencé à l'itération numéro :",i)
        print('')
        print('***'*30)
        findAllArticles(url) 
        i=i+1
        print('***'*30)
        print('')
        print(" le scrping de Lemonde a Termine l'Iteration numero : ",i)
        print('')
        print('***'*30)
        
         # Appeler la fonction pour trouver tous les articles
        time.sleep(d)  # Attendre 60 secondes avant de recommencer (ou ajuster selon vos besoins)
     except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        break 

def fonction_Arrete_Script():
    global scraping_active
    scraping_active = False
    WebDriverSingleton.quit_instance()
    print("***"*30)
    print("")
    print("Le scraping sur Lemonde s'est arrêté avec succès.")
    print('')
    print('***'*30)



def start_scraping(d):
    global scraping_active
    scraping_active = True
    scraping_thread = threading.Thread(target=Lemonde_Find_All_Article, args=(d,))
    scraping_thread.start()


