app_name = "payroll_app"
app_title = "payroll_app"
app_publisher = "Avanti"
app_description = "Assignment 3"
app_email = "avanti.bhondwe@gmail.com"
app_license = "mit"

# Fixtures
fixtures = [
    {"dt": "DocType", "filters": [["module", "in", ["Payroll App"]]]},
    {"dt": "Client Script", "filters": [["module", "in", ["Payroll App"]]]},
    {"dt": "Server Script", "filters": [["module", "in", ["Payroll App"]]]},
    {"dt": "Print Format", "filters": [["module", "in", ["Payroll App"]]]},
    {"dt": "Workflow", "filters": [["document_type", "in", ["Leave Request Pro", "Client Project Onboarding", "Performance Review", "Monthly Payroll Run"]]]},
    {"dt": "Notification", "filters": [["document_type", "in", ["Leave Request Pro", "Client Project Onboarding", "Performance Review", "Monthly Payroll Run"]]]},
    {"dt": "Workflow State"},
    {"dt": "Workflow Action Master"},
    {"dt": "Role", "filters": [["name", "in", ["Leave Manager", "Leave HR", "Leave CEO", "Project Manager", "Tech Lead", "HR Manager", "HR User", "Appraisal Manager", "Employee Self Service", "Finance Head", "CEO"]]]},
]
