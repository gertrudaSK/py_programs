# -*- coding: utf-8 -*-
{
    'name': "Home Design",

    'summary': """Manage trainings""",

    'description': """
        Open Academy module for managing trainings:
            - training courses
            - training sessions
            - attendees registration
    """,

    'author': "GSK",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'board', 'hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/project_view.xml',
        'views/invoice_view.xml',
        'views/works_view.xml',
        'views/partner_inherited.xml',
        'views/hr_employee_inherited.xml',
        'views/project_board.xml',
        'reports/invoice_reports.xml',
        'reports/project_reports.xml',
        'views/mail_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
}
