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
        'views/hospital_disease_views.xml',
        'views/hospital_history_views.xml',
        'views/timetable_views.xml',
        'wizard/disease_report_wizard_view.xml',
        'views/hospital_diagnosis_views.xml',
        'wizard/change_doctor_wizard_view.xml',
        'wizard/write_timetable_wizard_view.xml',
        'wizard/transfer_visit_wizard_view.xml',

        'views/hospital_menu.xml',
        'views/analysis_views.xml',        
        
        'data/hospital_disease_data.xml',


        # 'data/hr.hosp.doctor.csv',
        
        'demo/hospital_doctor_demo.xml',
        'demo/hospital_doctor_intern_demo.xml',
        'demo/hospital_patient_demo.xml',
        'demo/hospital_visit_demo.xml',
        'demo/hospital_analysis_demo.xml',

    ],

    'demo': [
        # 'demo/hospital_doctor_demo.xml',
        # 'demo/hospital_patient_demo.xml',
        # 'demo/hospital_visit_demo.xml',
        # 'demo/hospital_analysis_demo.xml',
    ],
}
