# Imports standard Python
from datetime import datetime
import locale
import re

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ScrapingStatus
# Imports de bibliothèques tierces
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio
import pandas as pd
from io import BytesIO
import base64

# Imports Django
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Min, OuterRef, Subquery, Q
from django.contrib.auth.models import User

# Imports de votre application
#from .models import Article

from .forms import UserRegistrationForm



from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.views import View

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Chemin vers ton template de connexion



from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Connecter l'utilisateur automatiquement après l'inscription
            return redirect('home')  # Redirige vers la page d'accueil ou une autre page
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


from django.contrib.auth.decorators import user_passes_test

def staff_required(function=None, redirect_field_name='redirect_to', login_url='login'):
    """
    Décorateur pour restreindre l'accès aux utilisateurs qui sont staff.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
@staff_required
def admin_view(request):
    # Vue réservée aux administrateurs
    ...
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError

@csrf_protect
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        try:
            if form.is_valid():
                user = form.get_user()
                auth_login(request, user)
                if user.is_staff:
                    return redirect('scraping_page')  # Redirection pour les utilisateurs staff
                else:
                    return redirect('scraping_page')  # Redirection pour les autres utilisateurs
            else:
                raise ValidationError("Nom d'utilisateur ou mot de passe incorrect.")
        except ValidationError as e:
            messages.error(request, str(e))
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



def article_list(request):
    articles = Article.objects.all()
    
    # Récupérer et nettoyer les catégories
    categories = Article.objects.values_list('categorie', flat=True).distinct().order_by('categorie')
    categories = [categorie.strip() for categorie in categories if categorie.strip()]

    # Récupérer les paramètres de recherche
    search_site = request.GET.get('combobox_select_site', '').strip()
    search_order = request.GET.get('search_order', '').strip()
    search_date_debut = request.GET.get('search_date_debut', '').strip()
    search_date_fin = request.GET.get('search_date_fin', '').strip()
    search_titre = request.GET.get('search_titre', '').strip()
    search_description = request.GET.get('search_description', '').strip()
    search_author = request.GET.get('search_author', '').strip()
    search_categorie = request.GET.get('search_categorie', '').strip()
    search_date = request.GET.get('search_date', '').strip()
    search_mot_cle=request.GET.get('search_mot_cle','').strip()


    if search_mot_cle:
        mot_cle_in_titre=articles.filter(titre__icontains=search_mot_cle)
        mot_cle_in_description=articles.filter(description_article__icontains=search_mot_cle)
        mot_cle_in_auteur=articles.filter(nom_auteur__icontains=search_mot_cle)
        mot_cle_in_titre_page_accueil=articles.filter(	titre_page_accueil__icontains=search_mot_cle)
        articles=mot_cle_in_titre | mot_cle_in_description |mot_cle_in_auteur | mot_cle_in_titre_page_accueil 

    if search_site :
        articles = articles.filter(lien__icontains=search_site)
    if search_order:
        articles = articles.filter(ordre_actualite=search_order)
    try:
        if search_date and search_date.strip():
            search_date_form = datetime.strptime(search_date, '%Y-%m-%dT%H:%M')
            articles = articles.filter(date_publication__gte=search_date_form)
        else:
            search_date = None
    except ValueError:
        search_date = None
    if search_date_debut and search_date_fin:
        try:
            form_search_date_fin=datetime.strptime(search_date_fin, '%Y-%m-%dT%H:%M')
            form_search_date_debut = datetime.strptime(search_date_debut, '%Y-%m-%dT%H:%M')
            if search_date_fin>search_date_debut:
              articles = articles.filter(date_publication__range=(form_search_date_debut,form_search_date_fin))
        except ValueError:
            pass
    if search_titre:
      index_Titre = search_titre.find('|')
      if index_Titre != -1:
        partie1_Titre = search_titre[:index_Titre].strip()
        partie2_Titre = search_titre[index_Titre + 1:].strip()
        
        # Filtrer les articles par partie1_Titre et partie2_Titre séparément
        articles_partie1 = articles.filter(titre__icontains=partie1_Titre)
        articles_partie2 = articles.filter(titre__icontains=partie2_Titre)
        
        # Combiner les deux queryset
        articles = articles_partie1 | articles_partie2
      else:
        articles = articles.filter(titre__icontains=search_titre)
    
    
    
    if search_description:
      index_description=search_description.find('|')
      if index_description !=-1:
        partie_1_description=search_description[:index_description].strip()
        partie_2_description=search_description[index_description +1:].strip()
        articles_partie_1_description=articles.filter(description_article__icontains=partie_1_description)
        articles_partie_2_description=articles.filter(description_article__icontains=partie_2_description)
        articles = articles_partie_1_description | articles_partie_2_description
      else:  
        articles = articles.filter(description_article__icontains=search_description)
    if search_author:
        index_author = search_author.find('|')
        if index_author != -1:
            partie1_author = search_author[:index_author].strip()
            partie2_author = search_author[index_author+1:].strip()
            articles_partie1_author = articles.filter(nom_auteur__icontains=partie1_author)
            articles_partie2_author=articles.filter(nom_auteur__icontains=partie2_author)
            articles = articles_partie1_author | articles_partie2_author
        else:
            articles = articles.filter(nom_auteur__icontains=search_author)
    if search_categorie:
        articles = articles.filter(categorie__icontains=search_categorie)
    
    context = {
        'articles': articles,
        'categories': categories,
        
    }

    if any([search_site, search_order, search_date_debut, search_date_fin,
            search_titre, search_description, search_author, search_categorie, search_date]):
        context.update({
            'search_site': '',
            'search_order': '',
            'search_date_debut': '',
            'search_date_fin': '',
            'search_titre': '',
            'search_description': '',
            'search_author': '',
            'search_categorie': '',
            'search_date': '',
        })
    return render(request, 'Donee.html', context)




 # Assurez-vous que le modèle Article est correctement importé

from django.shortcuts import render
from django.db import transaction
from .models import Article

def remove_duplicate_articles(request):
    try:
        with transaction.atomic():
            # Étape 1: Récupérer tous les articles et les trier par date d'exportation ASC
            articles = Article.objects.order_by('date_exportation')

            # Étape 2: Initialiser les variables pour la logique de suppression
            seen_articles = {}
            to_delete = set()  # Utiliser un set pour éviter les doublons dans la liste de suppression

            # Étape 3: Itérer sur les articles, marquer les doublons et les ajouter à la liste de suppression
            for article in articles:
                unique_key = (
                    article.titre,
                    article.lien,
                    article.description_article,
                    article.ordre_actualite
                )

                if unique_key in seen_articles:
                    # Comparer les dates d'exportation pour garder l'article avec la date la plus ancienne
                    if seen_articles[unique_key].date_exportation > article.date_exportation:
                        # L'article actuel a une date d'exportation plus ancienne, supprimer l'ancien
                        to_delete.add(seen_articles[unique_key])
                        seen_articles[unique_key] = article
                    else:
                        # L'article actuel a une date d'exportation plus récente, supprimer l'actuel
                        to_delete.add(article)
                else:
                    # Conserver le premier article unique avec ce `unique_key`
                    seen_articles[unique_key] = article

            # Supprimer les articles marqués
            if to_delete:
                Article.objects.filter(id__in=[article.id for article in to_delete]).delete()

            # Nombre d'articles supprimés
            message = f"Suppression réussie : {len(to_delete)} articles en double supprimés."

        # Afficher tous les articles restants après la suppression
        articles_remaining = Article.objects.order_by('date_exportation')

        context = {
            'message': message,
            'articles': articles_remaining,
        }
        return render(request, 'Statistiques_Recherche.html', context)

    except Exception as e:
        # Gérer les exceptions ici
        print(f"Error deleting duplicate articles: {e}")
        return render(request, 'error.html', {'error_message': 'Une erreur est survenue lors de la suppression des articles en double.'})

def page_Acceuil(request):
 context={}
 template=loader.get_template("page_Acceuil.html")
 return HttpResponse(template.render(context,request))

def home(request):
    context = {}  # Vous pouvez ajouter des données contextuelles si nécessaire
    template = loader.get_template("registration/login.html")
    #template = loader.get_template("scraping_page.html")
    return HttpResponse(template.render(context, request))

def scraping_page(request):
    # Logique de vue pour la page de scraping
    context = {
        # Ajoutez des données contextuelles si nécessaire
    }
    return render(request, 'scraping_page.html', context)

def admin_scraping_page(request):
    context={

    }
    return render(request, 'admin_scraping.html', context)

def gestion_donnee_page(request):
    # Logique de vue pour la page de gestion des données
    context = { }
    template = loader.get_template("Donee.html")
    return HttpResponse(template.render(context, request))

def statistiques_page(request):
    # Logique de vue pour la page des statistiques
    context = {
        # Ajoutez des données contextuelles si nécessaire
    }
    return render(request, 'statistiques.html', context)

def Statistiques_Recherche(request):
    # Logique de vue pour la page des statistiques
    context = {
        # Ajoutez des données contextuelles si nécessaire
    }
    return render(request, 'Statistiques_Recherche.html', context)
#admin_Gestion_Donnee

def admin_Gestion_Donnee(request):
    # Logique de vue pour la page des statistiques
    context = {
        # Ajoutez des données contextuelles si nécessaire
    }
    return render(request, 'admin_Gestion_Donnee.html', context)

from django.shortcuts import render
from django.db import models
import pandas as pd
import plotly.express as px
import plotly.io as pio

from .models import Article

def article_statistics(request):
    if request.method == 'GET':
        try:
            # Étape 1 : Calculer les statistiques
            category_counts = Article.objects.values('categorie').annotate(count=models.Count('id')).order_by('-count')

            # Étape 2 : Créer un DataFrame avec les données
            df = pd.DataFrame(category_counts)

            # Vérifier si le DataFrame est vide
            if df.empty:
                return render(request, 'statistiques.html', {'error': 'Aucune donnée disponible pour afficher les statistiques.'})

            # Étape 3 : Créer un graphique à barres avec Plotly
            fig = px.bar(df, x='categorie', y='count', 
                         labels={'categorie': 'Catégories', 'count': 'Nombre d\'articles'},
                         title='Nombre d\'articles par catégorie')

            # Étape 4 : Convertir la figure Plotly en HTML
            plot_html = pio.to_html(fig, full_html=False)

            # Étape 5 : Rendre le template avec le graphique
            return render(request, 'statistiques.html', {'plot_html': plot_html})
        except Exception as e:
            return render(request, 'statistiques.html', {'error': str(e)})
    else:
        return render(request, 'statistiques.html', {'error': 'Invalid request method.'})


@csrf_exempt



def extract_domain(url):
    """
    Fonction pour extraire le nom de domaine d'une URL.
    """
    match = re.search(r'www\.(.*?)(\.fr|\.com)', url)
    return match.group(1) if match else url

def statistics_site_categorie(request):
    if request.method == 'GET':
        try:
            # Étape 1 : Extraire le nom de domaine pour chaque article et le stocker dans un DataFrame
            articles = Article.objects.values('lien', 'categorie')
            df = pd.DataFrame(list(articles))

            # Nettoyer les noms de domaine
            df['site'] = df['lien'].apply(extract_domain)

            # Calculer le nombre total d'articles par site
            total_counts = df.groupby('site').size().reset_index(name='total_count')

            # Calculer le nombre d'articles par site et catégorie
            category_counts = df.groupby(['site', 'categorie']).size().reset_index(name='count')

            # Fusionner les DataFrames pour calculer les pourcentages
            df_merged = pd.merge(category_counts, total_counts, on='site')
            df_merged['percentage'] = (df_merged['count'] / df_merged['total_count']) * 100

            # Vérifier si le DataFrame est vide
            if df_merged.empty:
                return render(request, 'statistiques.html', {'error': 'Aucune donnée disponible pour afficher les statistiques.'})

            # Étape 2 : Créer un graphique à barres Plotly pour afficher les pourcentages
            fig = px.bar(df_merged, x='categorie', y='percentage', color='site',
                         labels={'categorie': 'Catégorie', 'percentage': 'Pourcentage'},
                         title='Répartition des articles par catégorie pour chaque site')

            # Étape 3 : Convertir la figure Plotly en HTML
            plot_html = pio.to_html(fig, full_html=False)

            # Étape 4 : Rendre le template avec le graphique
            return render(request, 'statistiques.html', {'plot_html': plot_html})
        except Exception as e:
            return render(request, 'statistiques.html', {'error': str(e)})
    else:
        return render(request, 'statistiques.html', {'error': 'Invalid request method.'})

from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from AppScraping.models import ScrapingStatus

# Déclarez la variable globale pour stocker la valeur du combobox
selected_value_global = None

# Vue pour démarrer le scraping
def find_articles(request):
    global selected_value_global  # Accéder à la variable globale
    
    if request.method == 'POST':
        # Récupérer la valeur du combobox et la stocker dans la variable globale
        selected_value_global = request.POST.get('combobox', None)
        duree_value = request.POST.get('textfield1')
        status, created = ScrapingStatus.objects.get_or_create(id=1)
        status.is_scraping = True
        status.save()
        
        # Démarrer le scraping selon l'option sélectionnée
        if selected_value_global == "option1":
            from AppScraping.Scriptes.Lemonde_Scraping import Lemonde_Find_All_Article
            Lemonde_Find_All_Article(int(duree_value))
        elif selected_value_global == "option2":
            from AppScraping.Scriptes.Liberation_Scraping import fonction_liberation
            fonction_liberation(int(duree_value))
        elif selected_value_global == "option3":
            from AppScraping.Scriptes.Lefigaro_Scraping import start_scraping
            start_scraping(int(duree_value))
    
    # Afficher la page de scraping avec la valeur sélectionnée
    return render(request, 'scraping_page.html', {'selected_value': selected_value_global})


def get_scraping_status(request):
    status = ScrapingStatus.get_status()  # Assurez-vous que cette méthode existe et retourne un objet avec l'attribut `is_scraping`
    return JsonResponse({'is_scraping': status.is_scraping if status else False})

############################################################" Arrete le Scripte ###########################"
# Fonction pour arrêter le scraping
def arreter_scraping(selected_value):
    status, created = ScrapingStatus.objects.get_or_create(id=1)
    
    # Fonction d'arrêt pour chaque scraper
    if selected_value == 'option3':
        from AppScraping.Scriptes.Lefigaro_Scraping import fonction_Arrete_Script
        fonction_Arrete_Script()
    elif selected_value == 'option2':
        from AppScraping.Scriptes.Liberation_Scraping import fonction_Arrete_Script
        fonction_Arrete_Script()
    elif selected_value == 'option1':
        from AppScraping.Scriptes.Lemonde_Scraping import fonction_Arrete_Script
        fonction_Arrete_Script()
    else:
        return False

    # Mettre à jour le statut de scraping à False
    status.is_scraping = False
    status.save()
    return True

# Vue pour arrêter le scraping
def arreter_scraping_view(request):
    global selected_value_global  # Utiliser la variable globale
    
    if request.method == 'POST':
        if selected_value_global:
            # Appeler la fonction pour arrêter le scraping avec selected_value_global
            result = arreter_scraping(selected_value_global)
            if result:
                return redirect('scraping_page')  # Rediriger vers la page de scraping
            else:
                return HttpResponseBadRequest('Valeur sélectionnée invalide.')
        else:
            return HttpResponseBadRequest('Aucune valeur sélectionnée.')
    else:
        return HttpResponseBadRequest('Méthode non autorisée.')

import re
import unicodedata

def remove_accents(input_str):
    
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def highlight_keywords(text, keyword):
    
    # Supprimer les accents des chaînes de texte et de mot-clé pour la comparaison
    text_no_accents = remove_accents(text)
    keyword_no_accents = remove_accents(keyword)

    # Échapper les caractères spéciaux dans le mot clé pour éviter les problèmes avec les expressions régulières
    escaped_keyword = re.escape(keyword_no_accents)

    # Utiliser une expression régulière pour trouver les occurrences du mot clé en ignorant la casse
    def highlight_match(match):
        #return f'<mark>{match.group(0)}</mark>'
        return f'<mark style="background-color: gree; color: black; font-size: 18px;">{match.group(0)}</mark>'

    # Remplacer toutes les occurrences du mot-clé par la version surlignée
    highlighted_text = re.sub(
        fr'(?i){escaped_keyword}',  # (?i) rend la recherche insensible à la casse
        highlight_match,
        text_no_accents
    )

    return highlighted_text

from django.shortcuts import render
from datetime import datetime
from .models import Article
from django.core.paginator import Paginator

 # Assurez-vous que cette fonction est correctement définie

def Statistiques_mot_cle(request):
    articles = Article.objects.all()
    categories = Article.objects.values_list('categorie', flat=True).distinct().order_by('categorie')
    categories = [categorie.strip() for categorie in categories if categorie.strip()]

    # Récupérer les paramètres de recherche
    search_site = request.GET.get('combobox_select_site', '').strip()
    search_order = request.GET.get('search_order', '').strip()
    search_date_debut = request.GET.get('search_date_debut', '').strip()
    search_date_fin = request.GET.get('search_date_fin', '').strip()
    search_categorie = request.GET.get('search_categorie', '').strip()
    search_date = request.GET.get('search_date', '').strip()
    search_mot_cle = request.GET.get('search_mot_cle', '').strip()

    # Séparer les parties du mot-clé si nécessaire
    index_mot = search_mot_cle.find('|')
    partie1_mot = search_mot_cle[:index_mot].strip() if index_mot != -1 else search_mot_cle.strip()
    partie2_mot = search_mot_cle[index_mot + 1:].strip() if index_mot != -1 else None

    # Filtrer les articles en fonction des critères de recherche
    if search_site:
        articles = articles.filter(lien__icontains=search_site)
    if search_order:
        articles = articles.filter(ordre_actualite=search_order)
    try:
        if search_date:
            search_date_form = datetime.strptime(search_date, '%Y-%m-%dT%H:%M')
            articles = articles.filter(date_publication__gte=search_date_form)
    except ValueError:
        search_date = None
    if search_date_debut and search_date_fin:
        try:
            form_search_date_fin = datetime.strptime(search_date_fin, '%Y-%m-%dT%H:%M')
            form_search_date_debut = datetime.strptime(search_date_debut, '%Y-%m-%dT%H:%M')
            if form_search_date_fin > form_search_date_debut:
                articles = articles.filter(date_publication__range=(form_search_date_debut, form_search_date_fin))
        except ValueError:
            pass
    if search_categorie:
        articles = articles.filter(categorie__icontains=search_categorie)

    # Initialiser les variables pour les statistiques
    mot_cle_count_titre = 0
    mot_cle_count_description = 0
    mot_cle_count_auteur = 0
    mot_cle_count_titre_page_accueil = 0

    if search_mot_cle:
        if index_mot == -1:
            mot_cle_in_titre = articles.filter(titre__icontains=search_mot_cle)
            mot_cle_in_description = articles.filter(description_article__icontains=search_mot_cle)
            mot_cle_in_auteur = articles.filter(nom_auteur__icontains=search_mot_cle)
            mot_cle_in_titre_page_accueil = articles.filter(titre_page_accueil__icontains=search_mot_cle)

            mot_cle_count_titre = mot_cle_in_titre.count()
            mot_cle_count_description = mot_cle_in_description.count()
            mot_cle_count_auteur = mot_cle_in_auteur.count()
            mot_cle_count_titre_page_accueil = mot_cle_in_titre_page_accueil.count()

            articles = mot_cle_in_titre | mot_cle_in_description | mot_cle_in_auteur | mot_cle_in_titre_page_accueil
            total_articles_count = articles.distinct().count()

            for article in articles:
                article.titre = highlight_keywords(article.titre, search_mot_cle)
                article.description_article = highlight_keywords(article.description_article, search_mot_cle)
                article.nom_auteur = highlight_keywords(article.nom_auteur, search_mot_cle)
                article.titre_page_accueil = highlight_keywords(article.titre_page_accueil, search_mot_cle)

        else:
            # Recherche avec deux parties de mot-clé
            if partie1_mot:
                mot_cle_1_in_titre = articles.filter(titre__icontains=partie1_mot)
                mot_cle_1_in_description = articles.filter(description_article__icontains=partie1_mot)
                mot_cle_1_in_auteur = articles.filter(nom_auteur__icontains=partie1_mot)
                mot_cle_1_in_titre_page_accueil = articles.filter(titre_page_accueil__icontains=partie1_mot)

                mot_cle_1_count_titre = mot_cle_1_in_titre.count()
                mot_cle_1_count_description = mot_cle_1_in_description.count()
                mot_cle_1_count_auteur = mot_cle_1_in_auteur.count()
                mot_cle_1_count_titre_page_accueil = mot_cle_1_in_titre_page_accueil.count()

                articles_1 = mot_cle_1_in_titre | mot_cle_1_in_description | mot_cle_1_in_auteur | mot_cle_1_in_titre_page_accueil
                total_articles_count_1 = articles_1.distinct().count()
            else:
                total_articles_count_1 = 0

            if partie2_mot:
                mot_cle_2_in_titre = articles.filter(titre__icontains=partie2_mot)
                mot_cle_2_in_description = articles.filter(description_article__icontains=partie2_mot)
                mot_cle_2_in_auteur = articles.filter(nom_auteur__icontains=partie2_mot)
                mot_cle_2_in_titre_page_accueil = articles.filter(titre_page_accueil__icontains=partie2_mot)

                mot_cle_2_count_titre = mot_cle_2_in_titre.count()
                mot_cle_2_count_description = mot_cle_2_in_description.count()
                mot_cle_2_count_auteur = mot_cle_2_in_auteur.count()
                mot_cle_2_count_titre_page_accueil = mot_cle_2_in_titre_page_accueil.count()

                articles_2 = mot_cle_2_in_titre | mot_cle_2_in_description | mot_cle_2_in_auteur | mot_cle_2_in_titre_page_accueil
                total_articles_count_2 = articles_2.distinct().count()
            else:
                total_articles_count_2 = 0

            # Combine results from both parts
            articles = articles_1 | articles_2
            total_articles_count = articles.distinct().count()

            for article in articles:
                if partie1_mot:
                    article.titre = highlight_keywords(article.titre, partie1_mot)
                    article.description_article = highlight_keywords(article.description_article, partie1_mot)
                    article.nom_auteur = highlight_keywords(article.nom_auteur, partie1_mot)
                    article.titre_page_accueil = highlight_keywords(article.titre_page_accueil, partie1_mot)
                if partie2_mot:
                    article.titre = highlight_keywords(article.titre, partie2_mot)
                    article.description_article = highlight_keywords(article.description_article, partie2_mot)
                    article.nom_auteur = highlight_keywords(article.nom_auteur, partie2_mot)
                    article.titre_page_accueil = highlight_keywords(article.titre_page_accueil, partie2_mot)
    else:
        total_articles_count = articles.distinct().count()


  
     # Pagination setup
    #paginator = Paginator(articles.distinct(), 3)  # Limite à 3 articles par page
    #page_number = request.GET.get('page')  # Obtient le numéro de la page actuelle
    #page_obj = paginator.get_page(page_number)  # Récupère la page actuelle des articles
    
    paginator = Paginator(articles, 3)  # Affiche 3 articles par page
    page_number = request.GET.get('page')  # Obtient le numéro de la page actuelle
    page_obj_pagination = paginator.get_page(page_number) 
    
    
    
    
    # Context setup
    context = {
        'articles_Statistiques_pagination': page_obj_pagination, 
        'articles_Statistiques_mot_cle': articles,
        'categories': categories,
        'total_articles_count': total_articles_count,
        'search_mot_cle': search_mot_cle,
        'mot_cle_count_titre': mot_cle_count_titre,
        'mot_cle_count_description': mot_cle_count_description,
        'mot_cle_count_auteur': mot_cle_count_auteur,
        'mot_cle_count_titre_page_accueil': mot_cle_count_titre_page_accueil,
        
    }

    if index_mot != -1:
        context.update({
            'mot_cle_1_count_titre': mot_cle_1_count_titre,
            'mot_cle_1_count_description': mot_cle_1_count_description,
            'mot_cle_1_count_auteur': mot_cle_1_count_auteur,
            'mot_cle_1_count_titre_page_accueil': mot_cle_1_count_titre_page_accueil,
            'total_articles_count_1': total_articles_count_1,
            'mot_cle_2_count_titre': mot_cle_2_count_titre,
            'mot_cle_2_count_description': mot_cle_2_count_description,
            'mot_cle_2_count_auteur': mot_cle_2_count_auteur,
            'mot_cle_2_count_titre_page_accueil': mot_cle_2_count_titre_page_accueil,
            'total_articles_count_2': total_articles_count_2,
            'partie1_mot': partie1_mot,
            'partie2_mot': partie2_mot,
            
        })

    # Ajouter les paramètres de recherche au contexte si fournis
    if any([search_site, search_order, search_date_debut, search_date_fin, search_categorie, search_mot_cle, search_date]):
        context.update({
            'search_site': search_site,
            'search_order': search_order,
            'search_date_debut': search_date_debut,
            'search_date_fin': search_date_fin,
            'search_categorie': search_categorie,
            'search_date': search_date,
            'search_mot_cle': search_mot_cle,
            'index_mot': index_mot,
        })

        

    return render(request, 'Statistiques_Recherche.html', context)

   
#return render(request, 'Statistiques_Recherche.html', context)
###############################""import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from django.shortcuts import render
from .models import Article
from datetime import datetime
from collections import defaultdict
import plotly.graph_objects as go

def extract_prefix(category_name):
    """
    Extrait un préfixe commun ou un groupe à partir du nom de la catégorie,
    en tenant compte des articles définis comme 'le', 'les', 'la'.
    """
    articles_definis = {'le', 'les', 'la', 'l', 'M', 'M le'}
    words = category_name.split()
    
    if words:
        if words[0].lower() in articles_definis and len(words) > 1:
            return ' '.join(words[:2])
        return words[0]
    return category_name

def normalize_category(category_name, prefix_map):
    """
    Normalise le nom de la catégorie en utilisant les préfixes définis dans prefix_map.
    """
    prefix = extract_prefix(category_name)
    return prefix_map.get(prefix, category_name)

def generate_chart_for_site(site_name, start_date=None):
    # Définir les préfixes d'URL pour chaque site
    url_prefixes = {
        'lefigaro': 'https://www.lefigaro.fr/',
        'lemonde': 'https://www.lemonde.fr',
        'libération': 'https://www.liberation.fr'
    }
    
    # Récupérer les données pour le site spécifique
    prefix = url_prefixes.get(site_name, '')
    filter_args = {'lien__startswith': prefix}
    
    if start_date:
        filter_args['date_publication__gte'] = start_date
    
    data = Article.objects.filter(**filter_args).values_list('categorie', flat=True)
    
    # Déterminer les préfixes communs
    category_counts = defaultdict(int)
    all_categories = set(data)
    prefix_map = {}
    
    for category in all_categories:
        if category and not category.lower().startswith('non trouvee'):
            prefix = extract_prefix(category)
            if prefix not in prefix_map:
                prefix_map[prefix] = prefix
    
    # Compter les occurrences de chaque catégorie après normalisation
    for category in data:
        if category and not category.lower().startswith('non trouvee'):
            normalized_category = normalize_category(category, prefix_map)
            category_counts[normalized_category] += 1

    categories = [cat for cat in category_counts.keys() if cat]
    values = [category_counts[cat] for cat in categories]

    # Génération des couleurs pour chaque catégorie
    color_scale = px.colors.qualitative.Plotly
    num_colors = len(categories)
    colors = color_scale[:num_colors]

    # Création du graphique en barres
    bar_fig = go.Figure(data=[go.Bar(x=categories, y=values, marker_color=colors)])
    bar_fig.update_layout(title=f'Statistiques pour {site_name} (Barres)',
                          xaxis_title='Catégories',
                          yaxis_title='Nombre d\'Articles',
                          showlegend=False)  # Ne pas afficher la légende externe

    # Création du graphique circulaire
    pie_fig = go.Figure(data=[go.Pie(labels=categories, values=values, textinfo='label+percent', hole=0.3, marker_colors=colors)])
    pie_fig.update_layout(title=f'Statistiques pour {site_name} (Circulaire)',
                          showlegend=False)  # Ne pas afficher la légende externe

    # Convertir les graphiques en HTML
    bar_plot_html = pio.to_html(bar_fig, full_html=False)
    pie_plot_html = pio.to_html(pie_fig, full_html=False)
    
    return bar_plot_html, pie_plot_html

def statistics_site(request):
    site = request.GET.get('site', '')
    start_date_str = request.GET.get('start_date', '')
    
    start_date = None
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            start_date = None
    
    sites = ['lefigaro', 'lemonde', 'libération']
    bar_plots = {}
    pie_plots = {}
    
    if site and site in sites:
        bar_plot, pie_plot = generate_chart_for_site(site, start_date)
        bar_plots[site] = bar_plot
        pie_plots[site] = pie_plot
    elif site == 'all':
        for site in sites:
            bar_plot, pie_plot = generate_chart_for_site(site, start_date)
            bar_plots[site] = bar_plot
            pie_plots[site] = pie_plot
    else:
        for site in sites:
            bar_plot, pie_plot = generate_chart_for_site(site, start_date)
            bar_plots[site] = bar_plot
            pie_plots[site] = pie_plot
    
    return render(request, 'statistiques.html', {'bar_plots': bar_plots, 'pie_plots': pie_plots})

#######################################################################
from django.shortcuts import render, get_object_or_404
from .models import Article
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime

def article_lifecycle_plot(request, article_title):
    article = get_object_or_404(Article, titre=article_title)
    
    # Récupérer tous les articles similaires par lien
    articles = Article.objects.filter(lien=article.lien).values('date_exportation', 'ordre_actualite')
    
    dates = []
    orders = []
    
    for a in articles:
        date_exportation = a.get('date_exportation')
        if date_exportation:
            # Vérifier si date_exportation est déjà un objet datetime
            if isinstance(date_exportation, datetime):
                dates.append(date_exportation)
            else:
                try:
                    # Convertir la chaîne en datetime si nécessaire
                    date_exportation = datetime.strptime(date_exportation, '%d-%m-%YT%H:%M:%S')
                    dates.append(date_exportation)
                except ValueError:
                    continue
            ordre_actualite = a.get('ordre_actualite')
            # Limiter les valeurs de ordre_actualite à 1, 2 et 3
            if ordre_actualite in [1, 2, 3]:
                orders.append(ordre_actualite)

    # Création du graphique de nuage de points avec lignes
    scatter_fig = go.Figure(data=[
        go.Scatter(x=dates, y=orders, mode='lines+markers', name='Articles')
    ])
    scatter_fig.update_layout(title=f'Cycle de Vie de l\'Article "{article_title}"',
                              xaxis_title='Date d\'Exportation',
                              yaxis_title='Ordre Actualité',
                              xaxis_rangeslider_visible=True)  # Afficher le slider pour la plage de dates
    
    # Convertir le graphique en HTML
    scatter_plot_html = pio.to_html(scatter_fig, full_html=False)
    
    return render(request, 'article_lifecycle_plot.html', {'scatter_plot_html': scatter_plot_html})




from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import base64
from .models import Article

def cycle_vie_article(request):
    # Étape 1 : Récupérer tous les articles
    articles = Article.objects.all()

    if not articles.exists():
        return render(request, 'cycle_vie_article.html', {'graphs': []})

    # Étape 2 : Groupement des articles par lien, titre, description, categories, auteur
    grouped_articles = {}
    for article in articles:
        key = (article.lien, article.titre, article.description_article, article.categorie, article.nom_auteur)
        if key not in grouped_articles:
            grouped_articles[key] = []
        grouped_articles[key].append(article)

    # Étape 3 : Générer les données pour le graphe pour chaque groupe d'articles
    graphs = []
    for key, articles in grouped_articles.items():
        # Trier les articles par date de publication puis par date d'exportation
        articles.sort(key=lambda x: (x.date_publication, x.date_exportation))
        
        dates = []
        ordres = []
        
        # Point A : date_publication de l'article le plus ancien
        dates.append(articles[0].date_publication)
        ordres.append(articles[0].ordre_actualite)
        
        # Points B : chaque date_exportation avec son ordre_actualite correspondant
        for article in articles[1:]:  # Ignorer le premier article déjà utilisé pour Point A
            if article.ordre_actualite in [1, 2, 3]:  # Filtrer pour n'avoir que les valeurs 1, 2, ou 3
                dates.append(article.date_exportation)
                ordres.append(article.ordre_actualite)
        
        # Tracer le graphe
        plt.figure(figsize=(10, 6))
        plt.plot(dates, ordres, marker='o', linestyle='-', color='b')
        plt.title(f"Cycle de vie de l'article: {key[1]}")
        plt.xlabel('Date')
        plt.ylabel("Ordre d'Actualité")
        plt.yticks([1, 2, 3])  # Limiter les ticks de l'axe Y à 1, 2, 3
        plt.grid(True)
        
        # Sauvegarder le graphe dans un buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        # Encoder l'image en base64 pour l'afficher dans un template
        graphic = base64.b64encode(image_png).decode('utf-8')

        # Ajouter le graphique au contexte pour l'affichage
        graphs.append({
            'graphic': graphic,
            'titre': key[1],
            'lien': key[0],
            'description': key[2],
            'categories': key[3],
            'auteur': key[4],
        })

    # Rendre le template avec les graphiques
    context = {
        'graphs': graphs,
    }
    return render(request, 'cycle_vie_article.html', context)

# compte les articles doublons(qu'elles ont le meme titre ect mais differentes valeures de order actualite apres il trace le graphe pour le cycle de vie d'article)


def compter_doublons_articles(request, article_id):
    from django.shortcuts import render, get_object_or_404
    from django.db.models import Count
    from .models import Article
    import json
    from django.utils.timezone import make_naive
    article = get_object_or_404(Article, pk=article_id)
    articles_grouped = Article.objects.filter(
        lien=article.lien,
        titre=article.titre,
        description_article=article.description_article,
        categorie=article.categorie,
        nom_auteur=article.nom_auteur
    ).values(
        'lien',
        'titre',
        'description_article',
        'categorie',
        'nom_auteur'
    ).annotate(nombre_doublons=Count('id')).order_by('-nombre_doublons')

    graphs_data = []

    for group in articles_grouped:
        articles = Article.objects.filter(
            lien=group['lien'],
            titre=group['titre'],
            description_article=group['description_article'],
            categorie=group['categorie'],
            nom_auteur=group['nom_auteur']
        ).order_by('date_exportation')

        if articles.exists():
            dates = []
            ordres = []

            date_publication = make_naive(articles[0].date_publication)
            dates.append(date_publication.strftime('%d-%m-%Y %H:%M:%S'))
            ordres.append(articles[0].ordre_actualite)

            for article in articles:
                if article.ordre_actualite in [1, 2, 3]:
                    date_exportation = make_naive(article.date_exportation)
                    dates.append(date_exportation.strftime('%d-%m-%Y %H:%M:%S'))
                    ordres.append(article.ordre_actualite)

            if dates and ordres:
                graphs_data.append({
                    'dates': dates,
                    'ordres': ordres,
                    'titre': group['titre'],
                })

    context = {
        'graphs_data': json.dumps(graphs_data),
    }

    return render(request, 'compter_doublons_articles.html', context)



from .models import Article

def get_articles_from_request(request):
    """
    Fonction pour récupérer les articles en fonction des paramètres de la requête.
    Adaptez cette fonction selon la manière dont vous filtrez les articles dans votre application.
    """
    # Exemple simple de filtrage selon des paramètres de requête
    # (remplacez ceci par la logique appropriée pour votre application)
    queryset = Article.objects.all()

    # Filtrer par date si fourni
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    if date_debut and date_fin:
        queryset = queryset.filter(date_publication__range=[date_debut, date_fin])

    # Filtrer par catégorie si fourni
    categorie = request.GET.get('categorie')
    if categorie:
        queryset = queryset.filter(categorie=categorie)

    # Vous pouvez ajouter d'autres filtres en fonction des paramètres de la requête ici

    return queryset



from django.http import HttpResponse
import openpyxl
from io import BytesIO

def download_articles_excel(request):
    # Créer un classeur Excel et une feuille
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Articles'

    # En-têtes de colonnes
    headers = ['Id', 'Titre page d\'accueil', 'Titre', 'Lien', 'Date Publication', 'Nom Auteur', 'Description Article', 'Statut Image', 'Actualité', 'Date Exportation', 'Catégorie', 'Ordre d\'Actualité']
    sheet.append(headers)

    # Récupérer les articles de la requête
    articles = get_articles_from_request(request)  # Implémentez cette fonction selon vos besoins

    for article in articles:
        sheet.append([
            article.id,
            article.titre_page_accueil,
            article.titre,
            article.lien,
            article.date_publication,
            article.nom_auteur,
            article.description_article,
            article.statut_image,
            article.actualite,
            article.date_exportation,
            article.categorie,
            article.ordre_actualite
        ])

    # Utiliser BytesIO pour écrire le contenu du fichier Excel
    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    # Créer une réponse HTTP avec le contenu du fichier Excel
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="articles.xlsx"'
    return response

import pandas as pd
from django.http import HttpResponse
from .models import Article

def telecharger_articles_excel(request):
    # Récupérer tous les articles depuis la base de données
    articles = Article.objects.all()

    # Créer une liste des données à exporter
    data = []
    for article in articles:
        # Si article.date_publication est timezone-aware, on enlève le fuseau horaire
        date_publication = article.date_publication
        date_exportation = article.date_exportation

        if date_publication and date_publication.tzinfo is not None:
            date_publication = date_publication.replace(tzinfo=None)
        if date_exportation and date_exportation.tzinfo is not None:
            date_exportation = date_exportation.replace(tzinfo=None)

        # Ajouter les données de chaque article dans la liste
        data.append({
            'Id': article.id,
            'Titre Accueil': article.titre_page_accueil,
            'Titre': article.titre,
            'Lien': article.lien,
            'Date Publication': date_publication,  # Utiliser la date sans fuseau horaire
            'Auteur': article.nom_auteur,
            'Description': article.description_article,
            'Statut Image': article.statut_image,
            'Statut Actualite': article.actualite,
            'Date Exportation': date_exportation,  # Utiliser la date sans fuseau horaire
            'Categorie': article.categorie,
            'Ordre Actualite': article.ordre_actualite,
        })

    # Convertir les données en DataFrame pandas
    df = pd.DataFrame(data)

    # Créer une réponse HTTP avec un fichier Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=articles.xlsx'

    # Utiliser pandas pour exporter le DataFrame vers un fichier Excel
    df.to_excel(response, index=False, engine='openpyxl')

    return response



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
def gestion_utilisateurs(request):
    utilisateurs = User.objects.all()
    return render(request, 'gestion_utilisateurs.html', {'utilisateurs': utilisateurs})

@login_required
def modifier_utilisateur(request, user_id):
    utilisateur = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        utilisateur.username = request.POST['username']
        utilisateur.email = request.POST['email']
        password = request.POST['password']
        if password:
            utilisateur.set_password(password)
        utilisateur.save()
        return redirect('gestion_utilisateurs')
    return render(request, 'modifier_utilisateur.html', {'utilisateur': utilisateur})

@require_POST
@login_required
def bloquer_utilisateur(request, user_id):
    utilisateur = get_object_or_404(User, id=user_id)
    utilisateur.is_active = False
    utilisateur.save()
    return redirect('gestion_utilisateurs')





##############################

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


def ajouter_utilisateur(request):
    return render(request, 'ajouter_utilisateur.html')

def enregistrer_utilisateur(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Créer un nouvel utilisateur
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Utilisateur ajouté avec succès.')
        return redirect('gestion_utilisateurs')




from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def supprimer_utilisateur(request, utilisateur_id):
    utilisateur = get_object_or_404(User, id=utilisateur_id)
    if request.method == 'POST':
        utilisateur.delete()
        messages.success(request, "L'utilisateur a été supprimé avec succès.")
        return redirect('gestion_utilisateurs')  # Redirection vers la liste des utilisateurs
    return redirect('gestion_utilisateurs')  # Redirection si la méthode n'est pas POST
