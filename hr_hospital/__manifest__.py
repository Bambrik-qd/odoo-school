{
    'name': "hr_hospital",
    'version': '16.0.1.0.0',
    'category': 'Uncategorized',
    'author': "Zhmyhova T.N.",
    'maintainer': 'ztn@qdes.com.ua',
    'website': "https://github.com/Bambrik-qd/odoo-school",
    'license': 'LGPL-3',
    'depends': ['base'],

    'summary': "A module for hospital automation: keeping records of doctor and patients",

    'data': [
        'security/ir.model.access.csv',

        'views/hospital_doctor_views.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_visit_views.xml',
        'views/hospital_menu.xml',

        'data/hospital_disease_data.xml',
        'data/hr.hosp.doctor.csv',

    ],

    'demo': [
        'data/hospital_doctor_demo.xml',
        'data/hospital_patient_demo.xml',
    ],
}
