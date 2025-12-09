{
    'name': 'Indentix K90 Pro+ Biometric Attendance',
    'version': '19.0.1.0.0',
    'category': 'Human Resources/Attendance',
    'summary': 'Sync Indentix K90 Pro+ (ZKTeco) biometric device with Odoo',
    'description': """
        Connects Indentix K90 Pro+ ID+B biometric machine to Odoo 19
        • Real-time sync
        • Test connection button
        • Manual & auto sync
        • Works on Odoo.sh / Self-hosted
    """,
    'author': 'Your Company',
    'depends': ['hr', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/zk_attendance_views.xml',
        'data/cron.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'external_dependencies': {
        'python': ['zk'],
    },
}
