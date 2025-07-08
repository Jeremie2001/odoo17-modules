{
    'name': 'Product Margin',
    'summary': 'Track product margins on sales orders to analyze profitability',
    'version': '17.0.1.0.0',
    'category': 'Sales/Sales',
    'author': 'Jeremie',
    'website': 'https://ton-site-ou-github.com',
    'license': 'LGPL-3',
    'depends': [
        'sale_management',
    ],
    'data': [
        'views/marge_view.xml',
    ],
    'images': [
        
        'static/description/screenshot1.png',
        'static/description/screenshot2.png',
    
    ],
    'installable': True,
    'application': False,
    'description': """
Product Margin on Sales Orders
==============================

This module adds the *Margin* field on sales orders.

It helps you analyze the profitability of each sales order line by calculating the difference between the **Unit Sale Price** and the **Cost Price** of the product.

✨ Features:
------------
- Adds *Margin* on each sales order line.
- Calculates the profitability per product.
- Integrated seamlessly into the sales module.

👤 Target audience:
-------------------
- Sales managers
- Accountants
- Business owners who want to monitor profit margins on sales.

Compatible with **Odoo 17.0** Community & Enterprise editions.
""",
}
