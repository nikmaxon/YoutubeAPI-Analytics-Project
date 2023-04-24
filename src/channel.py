import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YouTube API')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

    def __str__(self):
        return f'{self.title}({self.url})'

    def __add__(self, other):
        return int(self.subs) + int(other.subs)

    def __sub__(self, other):
        return int(self.subs) - int(other.subs)

    def __gt__(self, other):
        return int(self.subs) > int(other.subs)

    def __ge__(self, other):
        return int(self.subs) >= int(other.subs)

    def __lt__(self, other):
        return int(self.subs) < int(other.subs)

    def __le__(self, other):
        return int(self.subs) <= int(other.subs)

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    @property
    def title(self):
        return self.print_info()["items"][0]["snippet"]["title"]

    @property
    def description(self):
        return self.print_info()["items"][0]["snippet"]["description"]

    @property
    def url(self):
        return f'https://www.youtube.com/channel/{self.__channel_id}'

    @property
    def subs(self):
        return self.print_info()["items"][0]["statistics"]["subscriberCount"]

    @property
    def video_count(self):
        return self.print_info()["items"][0]["statistics"]["videoCount"]

    @property
    def viewers(self):
        return self.print_info()["items"][0]["statistics"]["viewCount"]

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        # print(json.dumps(channel, indent=2, ensure_ascii=False))
        return channel

    def to_json(self, filename):
        channel_dict = {"id": self.__channel_id,
                        "title": self.title,
                        "video_count": self.video_count,
                        "url": self.url,
                        "description": self.description
                        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(channel_dict, f, indent=2, ensure_ascii=False)

# vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
# vdud.to_json('vdud.json')
