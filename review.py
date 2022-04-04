from datetime import datetime

REASONS = {1: 'Fora dos padrões', 2: 'Não gostei', 3: 'Não entendi'}
#                                 ^^^--- NÃO FAÇA ASSIM ------^^^


class Review:
    last_id = 0

    def __init__(self, **args):
        self.id = args.get('id') or self.next_id()
        self.author = args.get('author', '')
        self.file = args.get('file', '')
        self.lines = args.get('lines', '')
        self.created_at = args.get('created_at', str(datetime.now()))
        self.comment = args.get('comment', '')
        self.votes = args.get('votes', '')
    @classmethod

    def next_id(cls):
        cls.last_id += 1
        return cls.last_id

    def approve(self, reviewer: str):
        vote_list = [v for v in self.votes.split(',') if v]
        if reviewer and reviewer not in vote_list:
            vote_list.append(reviewer)
            self.votes = ','.join(vote_list)
            self.comment = ''
        return len(vote_list)

    def report_problem(self, reason: int):
        if self.approve('') > 2:
            raise Exception('A tarefa já foi aprovada.')
        self.comment = REASONS[reason]
