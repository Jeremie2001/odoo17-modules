{
    'name': 'Sale Order — Copy to Another Company',
    'version': '17.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Copy sale orders from one company to another in one click',
    'author': 'Jeremie Ndjoli, Crakitech',
    'depends': ['sale_management', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_copy_wizard.xml',
        'views/sale_order_view.xml',
    ],
    
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

