{
    'name': 'Auto-Attach Product Documents to Sales Emails',
    'version': '19.0.1.0.0',  
    'category': 'Sales/Sales',
    'summary': 'Automatically attach product documents when sending quotation emails',
    'description': """
        Auto-Attach Product Documents
        =============================
        
        This module automatically attaches product-related documents (catalogs, 
        specifications, images, etc.) when sending quotation emails from sales orders.
        
        Features:
        * Automatically detects products in the quotation
        * Adds all related product attachments to the email
        * Works seamlessly with the standard mail composer
        * Saves time and ensures customers receive complete documentation
        
        How it works:
        When composing an email from a sales order, the module automatically 
        retrieves all attachments linked to the products in the quotation and 
        adds them to the email being sent.
    """,
    'author': 'Jeremie Ndjoli',
    'website': 'https://github.com/Jeremie2001/odoo17-modules',
    'license': 'LGPL-3',
    'depends': ['sale', 'mail'],  
    'images': [
        
        'static/description/banner.jpg',
        'static/description/screenshot_before.png',
        'static/description/screenshot_after.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
