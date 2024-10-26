import threading
import locale
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException

# Classe singleton pour le WebDriver
class WebDriverSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if WebDriverSingleton._instance is None or not WebDriverSingleton.is_session_valid():
            chrome_options = Options()
            chrome_options.add_argument("--disable-features=NotificationPermissions")
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("start-maximized")
            chrome_options.add_argument("--headless")  # Mode headless si nécessaire
            
            service = Service(ChromeDriverManager().install())
            WebDriverSingleton._instance = webdriver.Chrome(service=service, options=chrome_options)

            # Configurer la locale en français
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        
        return WebDriverSingleton._instance

    @staticmethod
    def is_session_valid():
        """Vérifie si la session WebDriver est encore active et valide."""
        try:
            WebDriverSingleton._instance.current_url  # Vérifier l'URL courante
            return True
        except (InvalidSessionIdException, WebDriverException):
            return False

    @staticmethod
    def quit_instance():
        if WebDriverSingleton._instance is not None:
            WebDriverSingleton._instance.quit()
            WebDriverSingleton._instance = None

# Variables globales pour la gestion du scraping
scraping_active = False
threads = []

# Fonctions de démarrage et d'arrêt du scraping
def start_all_scraping(duree_value):
    #global scraping_active
    #scraping_active = True

    # Importer les fonctions de scraping de chaque site
    from AppScraping.Scriptes.Lemonde_Scraping import Lemonde_Find_All_Article
    from AppScraping.Scriptes.Liberation_Scraping import fonction_liberation
    from AppScraping.Scriptes.Lefigaro_Scraping import start_scraping

    # Démarre le scraping pour chaque site dans un thread
    threads.append(threading.Thread(target=Lemonde_Find_All_Article, args=(int(duree_value),)))
    threads[-1].start()

    threads.append(threading.Thread(target=fonction_liberation, args=(int(duree_value),)))
    threads[-1].start()

    threads.append(threading.Thread(target=start_scraping, args=(int(duree_value),)))
    threads[-1].start()

def stop_all_scraping():
    global scraping_active
    scraping_active = False

    # Arrêter le scraping pour chaque site
    from AppScraping.Scriptes.Lefigaro_Scraping import fonction_Arrete_Script
    fonction_Arrete_Script()
    
    from AppScraping.Scriptes.Liberation_Scraping import fonction_Arrete_Script
    fonction_Arrete_Script()
    
    from AppScraping.Scriptes.Lemonde_Scraping import fonction_Arrete_Script
    fonction_Arrete_Script()

    # Attendre que tous les threads se terminent
    for thread in threads:
        thread.join()
    threads.clear()  # Réinitialiser la liste des threads

# Exemple de démarrage du scraping
#if __name__ == "__main__":
    # Exemple d'utilisation
    #start_all_scraping()  # Démarrer le scraping pour 60 secondes
