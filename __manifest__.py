# -*- coding: utf-8 -*-
{
    'name': 'Gestion Scolaire',
    'version': '18.0.1.0.0',
    'category': 'Education',
    'summary': 'Module de gestion scolaire complète: étudiants, notes, emplois du temps, présence et rapports',
    'description': """
        Gestion Scolaire Complète
        ==========================
        
        Ce module offre une solution complète pour la gestion d'établissements scolaires:
        
        Fonctionnalités principales:
        * Gestion des étudiants avec informations personnelles
        * Gestion des cours et matières
        * Gestion des notes et évaluations
        * Gestion des emplois du temps
        * Suivi de la présence
        * Génération de rapports et bulletins
        * Gestion des classes et niveaux
        * Gestion des enseignants
    """,
    'author': 'Sawssan',
    'website': 'https://www.example.com',
    'depends': ['base', 'mail', 'web'],
    'data': [
        # Sécurité
        'security/school_security.xml',
        'security/ir.model.access.csv',
        
        # Données
        'data/sequence_data.xml',
        
        # Vues
        'views/student_views.xml',
        'views/course_views.xml',
        'views/class_views.xml',
        'views/grade_views.xml',
        'views/schedule_views.xml',
        'views/attendance_views.xml',
        'views/teacher_views.xml',
        'views/menu_views.xml',
        
        # Rapports
        'reports/report_template.xml',
        'reports/student_report.xml',
        'reports/bulletin_report.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
