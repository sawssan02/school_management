# Module de Gestion Scolaire pour Odoo 18

## Description

Ce module offre une solution complète pour la gestion d'établissements scolaires avec Odoo 18. Il permet de gérer tous les aspects de la vie scolaire : étudiants, enseignants, cours, notes, emplois du temps, présence et génération de rapports.

## Fonctionnalités principales

### 1. Gestion des Étudiants
- Création et gestion de fiches étudiants complètes
- Informations personnelles (nom, date de naissance, contact, etc.)
- Informations académiques (classe, matricule, statut)
- Informations du tuteur/parent
- Suivi des notes et de la présence
- Calcul automatique de la moyenne générale
- Génération de fiches étudiants et bulletins de notes

### 2. Gestion des Enseignants
- Profils complets des enseignants
- Informations professionnelles
- Suivi des cours enseignés
- Emploi du temps personnalisé

### 3. Gestion des Classes
- Organisation par niveaux et sections
- Affectation d'un enseignant principal
- Capacité maximale et salle de classe
- Statistiques de la classe (nombre d'étudiants, moyenne)
- Liste des étudiants et cours associés

### 4. Gestion des Cours
- Création de cours avec code unique
- Affectation enseignant et classe
- Gestion des crédits et heures
- Suivi des notes du cours
- Calcul de la moyenne du cours

### 5. Système de Notes
- Différents types d'évaluations (devoirs, interrogations, examens, projets)
- Notes par semestre
- Calcul automatique des pourcentages
- Attribution automatique de lettres (A+, A, B+, etc.)
- Vues analytiques (pivot, graphique)
- Validation des notes

### 6. Emploi du Temps
- Planning hebdomadaire complet
- Affectation par jour et horaire
- Types de sessions (cours magistral, TD, TP, examen)
- Détection automatique des conflits d'horaire
- Vues calendrier et Gantt
- Génération de rapports d'emploi du temps

### 7. Gestion de la Présence
- Marquage quotidien de la présence
- Statuts : Présent, Absent, En retard, Absent justifié
- Enregistrement des heures d'arrivée et de départ
- Calcul automatique du taux de présence
- Vues analytiques et rapports
- Marquage en masse possible

### 8. Rapports
- Fiche étudiant détaillée
- Bulletin de notes avec moyennes par semestre et par cours
- Rapport de présence
- Emploi du temps de classe
- Tous les rapports sont exportables en PDF

## Installation

### Prérequis
- Odoo 18
- Python 3.8+
- PostgreSQL 12+

### Étapes d'installation

1. Copiez le dossier `school_management` dans le répertoire addons de votre installation Odoo:
   ```bash
   cp -r school_management /path/to/odoo/addons/
   ```

2. Redémarrez le serveur Odoo:
   ```bash
   sudo systemctl restart odoo
   # ou
   python3 odoo-bin -c /path/to/odoo.conf
   ```

3. Activez le mode développeur dans Odoo:
   - Allez dans Paramètres → Activer le mode développeur

4. Mettez à jour la liste des applications:
   - Allez dans Applications → Mettre à jour la liste des applications

5. Recherchez "Gestion Scolaire" dans les applications et cliquez sur "Installer"

## Configuration initiale

### 1. Créer les utilisateurs et groupes

Le module crée automatiquement 4 groupes d'accès:
- **Utilisateur**: Lecture seule
- **Enseignant**: Peut gérer les notes et la présence
- **Gestionnaire**: Peut gérer les étudiants, classes et cours
- **Administrateur**: Accès complet

Affectez les utilisateurs aux groupes appropriés dans Paramètres → Utilisateurs

### 2. Créer les classes

1. Allez dans Gestion Scolaire → Académique → Classes
2. Créez vos classes avec:
   - Nom et code unique
   - Niveau (1 à 6)
   - Section
   - Capacité
   - Numéro de salle
   - Enseignant principal

### 3. Créer les enseignants

1. Allez dans Gestion Scolaire → Enseignants → Tous les enseignants
2. Ajoutez les enseignants avec leurs informations complètes

### 4. Créer les cours

1. Allez dans Gestion Scolaire → Académique → Cours
2. Créez les cours en associant:
   - Un enseignant
   - Une classe
   - Les crédits et heures

### 5. Créer l'emploi du temps

1. Allez dans Gestion Scolaire → Académique → Emploi du temps
2. Créez les horaires hebdomadaires
3. Le système vérifie automatiquement les conflits

### 6. Ajouter les étudiants

1. Allez dans Gestion Scolaire → Étudiants → Tous les étudiants
2. Créez les fiches étudiants avec:
   - Informations personnelles
   - Contact
   - Classe
   - Informations du tuteur

## Utilisation quotidienne

### Marquer la présence

1. Allez dans Gestion Scolaire → Présence → Présence journalière
2. Créez des enregistrements de présence pour chaque étudiant
3. Sélectionnez le statut approprié
4. Le taux de présence est calculé automatiquement

### Saisir les notes

1. Allez dans Gestion Scolaire → Notes → Toutes les notes
2. Créez une nouvelle note en sélectionnant:
   - L'étudiant
   - Le cours
   - Le type d'évaluation
   - Le semestre
   - La note sur le maximum
3. Le pourcentage et la lettre sont calculés automatiquement

### Générer les bulletins

1. Ouvrez la fiche d'un étudiant
2. Cliquez sur "Imprimer" → "Bulletin de Notes"
3. Le PDF est généré avec:
   - Notes par semestre
   - Moyennes par cours
   - Moyenne générale
   - Appréciation

### Consulter l'emploi du temps

1. Allez dans Gestion Scolaire → Académique → Emploi du temps
2. Utilisez les vues:
   - Arbre: Vue liste
   - Calendrier: Vue hebdomadaire
   - Gantt: Vue planning
3. Filtrez par classe, enseignant ou cours

## Structure du module

```
school_management/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── student.py          # Modèle étudiant
│   ├── teacher.py          # Modèle enseignant
│   ├── class_level.py      # Modèle classe
│   ├── course.py           # Modèle cours
│   ├── grade.py            # Modèle notes
│   ├── schedule.py         # Modèle emploi du temps
│   └── attendance.py       # Modèle présence
├── views/
│   ├── student_views.xml
│   ├── teacher_views.xml
│   ├── class_views.xml
│   ├── course_views.xml
│   ├── grade_views.xml
│   ├── schedule_views.xml
│   ├── attendance_views.xml
│   └── menu_views.xml
├── security/
│   ├── school_security.xml
│   └── ir.model.access.csv
├── data/
│   └── sequence_data.xml
├── reports/
│   ├── __init__.py
│   ├── report_template.xml
│   ├── student_report.xml
│   └── bulletin_report.xml
└── static/
    └── description/
        ├── icon.png
        └── banner.png
```


---
