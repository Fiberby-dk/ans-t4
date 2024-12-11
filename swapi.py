from keyword import kwlist
from typing import Type, Union
from urllib.parse import urlparse

import requests


class SwapiType:
    type_slug = None

    def __init__(self, **kwargs):
        self.data = kwargs


class SwapiList(list):
    def __init__(self, obj_type: Type[SwapiType], **kwargs):
        super().__init__()
        self.obj_type = obj_type
        self.count = kwargs["count"]
        self.next = kwargs["next"]
        self.previous = kwargs["previous"]
        for value in kwargs["results"]:
            self.append(obj_type(**value))

    def append(self, obj: Union[Type[SwapiType], SwapiType]):
        if isinstance(obj, self.obj_type):
            super().append(obj)


"""
NOTE
Refactored the People class into "BaseEntity" class since both people and films are 
sharing pretty much the same functionality, as well to make it easier to further 
development to the SWAPI.
"""


class BaseEntity(SwapiType):
    type_slug = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getattr__(self, attr_name):
        print(self.data)
        if attr_name in self.data:
            return self.data[attr_name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{attr_name}'"
        )

    def id_from_url(self) -> int:
        if "url" not in self.data:
            raise ValueError("'url' not found in data")
        path = urlparse(self.data["url"]).path
        path_parts = path.split("/")
        print(path_parts)
        print(self.data["url"])
        if path_parts[1] != "api" or path_parts[2] != self.type_slug:
            raise Exception("Invalid API URL")
        return int(path_parts[3])


class People(BaseEntity):
    type_slug = "people"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Film(BaseEntity):
    type_slug = "films"
    people_list = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """
    NOTE
    A function that requests the information about the characters in the movie. 
    However this fires off multiple of http requests that preferrably should be 
    cached to increase the load time. 
    """

    def get_people(self):
        people_list = []
        for char in self.characters:
            sess = requests.Session()
            req = sess.get(char)
            people_list.append(req.json())
        self.people_list = people_list


class Swapi:
    def __init__(self):
        self.session = requests.Session()

    def get(
        self, obj_type: Type[SwapiType], page: int = None, obj_id: int = None
    ) -> SwapiType | SwapiList:
        url = Swapi._build_request_url(obj_type, obj_id)
        if page is not None:
            resp = self.session.get(url, params={"page": page})
        else:
            resp = self.session.get(url)
        if obj_id is not None:
            return obj_type(**resp.json())
        return SwapiList(obj_type, **resp.json())

    @staticmethod
    def _build_request_url(obj_type: Type[SwapiType], obj_id: int = None):
        if obj_id is not None:
            return f"https://swapi.dev/api/{obj_type.type_slug}/{obj_id}"
        return f"https://swapi.dev/api/{obj_type.type_slug}"
