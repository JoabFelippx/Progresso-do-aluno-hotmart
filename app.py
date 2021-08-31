import requests
import json
import getToken
from datetime import datetime
import pandas as pd

# parametros para fazer as requisições
api = 'https://developers.hotmart.com/'
TOKEN = getToken.TOKEN_CB()

# subdominio do curso
subdomain = ''

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer ' + TOKEN
}
path = './alunos-progresso/'


# converter datas para exibição
def convertUnixTimestamp(timestamp):

    datetime_converted = datetime.fromtimestamp(timestamp/1000)
    formated_date = datetime_converted.isoformat(
        sep=' ', timespec='milliseconds')

    return formated_date.split(' ')[0]


# coletar dados dos estudantes
def getStudents():

    students_datas = []
    user_id = []

    url = api + 'club/api/v1/users?subdomain=' + subdomain

    res_1 = requests.get(url, headers=HEADERS)
    data = res_1.json()
    items_info = data['items']
    page_info = data['page_info']

    # verificar se existe mais paginas
    for items in page_info.items():

        if 'next_page_token' in items[0]:

            url = api + 'club/api/v1/users?page_token=' + \
                items[1] + '&subdomain=' + subdomain

            res_2 = requests.get(url, headers=HEADERS)

            next_page_data = res_2.json()
            # juntando os dados das paginas
            items_info += next_page_data['items']
            page_info = next_page_data['page_info']

    # separar as informações dos alunos de acordo com seu ID
    for c in range(0, len(items_info)):
        infos = {
            items_info[c]['user_id']: [
                items_info[c]['name'], items_info[c]['email']]
        }
        user_id.append(items_info[c]['user_id'])
        students_datas.append(infos)

    return user_id, students_datas


# progresso de cada aluno
def studProgress(user_id, students_datas):

    modules = []
    pages = []
    completed = []
    datas = []

    for i in range(0, len(user_id)):

        url = api + 'club/api/v1/users/' + \
            user_id[i] + '/lessons?subdomain=' + subdomain

        # nome do aluno
        name = students_datas[i][user_id[i]][0]
        res_3 = requests.get(url, headers=HEADERS)
        lessons = res_3.json()['lessons']

        # gerar arquivo com as informações do progresso do aluno
        for v in range(0, len(lessons)):

            # verificar se a aula foi assistida
            if lessons[v]['is_completed'] == True:
                completed.append('Sim')
                datas.append(convertUnixTimestamp(
                    lessons[v]['completed_date']))
            else:
                datas.append('')
                completed.append('Não')

            # listar os modulos e as aulas
            modules.append(lessons[v]['module_name'])
            pages.append(lessons[v]['page_name'])

            dict_inf = {
                'Modulo': modules,
                'Aula': pages,
                'Completo': completed,
                'Data': datas,
            }
            dados = pd.DataFrame(data=dict_inf)
            dados.to_excel(f'{path}{name}.xls', index=False)

        modules = []
        pages = []
        completed = []
        datas = []


# iniciar programa
if __name__ == '__main__':

    getStudents = getStudents()
    print(getStudents)
    studProgress(getStudents[0], getStudents[1])
