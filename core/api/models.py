from django.db import models
# Importe les classes de base pour la gestion des utilisateurs Django
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserProfileManager(BaseUserManager):
    """Gestionnaire personnalisé pour le modèle UserProfile"""
    def create_user(self, email, name, password=None):
        """
        Crée et sauvegarde un nouvel utilisateur
        Args:
            email: Email de l'utilisateur (obligatoire)
            name: Nom de l'utilisateur (obligatoire)
            password: Mot de passe de l'utilisateur (optionnel)
        Raises:
            ValueError: Si l'email n'est pas fourni
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email) # Normalise l'adresse email
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        """
        Crée et sauvegarde un superutilisateur avec les droits d'administration
        Args:
            email: Email du superutilisateur (obligatoire)
            password: Mot de passe du superutilisateur (obligatoire)
        Raises:
            ValueError: Si l'email ou le mot de passe n'est pas fourni
                    """
        if not email:
            raise ValueError('Superusers must have an email address')
        if not password:
            raise ValueError('Superusers must have a password')
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Modèle personnalisé pour les utilisateurs
    Hérite de AbstractBaseUser pour la gestion de l'authentification
    et PermissionsMixin pour la gestion des permissions
    """
    # Champs personnalisés du modèle
    email = models.EmailField(max_length=255, unique=True)  # Email unique comme identifiant
    name = models.CharField(max_length=255)  # Nom de l'utilisateur
    is_active = models.BooleanField(default=True)  # Indique si le compte est actif
    is_staff = models.BooleanField(default=False)  # Indique si l'utilisateur est staff

    # Associe le gestionnaire personnalisé
    objects = UserProfileManager() # Gestionnaire de base de données pour les utilisateurs

    # Configure l'email comme champ d'identification
    USERNAME_FIELD = 'email'
    # Définit les champs requis à la création
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name
    
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name
    
    def __str__(self):
        """Return string representation of user"""
        return self.email
