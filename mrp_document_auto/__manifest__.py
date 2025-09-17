# -*- coding: utf-8 -*-
{
    'name': "MRP - Auto Copy Documents",
    'summary': "Copie automatique des documents des composants vers le produit fini (BoM)",
    
    'description': """
 **Fonctionnalités principales**
----------------------------------
- Copie automatiquement tous les documents et pièces jointes liés aux composants (produits ou variantes) vers le produit final associé à la nomenclature (BoM).
- Évite les doublons grâce à un contrôle sur le nom et le checksum du fichier.
- Met à jour les documents en temps réel lorsque les composants changent.
- Marque les documents supprimés comme `[LEGACY]` pour conserver l'historique.
- Synchronisation bidirectionnelle entre les documents des produits et ceux de la nomenclature.

**Cas d'utilisation**
------------------------
- Gestion des plans techniques (PDF, images, DXF…).
- Centralisation des fiches techniques et certifications au niveau du produit fini.
- Suivi documentaire complet dans le processus de fabrication.

**Avantages**
----------------
- Gain de temps : plus besoin de copier les documents manuellement.
- Moins d'erreurs : tous les documents sont toujours à jour au bon endroit.
- Transparence : traçabilité complète des documents hérités des composants.

""",

    'author': "Jeremie Ndjoli",
    'website': "https://www.linkedin.com/in/jeremie-ndjoli-39a550255/",

    'category': 'Manufacturing',
    'version': '18.0.1.0.0',  

    'depends': ['mrp', 'base'],

    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],

    'images': [
        'static/description/icon.png',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,  # AJOUTÉ : Explicitement défini
    'license': 'LGPL-3',
}