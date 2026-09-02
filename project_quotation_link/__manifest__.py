# -*- coding: utf-8 -*-
{
    'name': 'Project - Quotation Link',
    'version': '18.0.1.0.0',
    'summary': 'Link sales quotations to specific projects',
    'description': """
This module allows you to associate sales quotations with a specific project.

Main features:
- Link a quotation directly to a project
- Manage multiple projects per customer with their own quotations
- Improve traceability and project-based quotation management

Ideal for companies managing several projects for the same client.
    """,
    'category': 'Projects',
    'author': 'Jeremie Ndjoli',
    'website': 'https://www.linkedin.com/in/jeremie-ndjoli-39a550255/',
    'depends': [
        'project',
        'sale_project',
    ],
    'data': [
        'views/sale_order.xml',
        'views/project_view.xml',
    ],
    

    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/01_creation_projet.png',
        'static/description/02_projet_avec_devis.png',
        'static/description/03_vue_kanban.png',
        'static/description/04_devis_avec_projet.png',
    ],

    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}


