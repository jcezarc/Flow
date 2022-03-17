import os
from tasks import tasks_assigned_to_me
from git import Git
from conda import Conda


def main(project: str, env: str, flag: str):
    company_name = os.environ['COMPANY_NAME']
    task = tasks_assigned_to_me({
        'url': os.environ['JIRA_URL'],
        'username': os.environ['JIRA_USERNAME'],
        'password': os.environ['JIRA_PASSWORD'],
        'project': project,
        'status': 'Doing' if flag == 'end' else 'To Do'
    })[0]
    conda = Conda(env) #--- Ambiente de desenvolvimento
    git = Git(project, company_name)
    git.checkout(task.key) #--- checkout do branch da tarefa
    if flag == 'start': # ---- Inicia a primeira tarefa atribuída a você:
        task.update(started = True) #--- marca como DOING
        git.pull()
    else:
        git.commit(task.fields.summary)
        git.push()
        conda.deactivate()


print('FLOW'.center(50, '-'))
print('-' * 50)
if len(sys.argv) < 3:
    print('Usage: python3 args.py project env [start/end]')
else:
    params = [a for i, a in enumerate(sys.argv) if i > 0]
    main(*params)
