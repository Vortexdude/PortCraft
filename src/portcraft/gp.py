import requests
from src.decorators import AuthDecorator
from src.utils import url_joiner
from src.models import Model
import time




class GitUser(Model):

    @property
    def username(self):
        return self._getter("login")

    @property
    def name(self):
        return self._getter("name")

    def Etag(self):
        return self._Etag



class GB(object):
    model = GitUser

    def __init__(self, api_version=None, username=None, password=None, *args, **kwargs):
        if not api_version:
            api_version = "2022-11-28"

        self.api_version = api_version
        self.headers = {
            "X-GitHub-Api-Version": self.api_version
        }
        self.base_url = "https://api.github.com/"
        self.metadata = self.get_metadata()
        self.Etag = self.events().headers.get("Etag")

        
    @AuthDecorator
    def get_version(self):
        _url = self.base_url + 'versions'
        return requests.get(_url, headers=self.headers)

    @AuthDecorator
    def get_metadata(self):
        _url = url_joiner(self.base_url, "user")
        metadata = requests.get(_url, headers=self.headers).json()
        return self.model(attrs=metadata)

    def events(self, username=None, *args, **kwargs):
        if not username:
            username = self.metadata.username
        _url = url_joiner(self.base_url, "users", username, "events")

        if "Etag" in args or "Etag" in kwargs:
            self.headers.update({"If-None-Match": kwargs.get("Etag", None)})
        
        return requests.get(_url, headers=self.headers)

    def polling(self, time_interval: str = None):
        if not time_interval:
            time_interval = 60
        etag = None
        for i in range(60):
            if self.Etag:
                etag = self.Etag
            _ev = self.events(Etag=etag)
            print(_ev)
            #if _ev.status_code == 304:
            #    print("No new events are there")
            #else:
            #    print("Status code 200")
            time.sleep(4)


    def event_wrapper(self, repo, username=None, branch=None, event_type=None):
        _data = {}
        if not event_type:
            event_type = "PushEvent"
        if not username:
            username = self.metadata.username
        if not branch:
            branch = "image_methods"
        for event in self.events().json():
            if event['repo']['name'] == f"{username}/{repo}" and event['type'].lower() == event_type.lower():
                if branch == event['payload']['ref'].split("/")[-1]:
                    commits = [commit['message'] for commit in event['payload']['commits']]
                    _data.update({branch: commits})
        return _data

    
dd = GB()
dd.polling()
#print(dd.)
