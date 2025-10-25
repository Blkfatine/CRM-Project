# 🚀 CRM Project - WebRasma & Digital Ranking

Un système de gestion de la relation client (CRM) complet et moderne développé avec Django, conçu pour simplifier la gestion des leads, rendez-vous, et communications.

## 📋 Table des Matières
- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Structure du Projet](#structure-du-projet)
- [Installation](#installation)
- [Guide d'Utilisation](#guide-dutilisation)
- [Technologies Utilisées](#technologies-utilisées)

---

## 🎯 Aperçu

Ce CRM permet aux équipes commerciales de gérer efficacement leurs leads, suivre les interactions clients, planifier des rendez-vous et communiquer en temps réel. Le système comprend un tableau de bord administrateur complet avec des statistiques en temps réel.

---

## ✨ Fonctionnalités

### 🔐 Authentification
- **Page de connexion/inscription** : Interface moderne avec animation de bascule entre login et signup
- **Gestion des sessions** : Système sécurisé avec protection CSRF
- **Rôles utilisateurs** : Distinction entre administrateurs et utilisateurs normaux

### 👤 Pour les Utilisateurs

#### 📊 **Tableau de Bord (Lead List)**
Votre page d'accueil après connexion. Vous y trouvez :
- Vue d'ensemble des leads récents (4 derniers)
- Statistiques rapides : leads pris en charge, non pris en charge, non contactés
- Rendez-vous à venir (3 prochains)
- Graphique des leads générés par mois
- Annonces importantes de l'équipe
- Notifications en temps réel

#### 📋 **Liste des Leads (Lead Actions)**
Page complète pour gérer tous vos leads :
- Filtres par statut (nouveau, contacté, perdu)
- Ajout de nouveaux leads
- Modification et suppression de leads
- Import de leads par fichier CSV
- Attribution de leads à des utilisateurs
- Graphique des performances mensuelles

#### 👥 **Détail du Lead**
Page détaillée pour chaque lead :
- Informations complètes (nom, email, téléphone, source)
- Historique des interactions
- Enregistrement d'appels avec durée et notes
- Envoi d'emails directs
- Historique complet des communications

#### 📅 **Rendez-vous (Appointments)**
Gestion de vos rendez-vous :
- Liste de tous les rendez-vous
- Création de nouveaux rendez-vous
- Association avec des leads
- Statut (planifié, confirmé, terminé, annulé)

#### 💬 **Discussions (Conversations)**
Système de messagerie interne :
- Conversations individuelles ou de groupe
- Envoi de messages texte et fichiers
- Indicateur de messages non lus
- Historique complet des échanges

#### 📢 **Annonces**
Consultez les annonces de l'équipe :
- Annonces importantes de l'administration
- Mises à jour du système
- Notifications sur les nouvelles annonces

### 🔧 Pour les Administrateurs

#### 🎛️ **Tableau de Bord Admin**
Vue complète de l'activité :
- Statistiques globales (nombre de leads, rendez-vous, taux de conversion)
- Graphiques de performance par utilisateur
- Leads récents avec détails
- Sources des leads
- Performances de conversion par utilisateur
- **Ajout rapide d'utilisateurs** directement depuis le dashboard

#### 👥 **Gestion des Utilisateurs**
Page dédiée à la gestion de l'équipe :
- Liste de tous les utilisateurs
- Modification des informations utilisateur
- Changement de mots de passe
- Suppression d'utilisateurs
- Attribution de permissions

#### 📣 **Gestion des Annonces**
Créez et gérez les communications :
- Création de nouvelles annonces
- Modification d'annonces existantes
- Suppression d'annonces
- Notifications automatiques à tous les utilisateurs

---

## 📁 Structure du Projet

```
crm_project/
├── users/              # Gestion des utilisateurs et authentification
│   ├── views.py       # Login, signup, admin dashboard, gestion utilisateurs
│   ├── forms.py       # Formulaires d'inscription et annonces
│   └── models.py      # Modèle Announcement
│
├── leads/              # Gestion des leads
│   ├── views.py       # CRUD leads, interactions, emails, appels
│   ├── models.py      # Lead, Interaction, EmailHistory
│   ├── forms.py       # Formulaires de leads et interactions
│   └── templates/     # Templates HTML pour les leads
│       ├── lead_list.html         # Tableau de bord principal
│       ├── lead_actions.html      # Liste complète des leads
│       ├── lead_detail.html       # Détail d'un lead
│       ├── lead_form.html         # Ajout/modification de lead
│       ├── lead_import.html       # Import CSV
│       ├── lead_interactions.html # Interactions avec le lead
│       ├── historique_appels.html # Historique des appels
│       ├── historique_emails.html # Historique des emails
│       └── BoiteGmail.html        # Envoi d'emails
│
├── appointments/       # Gestion des rendez-vous
│   ├── views.py       # CRUD rendez-vous
│   ├── models.py      # Appointment
│   └── forms.py       # Formulaire de rendez-vous
│
├── conversations/      # Système de messagerie
│   ├── views.py       # Gestion des conversations et messages
│   ├── models.py      # Conversation, Message, ConversationParticipant
│   └── templates/     # Templates de messagerie
│
├── notifications/      # Système de notifications
│   ├── views.py       # Notifications, compteur non lues
│   ├── models.py      # Notification
│   └── urls.py        # Routes notifications
│
├── templates/          # Templates globaux
│   ├── login.html                  # Page de connexion/inscription
│   ├── admin_dashboard.html        # Dashboard administrateur
│   ├── announcements_list.html     # Liste des annonces
│   ├── create_announcement.html    # Création d'annonce
│   ├── edit_announcement.html      # Modification d'annonce
│   ├── user_management.html        # Gestion utilisateurs
│   ├── edit_user.html             # Modification utilisateur
│   └── change_user_password.html  # Changement de mot de passe
│
├── static/             # Fichiers statiques (CSS, JS, images)
├── media/              # Fichiers uploadés (CV, documents)
├── db.sqlite3          # Base de données
└── manage.py           # Script Django
```

---

## 🛠️ Installation

### Prérequis
- Python 3.8+
- pip
- Git

### Étapes

1. **Cloner le dépôt**
```bash
git clone https://github.com/Blkfatine/CRM-Project.git
cd CRM-Project
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer un super utilisateur**
```bash
python manage.py createsuperuser
```

6. **Lancer le serveur**
```bash
python manage.py runserver
```

7. **Accéder à l'application**
- Application : http://127.0.0.1:8000
- Admin Django : http://127.0.0.1:8000/admin

---

## 📖 Guide d'Utilisation

### Premier Lancement

1. **Créez votre compte** via la page d'inscription (bouton "S'inscrire")
2. **Connectez-vous** avec vos identifiants
3. **Explorez le tableau de bord** pour voir vos leads et rendez-vous
4. **Ajoutez votre premier lead** depuis "Liste des leads" → "Ajouter un lead"

### Workflow Recommandé

1. **Import de leads** : Importez vos contacts via CSV
2. **Attribution** : L'admin attribue les leads aux commerciaux
3. **Suivi** : Enregistrez vos interactions (appels, emails)
4. **Rendez-vous** : Planifiez des rendez-vous avec les prospects
5. **Conversion** : Changez le statut quand le lead devient client

### Rôles et Permissions

- **Administrateur** :
  - Accès au dashboard admin
  - Gestion des utilisateurs
  - Création d'annonces
  - Vue globale des statistiques

- **Utilisateur** :
  - Gestion de ses leads attribués
  - Création de rendez-vous
  - Messagerie interne
  - Consultation des annonces

---

## 🔧 Technologies Utilisées

### Backend
- **Django 5.0.7** - Framework web Python
- **SQLite** - Base de données
- **Django ORM** - Gestion des données

### Frontend
- **HTML5/CSS3** - Structure et style
- **JavaScript** - Interactivité
- **Ion Icons** - Icônes
- **Chart.js** - Graphiques (implicite dans les statistiques)

### Fonctionnalités
- **Authentication Django** - Système de connexion sécurisé
- **CSRF Protection** - Sécurité des formulaires
- **Messages Framework** - Notifications utilisateur
- **File Upload** - Gestion des fichiers

---

## 🔐 Sécurité

- Protection CSRF sur tous les formulaires
- Authentification obligatoire pour les pages sensibles
- Séparation des rôles admin/utilisateur
- Sessions sécurisées
- Validation des formulaires côté serveur

---

## 📝 Notes

### Compte Admin par Défaut
```
Username: admin
Password: admin123
```
**⚠️ Changez ce mot de passe après la première connexion !**

### URLs Principales
- `/` - Page de connexion
- `/login/` - Connexion
- `/signup/` - Inscription
- `/leads/` - Tableau de bord utilisateur
- `/admin-dashboard/` - Dashboard administrateur
- `/appointments/` - Liste des rendez-vous
- `/conversations/` - Messagerie
- `/announcements_list/` - Annonces

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou un pull request.

---

## 📄 Licence

Ce projet est sous licence MIT.

---

## 👨‍💻 Auteur

**WebRasma & Digital Ranking Team**

Pour toute question, contactez-nous !

---

## 🎯 Fonctionnalités à Venir

- [ ] Export des leads en PDF/Excel
- [ ] Notifications push en temps réel
- [ ] Intégration email (Gmail, Outlook)
- [ ] API REST pour intégrations externes
- [ ] Application mobile
- [ ] Tableau de bord analytics avancé

---

**Merci d'utiliser notre CRM ! 🚀**
