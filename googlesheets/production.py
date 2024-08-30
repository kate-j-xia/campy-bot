from .constants import POINTS_MAX

class Production:
    def __init__(self, username, firstname=None, lastname=None):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname        

        self.fullname = (firstname, lastname)

        self.uploads = 0 # number of online uploads
        self.uploaded = 0 # points earned for uploads
        self.story_ideas = 0 # points earned for story ideas
        self.sources = 0
        self.outline = 0
        self.first_draft = 0
        self.final_draft = 0

        # total points earned
        # self.total = self.story_ideas + self.sources + self.outline + self.first_draft + self.final_draft + self.uploaded
        self.total = 0
        # final grade in percentage
        # self.grade = self.total / POINTS_MAX * 100
        self.grade = 0

        self.status = None
        self.date = None

        self.completion_list = []
        self.upload_list = []

    def __str__(self) -> str:
        return f'{self.username} ({self.firstname} {self.lastname}): uploads={self.uploads}, uploaded={self.uploaded} \
            story_ideas={self.story_ideas}, sources={self.sources}, outline={self.outline}, \
            first_draft={self.first_draft}, final_draft={self.final_draft} \
            total={self.total}, grade={self.grade}'
	
