# -*- coding: utf-8 -*-
{
    'name': "Bissweb",

    'summary': """
        Bissweb Modul Inherit for odoo""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Sol",
    'website': "",
    'category': 'Administration',
    'version': '1.0.0',
    'depends': ['base','crm','base_setup','hr','calendar','website','web'],
    'data': [
        'security/bissweb_security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_crm.xml',
        'data/format_printer.xml',
        'data/email_template.xml',        
        'views/views.xml',
        'views/doitac_crm.xml',        
        'views/res_users_view.xml',
        'report/web_form_view.xml',
        'views/form_lead_view.xml',
        'views/templates.xml',        
        'views/hr_attendance.xml',
        'views/dataclose.xml',
        'views/dataopen.xml',    
		'views/templates_public_form.xml'           
    ],
    'assets': {
    'web.assets_backend': [
        'bissweb/static/src/scss/style.scss',
        'bissweb/static/src/js/copy_link.js',
    ]
    },
     # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
