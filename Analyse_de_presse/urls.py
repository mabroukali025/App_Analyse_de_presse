"""
URL configuration for Analyse_de_presse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import admin
from django.urls import path
from AppScraping import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('page_Acceuil',views.page_Acceuil),
    path('login/', views.custom_login, name='login'),
    path('register/', views.register, name='register'),
    
    
    # urls.py

    path('gestion_utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('modifier_utilisateur/<int:user_id>/', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('bloquer_utilisateur/<int:user_id>/', views.bloquer_utilisateur, name='bloquer_utilisateur'),
    
    

    
    path('utilisateurs/ajouter/', views.ajouter_utilisateur, name='ajouter_utilisateur'),
    path('utilisateurs/enregistrer/', views.enregistrer_utilisateur, name='enregistrer_utilisateur'),
    path('utilisateurs/supprimer/<int:utilisateur_id>/',views.supprimer_utilisateur, name='supprimer_utilisateur'),


    path('', views.home, name='home_page'), 
    path('home/', views.page_Acceuil, name='page_Acceuil'),
    path('login/scraping/', views.scraping_page, name='scraping_page'),
    path('gestion-donnee/', views.gestion_donnee_page, name='gestion_donnee_page'),
    path('statistiques/', views.statistiques_page, name='statistiques_page'),
    path('find_articles/',views.find_articles, name='find_articles'),
    #path('find_article_from_Data/', views.find_article_from_Data, name='find_article_from_Data'),
    path('articles/', views.article_list, name='article_list'),
    path('remove-duplicates/', views.remove_duplicate_articles, name='remove_duplicate_articles'),
    path('statistiques_page/',views.statistiques_page,name="statistiques_page"),
    path('article-statistics/',views.article_statistics, name='article_statistics'),
    path('arreter_scraping/', views.arreter_scraping_view, name='arreter_scraping_view'),
    path('statistics_site_categorie/', views.statistics_site_categorie, name='statistics_site_categorie'),
    path('Statistiques_Recherche/',views.Statistiques_Recherche, name='Statistiques_Recherche'),
    path('Statistiques_mot_cle/', views.Statistiques_mot_cle,name='Statistiques_mot_cle'),
    path('statistics_site/',views.statistics_site,name='statistics_site'),
    #path('global_statistics/',views.global_statistics,name='global_statistics')
    path('cycle_vie_article/', views.cycle_vie_article, name='cycle_vie_article'),
    path('compter_doublons_articles/<int:article_id>/', views.compter_doublons_articles, name='compter_doublons_articles'),
    path('get_scraping_status/', views.get_scraping_status, name='get_scraping_status'),
    path('download_articles_excel/', views.download_articles_excel, name='download_articles_excel'),
    path('telecharger-excel/', views.telecharger_articles_excel, name='telecharger_excel'),
    path('telecharger-article/<int:article_id>/', views.telecharger_article_unique_excel, name='telecharger_article_unique_excel'),

    path('plot/', views.plot_motcle_counts, name='plot_motcle_counts'),



    
    
]

