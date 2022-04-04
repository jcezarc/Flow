from git import Git
from review import Review
from orm import Commands # <<---- Esse a gente já viu antes! ;)


class PullRequest:
    def __init__(self, git: Git, author: str):
        self.git = git
        self.author = author
        self.to_review: list[Review] = []

    def write(self, db_function: callable):
        for file, lines in self.git.diff().items():
            db_function(Commands(
                Review(author=self.author, file=file, lines='\n'.join(lines))
            ).sql['insert'])

    def read(self, db_function: callable):
        dataset = db_function(
            Commands(
                self.empty_review(),
                [f'author <> "{self.author}"']).sql['select']
        )
        self.to_review = [Review(**row) for row in dataset]

    def resolve(self, item: Review, approved: bool, db_function: callable):
        cmd = Commands(item)
        if approved and item.approve(self.author) > 2:
            db_function(cmd.sql['delete'])
        else:
            db_function(cmd.sql['update'])
        self.to_review.remove(item)

    def empty_review(self):
        return Review(id=-1)
