import requests

from bs4 import BeautifulSoup


class BaseParser:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    def __init__(self, parse_url: str):
        self.parse_url = parse_url
    
    def _save_html_response(self, content: bytes, filename='parsed.html'):
        with open(filename, 'wb+') as file:
            file.write(content)
    
    @property
    def last_update(self):
        raise NotImplementedError

    def get_schedules(self):
        raise NotImplementedError

    def _get_response(self):
        response = requests.get(self.parse_url, headers=self.headers)

        if not response.status_code == 200:
            response.raise_for_status()
        return response
    
    def get_soup(self):
        response = self._get_response()
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    
    def get_schedules_pattern(self, city_id=None, city_name=None):
        schedules_pattern = {
            'city_id': city_id,
            'city_name': city_name,
            'groups': list(),
        }
        return schedules_pattern
    
    def get_groups_pattern(self, group_number=None, last_update=None, schedule=None):
        groups_pattern = {
            'group': group_number,
            'last_update': last_update,
            'schedule': schedule,
        }
        return groups_pattern
    
    def get_states_pattern(self, time=None, electricity_state=None):
        groups_pattern = {
            'time': time,
            'light': electricity_state,
        }
        
        return groups_pattern
