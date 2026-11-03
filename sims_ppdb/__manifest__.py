{
    'name': "sims_ppdb",

    'summary': "Sistem Penerimaan Peserta Didik Baru Madrasah",

    'description': """
        Modul PPDB untuk mengelola master data dan proses
        penerimaan peserta didik baru madrasah.
    """,

    'author': "Widianto",
    'website': "Will Create",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
        'security/ir.model.access.csv',
        'data/ppdb_sequence.xml',
        'views/ppdb_period_views.xml',
        'views/ppdb_document_type_views.xml',
        'views/ppdb_selection_component_type_views.xml',
        'views/ppdb_selection_component_views.xml',
        'views/ppdb_registration_path_views.xml',
        'views/ppdb_achievement_type_views.xml',
        #'views/ppdb_document_requirement_views.xml',
        'views/ppdb_wave_views.xml',
        'views/ppdb_wave_path_views.xml',
        'views/ppdb_wave_path_selection_views.xml',
        'views/ppdb_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

