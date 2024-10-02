from django.db import models

from django.db import models
from datetime import date, time

class Article(models.Model):
    """
    Modèle pour représenter un article
    """
    id = models.AutoField(primary_key=True)
    titre_page_accueil = models.CharField(max_length=255, default='Titre par défaut')
    titre = models.CharField(max_length=255, default='Titre par défaut')
    lien = models.CharField(max_length=500, default='https://exemple.com')
    date_publication =models.DateTimeField(verbose_name="Date d'exportation", help_text="Date au format jour mois année, heure:minute:seconde")
    nom_auteur = models.CharField(max_length=255, default='Auteur inconnu')
    description_article = models.TextField(default='Description par défaut')
    statut_image = models.CharField(max_length=255)
    actualite = models.CharField(max_length=255)
    date_exportation = models.DateTimeField(verbose_name="Date d'exportation", help_text="Date au format jour mois année, heure:minute:seconde")
    categorie = models.CharField(max_length=255, default='Catégorie par défaut')
    ordre_actualite = models.IntegerField(blank=True, null=True)

    # Champ id auto-incrémenté (pas besoin de le définir dans le constructeur)
    

    def __str__(self):
        return self.titre

    class Meta:
        db_table = 'articles'
        verbose_name='Article'
        verbose_name_plural='Article'



class ScrapingStatus(models.Model):
    is_scraping = models.BooleanField(default=False)

    @classmethod
    def get_status(cls):
        return cls.objects.first()  # Retourne le premier enregistrement (ou ajustez selon votre logique)


from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)  # Champ pour distinguer les administrateurs des utilisateurs

    def __str__(self):
        return self.user.username



