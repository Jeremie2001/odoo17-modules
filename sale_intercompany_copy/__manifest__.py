{
    'name': 'Sale Order — Copy to Another Company',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Copy sale orders from one company to another in one click',
    'description': """
Sale Order — Copy to Another Company
=====================================

Stop re-entering quotations manually across your Odoo companies.

This module adds a Copy to Another Company action on every sale order.
Select the target company, click Copy Order — done.

Key Features
------------
- Copy any sale order to another company in one click
- Bulk copy from the list view
- Full traceability in the chatter with a direct link to the copied order
- Automatic tax reassignment based on target company configuration
- Sections and notes are copied with correct sequence
- Access control — only accessible companies are shown

Compatible with Odoo 17 Community and Enterprise.
    """,
    'author': 'Jeremie Ndjoli, Crakitech',
    'website': 'https://www.linkedin.com/in/jeremie-ndjoli-39a550255/',
    'support': 'crakitechpro@gmail.com',
    'depends': ['sale_management', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_copy_wizard.xml',
        'views/sale_order_view.xml',
    ],
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/34.png',
        'static/description/36.png',
        'static/description/38.png',
        'static/description/40.png',
        'static/description/41.png',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'price': 0.00,
    'currency': 'USD',
}
