from jinja2 import Environment, FileSystemLoader

address = 'Свердловская обл, г. Екатеринбург, СНТ <<Западный-1>>,  уч. 151'
cadaster = '66:41:0507091:21'
nomenclature = 'O-41-25'

# env = Environment(loader=FileSystemLoader('D:\GIT-REPOS\latex-templates\water'))
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('water.tex')

# data = {
#     'ADDRESS': '{Свердловская обл, г. Екатеринбург, СНТ <<Западный-1>>,  уч. 151}',
#     'CADASTER': '{66:41:0507091:21}',
#     'NOMENCLATURE': '{O-41-25}'
# }

data = {
    'ADDRESS': '{' + address + '}',
    'CADASTER': '{' + cadaster + '}',
    'NOMENCLATURE': '{' + nomenclature + '}'
}

tex = template.render(**data)
# tex = template.render(ADDRESS='{Свердловская обл, г. Екатеринбург, СНТ <<Западный-1>>,  уч. 151}')
print(tex)
