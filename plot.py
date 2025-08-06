from graphviz import Digraph

dot = Digraph(comment='Automation Solution Overview', format='png')

# Inputs
dot.node('F', 'HTML Forms')
dot.node('E', 'Emails')
dot.node('I', 'Invoices')

# Parsers
dot.node('FP', 'Form Parser')
dot.node('EP', 'Email Parser')
dot.node('IP', 'Invoice Parser')

# Validation
dot.node('V', 'Validation Engine')

# Dashboard
dot.node('D', 'User Dashboard\n(Approve/Edit/Reject)')

# Outputs
dot.node('G', 'Google Sheets/Excel')
dot.node('L', 'Logs & Alerts')

# Edges (now one-by-one)
dot.edge('F', 'FP')
dot.edge('E', 'EP')
dot.edge('I', 'IP')
dot.edge('FP', 'V')
dot.edge('EP', 'V')
dot.edge('IP', 'V')
dot.edge('V', 'D')
dot.edge('D', 'G', label='Approved')
dot.edge('D', 'L', label='Logs')

# Render to file
dot.render('solution_overview_diagram', view=True)
