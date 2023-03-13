import os
import requests

from abc import ABC
from typing import Optional
from dataclasses import dataclass, field

from errors import ClickUpException

from dotenv import load_dotenv

load_dotenv()


class ClickupObject(ABC):
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": os.getenv("CLICKUP_API_TOKEN"),
        }
        self.root_url = "https://api.clickup.com/api/v2/"


@dataclass
class Space(ClickupObject):
    id: str

    def __post_init__(self):
        super().__init__()

        self.space_url = self.root_url + f'space/{self.id}/'
        self.tag_url = self.space_url + 'tag'
    
    def get_tags(self):
        response = requests.get(self.tag_url, headers=self.headers)

        if response.status_code != 200:
            raise ClickUpException(response=response, message='Failed to retrieve tags.')
        
        return [Tag(**tag) for tag in response.json()['tags']]


class List(ClickupObject):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.list_url = self.root_url + f"/list/{self.id}"
        self.task_url = self.list_url + "/task"

    def create_task(self, task):
        response = requests.post(
            self.task_url, json={key:value for key, value in task.__dict__.items() if value is not None}, headers=self.headers
        )

        if response.status_code != 200:
            raise ClickUpException(response=response, message='Task creation failed.')

        response_data = response.json()

        task.update(response_data)

        return response_data

    def get_tasks(self, filter_parameters=None):
        response = requests.get(
            self.task_url, headers=self.headers, params=filter_parameters
        )

        if response.status_code != 200:
            raise ClickUpException(response=response, message='Task retrieval failed.')
        
        return [Task(**task) for task in response.json()['tasks']]


@dataclass
class Task(ClickupObject):
    name: str
    id: Optional[str] = None
    custom_id: Optional[str] = None
    text_content: Optional[str] = None
    description: Optional[str] = None
    status: Optional[dict] = "Open"
    orderindex: Optional[str] = None
    date_created: Optional[int] = None,
    date_updated: Optional[int] = None,
    date_closed: Optional[int] = None,
    date_done: Optional[int] = None,
    archived: bool = False,
    creator: Optional[dict] = None
    assignees: list = field(default_factory=list)
    watchers: list = field(default_factory=list)
    checklists: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    parent: Optional[dict] = None
    priority: Optional[dict] = None
    due_date: Optional[int] = None
    start_date: Optional[int] = None
    points: Optional[int] = None
    time_estimate: Optional[int] = None
    time_spent: Optional[int] = None
    custom_fields: list = field(default_factory=list)
    dependencies: list = field(default_factory=list)
    linked_tasks: list = field(default_factory=list)
    team_id: Optional[str] = None
    url: Optional[str] = None
    sharing: Optional[dict] = None
    token: Optional[str] = None
    seo_optimized: bool = False
    permission_level: Optional[str] = None
    list: Optional[dict] = None
    project: Optional[dict] = None
    folder: Optional[dict] = None
    space: Optional[dict] = None

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', id='{self.id}')"

    def __post_init__(self):
        super().__init__()

    def update(self, task_dict):
        self.__dict__ = task_dict

    @staticmethod
    def custom_fields(fields):
        id_map = {
            'URL': os.getenv('CLICKUP_URL_FIELD_ID')
        }

        return [{'id': id_map[field['name']], 'value': field['value']} for field in fields]


@dataclass
class Tag(ClickupObject):
    name: str
    tag_fg: str
    tag_bg: str
    creator: Optional[str] = None

    def __post_init__(self):
        super().__init__()
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"
