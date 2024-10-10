
from enum import Enum

GRADES_UPDATE_STARTING_ROW = 3

POINTS_UPLOADED = 20
POINTS_MAX = 160

COMPLETION_STATUS_COMPLETE = 'Complete'

COMPLETION_ITEMS = ['story_ideas', 'sources', 'outline', 'first_draft', 'final_draft']

Completion_points = {
    # sheet column header/completion items to completion points mapping
    "story_ideas": 10,
    "sources": 10,
    "outline": 10,
    "first_draft": 10,
    "final_draft": 30
}

Incompleted_assignments = {
    # incompleted assignments to sheet column mapping
    "story_ideas": 1,
    "sources": 2,
    "outline": 3,
    "first_draft": 4,
    "final_draft": 5
}

class Incompletes(Enum):
    STORY_IDEAS = 1
    SOURCES = 2
    OUTLINE = 3
    FIRST_DRAFT = 4
    FINAL_DRAFT = 5

NUMBER_TO_ASSIGNMENTS = {
    # incompleted assignments to sheet column mapping
    1: "5 story ideas",
    2: "5 sources",
    3: "outline",
    4: "first draft",
    5: "final draft"
}