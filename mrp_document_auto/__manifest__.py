# -*- coding: utf-8 -*-
{
    'name': "MRP - Auto Copy Documents",
    'summary': "Automatically copies documents from components to the finished product (BoM)",
    
    'description': """
 **Key features**
----------------------------------
- Automatically copies all documents and attachments related to components (products or variants) to the final product associated with the bill of materials (BoM).
- Avoids duplicates by checking the file name and checksum.
- Updates documents in real time when components change.
- Marks deleted documents as `[OBSOLETE]` to preserve history.
- Two-way synchronization between product documents and bill of materials documents.

**Use cases**
------------------------
- Management of technical drawings (PDF, images, DXF, etc.).
- Centralization of technical data sheets and certifications at the finished product level.
- Complete document tracking throughout the manufacturing process.

**Advantages**
----------------
- Time savings: no more need to copy documents manually.
- Fewer errors: all documents are always up to date and in the right place.
- Transparency: complete traceability of documents inherited from components.

""",

    'author': "Jeremie Ndjoli",
    'website': "https://github.com/Jeremie2001/odoo17-modules",

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
        'static/description/add_manufacturing.png',
        'static/description/component_doc.png',
        'static/description/component_with_doc.png',
        'static/description/finished_prod_doc.png',
        'static/description/finished_prod_with_doc.png',
        'static/description/finished_product_without_doc.png',
        'static/description/obsolete_component.png',


    ],


    'installable': True,
    'application': False,
    'auto_install': False,  
    'license': 'LGPL-3',
}