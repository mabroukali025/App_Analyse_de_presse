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
from datetime import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import date, datetime, timedelta
import pytz
import threading
import re
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pytz


url="https://www.lemonde.fr/"



import pytz
from datetime import datetime
""""
def fonction_date_exportation():
    french_tz = pytz.timezone('Europe/Paris')
    now = datetime.now(french_tz)  # Récupère l'heure actuelle avec le fuseau horaire
    return now

# Appel de la fonction pour obtenir la date et l'heure actuelles sous forme d'objet datetime
date_exportation_article_reconverted = fonction_date_exportation()

# Si tu veux convertir cet objet datetime en chaîne formatée
date_exportation_article = date_exportation_article_reconverted.strftime('%Y-%m-%dT%H:%M:%S')


print("Date exportation (chaîne) :", date_exportation_article)

"""

    
    
######################################################################




# Format the date and time
#Date_Exportation = now.strftime('%Y-%m-%dT%H:%M:%S')
#date_exportation_article = datetime.strptime(Date_Exportation, '%Y-%m-%dT%H:%M:%S')



######################################################## fonction principle  ##########################################
scraping_active = True

class WebDriverSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if WebDriverSingleton._instance is None:
            
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
            import locale
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
            
            
            
        return WebDriverSingleton._instance
    @staticmethod
    def is_session_valid():
        """Vérifie si la session WebDriver est encore active et valide."""
        try:
            # Effectuer une action simple pour vérifier la validité de la session
            WebDriverSingleton._instance.current_url  # Vérifier l'URL courante
            return True
        except (InvalidSessionIdException, WebDriverException):
            return False

    @staticmethod
    def quit_instance():
        if WebDriverSingleton._instance is not None:
            WebDriverSingleton._instance.quit()
            WebDriverSingleton._instance = None






########################################################################

def creer_article(titre_page_accueil, titre, lien, date_text, auteur_name, paragraphe, has_image, Actualite, Date_Exportation, categorie, order):
    #from django.utils import timezone
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
    
    # Exemple de manipulation pour rendre la date timezone-aware avant enregistrement
    #if article.date_publication.tzinfo is None:
        #article.date_publication = timezone.make_aware(article.date_publication, timezone.get_current_timezone())

    #if article.date_exportation.tzinfo is None:
        #article.date_exportation = timezone.make_aware(article.date_exportation, timezone.get_current_timezone())
    article.save()
    print(' ')
    print('\033[94m**************************************************** Save with success in LeMonde ***********************************\033[0m')
    print(' ')
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
 #print(' la date de publication est commasser par le :',chaine)
 if chaine and chaine.startswith('Publié le '):
    x=len("Publié le ")
    chaine=chaine[x:]
    # Nettoyer la chaîne en enlevant les espaces superflus et les virgules
    chaine = chaine.strip().replace(',', '')
    
    # Trouver la partie date
    date_partie = chaine.split('à')[0].strip()
    
    # Trouver la partie heure
    heure_partie = chaine.split('à')[1].strip()
    #print('partie date ',date_partie)
    #print('partie heur ',heure_partie)
    # Remplacer les mois français par leurs équivalents anglais
    for mois_fr, mois_en in mois_mapping.items():
        if mois_fr in date_partie:
            date_partie = date_partie.replace(mois_fr, mois_en)
            
            break
    
   
    
    # Combiner la date et l'heure
    if not isinstance(date_partie,str):
        date_heure_str = date_partie.strftime('%Y-%m-%d') + ' ' + heure_partie.replace('h', ':') + ':00'
        print('date heur str est : ',date_heure_str)
        # Convertir en objet datetime
        try:
            if not isinstance(date_heure_str,str):
                # Assumer que la chaîne fournie est en heure locale (Europe/Paris)
                date_publication_obj = datetime.strptime(date_heure_str, '%Y-%m-%dT%H:%M:%S')
                date_publication_obj = tz.localize(date_publication_obj)  # Localiser en Europe/Paris
                return date_publication_obj.strftime('%Y-%m-%dT%H:%M:%S')
        except ValueError as e:
            print(f"Erreur de conversion pour la chaîne : {date_heure_str}. Détails : {e}")
            return None
    else:
        return  None


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
    date_exportation_article=obtenir_date_exportation()
    if chaine and chaine.startswith("Publié aujourd’hui à"):
        return convertir_chaine_en_date_Lemonde(chaine)
    elif chaine and chaine.startswith("Publié hier à"):
        return date_publiee_hier(chaine)
    elif chaine and chaine.startswith("Publié le"):
        return date_publier_le(chaine)  # À implémenter si nécessaire
    else:
        return date_exportation_article  # Assurez-vous que cette variable est définie


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
        date_exportation_article=obtenir_date_exportation()
        heure_str = extraire_heure_Lemonde(chaine)
        # Convertir l'heure au format HH:MM
        heure_formatee = heure_str.replace('h', ':')
        date_exportation = date_exportation_article
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
    if chaine and chaine.startswith("Publié hier à "):
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
    while texte and texte.startswith("/"):
        texte = texte[1:]
    while texte and  texte.endswith("/"):
        texte = texte[:-1]
    return texte

##############################################################################################
def remove_characters(text, num_characters):
   
    if num_characters < 0:
        raise ValueError("Le nombre de caractères à supprimer doit être positif")
    return text[num_characters:]

###########################################################################################################################
from datetime import datetime

def obtenir_date_exportation():
    # Define the French time zone
    french_tz = pytz.timezone('Europe/Paris')

    # Get the current date and time in the French time zone
    now = datetime.now(french_tz)
    now = datetime.now()  # Obtenir la date et l'heure actuelles
    return datetime.strptime(now.strftime('%Y-%m-%dT%H:%M:%S'), '%Y-%m-%dT%H:%M:%S')



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
             # Utilisation
             date_exportation_article = obtenir_date_exportation()
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
              t=link.find(['h1', 'h3', 'p','a'], class_=lambda class_name: class_name and (class_name.startswith('article__title') or class_name.startswith('lmd-article__title')))
              if t:
                title_page_Acceuil=t.getText()
              else:
                  title_page_Acceuil=link.getText()
              if link_page.startswith(url):
                driver.get(link_page)
                html_article = BeautifulSoup(driver.page_source, 'html.parser')
                body_page_2=html_article.find('body')
                if body_page_2:
                   #print(' je suis dans body __2')
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
                                  date_text=date_exportation_article
                              


                              
                              #print("")
                              #print('****'*23)
                              #print("Date Text:", date_text)
                              #print(' link de la page est : ',link_page)
                              #print('****'*23)
                              #print("")

                              creer_article(title_page_Acceuil,title, link_page,date_text,auteur_name,paragraphe,has_img,Sous_Actualite,date_exportation_article,categorie,order)
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
                                         date_publication=date_exportation_article
                                      #print('******************** date exportation est  :',date_exportation_article)
                                      creer_article(title_page_Acceuil,title, link_page,date_publication,auteur_name,paragraphe,has_img,Sous_Actualite,date_exportation_article,categorie,order)
                                      #print("")
                                      #print('****'*23)
                                      #print("Date Text:", date_publication)
                                      #print(' link de la page est : ',link_page)
                                      #print('****'*23)
                                      #print("")
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
                                          date_publication=date_exportation_article
                                      #print('******************** date exportation est  :',date_exportation_article)
                                      #print("")
                                      #print('****'*23)
                                      #print("Date Text:", date_publication)
                                      #print(' link de la page est : ',link_page)
                                      #print('****'*23)
                                      #print("")
                                      creer_article(title_page_Acceuil,title, link_page,date_publication,auteur_name,paragraphe,has_img,Sous_Actualite,date_exportation_article,categorie,order)
                                      """
                                      print("Title Page (Accueil):",title_page_Acceuil)
                                      print("Title:",title)
                                      print("Link Page:",link_page)
                                      print("Date Text:", date_text)
                                      print("Auteur Name:",auteur_name)
                                      print("Paragraphe:", paragraphe)
                                      print("Has Image:", has_img)
                                      print("Sous Actualite:", Sous_Actualite)
                                      print("Date Exportation Article:",date_exportation_article)
                                      print("Categorie:", categorie)
                                      print("Order:", order)
                                      print("-" * 50)  # Séparateur pour chaque article
                                      """
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
                                        date_publication=date_exportation_article
                                      #print('******************** date exportation est  :',date_exportation_article)
                                      creer_article(title_page_Acceuil,title, link_page,date_publication,auteur_name,paragraphe,has_img,Sous_Actualite,date_exportation_article,categorie,order)
                                      #print("")
                                      #print('****'*23)
                                      #print("Date Text:", date_publication)
                                      #print(' link de la page est : ',link_page)
                                      #print('****'*23)
                                      #print("")
                                      #print('******************** date exportation est  :',date_exportation_article)
                                      initialisation_varialbes(title,date_publication,auteur_name,p,has_img,Sous_Actualite,categorie,order)
                                      #date_exportation_article=None
                                      """
                                      print("Title Page (Accueil):",title_page_Acceuil)
                                      print("Title:",title)
                                      print("Link Page:",link_page)
                                      print("Date Text:", date_text)
                                      print("Auteur Name:",auteur_name)
                                      print("Paragraphe:", paragraphe)
                                      print("Has Image:", has_img)
                                      print("Sous Actualite:", Sous_Actualite)
                                      print("Date Exportation Article:",date_exportation_article)
                                      print("Categorie:", categorie)
                                      print("Order:", order)
                                      print("-" * 50)  # Séparateur pour chaque article
                                      """
                          





                      
################################################################ fonction_extraire donnee section d'order                   ################################################################
def fonction_exportation_articles_order_1(section_order_1,driver,Sous_Actualite,order):
    if section_order_1:
        
        divs_in_section=section_order_1.find('h1',class_=('home-block-une__title'))
        div_article=section_order_1.find('div',class_=('article'))
        #sous_divs=section_order_1.find('div',{'class':lambda f:f and(f.startswith('home-block-une__grid'))})
        if divs_in_section:                                                                
            fonction_find_Article(divs_in_section,driver,'Non',order)
        if div_article:
            list_ul=div_article.find('ul',{'class':lambda x:x and(x.startswith('article_'))})
            if list_ul:
                list_lis=list_ul.find_all('li',{'class':lambda g:g and g.startswith('old__article')})
                for i in list_lis:
                     if i:
                      Sous_Actualite="Oui"
                      fonction_find_Article(i,driver,Sous_Actualite,order)
             
            
################################################################ fonction_extraire donnee section d'order                   ################################################################
def fonction_exportation_articles_order_2(section_order_2,driver,Sous_Actualite,order) :
    if section_order_2:
       
        sous_divs=section_order_2.find('div',{'class':lambda f:f and(f.startswith('home-block-une__grid'))})
        all_div=section_order_2.find_all('div',{'class':lambda f:f and(f.startswith('article article--headlines'))})
        if sous_divs:
                 #print('2 sous div ')                                                    
                 list_divs=sous_divs.find_all('div',{'class':lambda x:x and(x.startswith('home-block-une__une-related-articles'))})
                 if list_divs:
                     
                    for i_2 in list_divs:
                        all_articles=i_2.find_all('article',{'class':lambda x:x and(x.startswith('lmd-article'))})
                        if all_articles:                       
                            for art in all_articles:
                              if art:
                                  div_art=art.find('div',{'class':lambda x:x and(x.startswith('lmd-article__header'))})
                                  if div_art:
                                      div_h3=div_art.find('h3',{'class':lambda x:x and(x.startswith('lmd-article__title'))})
                                      if div_h3:
                                        fonction_find_Article(div_h3,driver,Sous_Actualite,order)
        if all_div:
            for i in all_div:
                fonction_find_Article(i,driver,Sous_Actualite,order)

            
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
      
       zone_1=div_princ.find('div',{'class':lambda k:k and(k.startswith('home-revo-top'))})
       zone_1_2=div_princ.find('section',{'class':lambda k:k and(k.startswith('zone zone--homepage'))})
       zone_2=div_princ.find('div',{'class':lambda c:c and(c.startswith('home-revo-top'))})
       zone_3=div_princ.find('section',{'class':lambda j:j and(j.startswith('area area--river'))})
       
       if zone_1 is not None or zone_1_2 is not None:
           
           if zone_1_2:                                            
              section_order_1_2=zone_1_2.find('section',{'class':lambda j:j and(j.startswith('area area--main old__area-'))})
              if section_order_1_2 : 
                   order = "1"
                   Sous_Actualite="Non"
                   
                   fonction_exportation_articles_order_1(section_order_1_2,driver,Sous_Actualite,order) 



           if zone_1:
              section_order_1=zone_1.find('div',{'class':lambda j:j and(j.startswith('home-block-une'))})# or j.startswith('area area--r'))})
              if section_order_1: 
                   order = "1"
                   Sous_Actualite="Non"
                   
                   fonction_exportation_articles_order_1(section_order_1,driver,Sous_Actualite,order) 



       if zone_2:
           section_order_2=zone_2.find('div',{'class':lambda j:j and(j.startswith('home-block-une'))})# or j.startswith('area area--r'))})
           if section_order_2:
                   
                   order = "2"
                   Sous_Actualite="Non"
                  
                   fonction_exportation_articles_order_2(section_order_2,driver,Sous_Actualite,order) 
       if zone_1_2:
           
            
           section_order_2=zone_1_2.find('section',{'class':lambda j:j and(j.startswith('area area--headlines old__area'))})# or j.startswith('area area--r'))})
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
         




import threading
import time

def Lemonde_Find_All_Article(d):
    global scraping_active
    print('')
    print('***************************************    Scripte LEMONDE         ***********************************')
    print('')
    if scraping_active==False:
        scraping_active=True
    i = 1
    while scraping_active:
        try:
            print('***' * 30)
            print(f"\n Le scraping de Lemonde a commencé à l'itération numéro : {i}\n")
            print('***' * 30)
            
            # Appeler la fonction pour trouver tous les articles
            # Utilisation
            date_exportation_article = obtenir_date_exportation()
            print('')
            print('             la date exportation est  : ',date_exportation_article )
            print('')
            findAllArticles(url)  # Assurez-vous que 'url' est défini quelque part

            print('***' * 30)
            print(f"\n Le scraping de Lemonde a terminé l'itération numéro : {i}\n")
            print('***' * 30)

            i += 1
            time.sleep(d)  # Attendre 'd' secondes avant la prochaine itération
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
            break

def fonction_Arrete_Script():
    global scraping_active
    scraping_active = False
    WebDriverSingleton.quit_instance()
    print('***' * 30)
    print("\nLe scraping sur Lemonde s'est arrêté avec succès.\n")
    print('***' * 30)

def start_scraping(d):
    global scraping_active
    scraping_active = True
    scraping_thread = threading.Thread(target=Lemonde_Find_All_Article, args=(d,))
    scraping_thread.start()


#Lemonde_Find_All_Article(25)