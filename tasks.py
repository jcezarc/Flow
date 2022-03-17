from jira import JIRA


def tasks_assigned_to_me(**args):
    jira = JIRA(args['url'], basic_auth=(args['username'], args['password']))
    query = 'assignee = {} AND project == {} AND status == {}'.format(
        'currentUser()',
        args['project'],
        args['status'],
    )
    return [issue for issue in jira.search_issues(query)]
