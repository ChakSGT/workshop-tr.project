# -*- coding: utf-8 -*-
{
    'name': "Open Project",

    'summary': """Manage trainings""",

    'description': """
        Open Academy module for managing trainings:
            - training courses
            - training sessions
            - attendees registration
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
        'purchase',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'templates.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/wizard_view.xml',
        'views/project.xml',
        'views/sales.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo.xml',
    ],
}
