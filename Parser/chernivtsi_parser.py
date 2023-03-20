import requests
import re

from bs4 import BeautifulSoup

from Parser.base_parser import BaseParser
    

class ChernivtsiParser(BaseParser):
    city = 'chernivtsi'
    transform_electricity_state = {
        'з': 'on',
        'в': 'off',
        'мз': 'maybe'
    }

    def __init__(self, groups_range: range, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups_range = groups_range
        self._soup = self.get_soup()
    
    @property
    def last_update(self):
        date = self._get_actual_date()
        time = self._get_actual_time()
        return f'{date} {time}'

    def _get_response(self):
        response = requests.get(self.parse_url, headers=ChernivtsiParser.headers)

        if not response.status_code == 200:
            response.raise_for_status()
        return response
    
    def get_soup(self):
        response = self._get_response()
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
        
    
    def _get_actual_time(self):
        schedule_time_html = self._soup.find_all(id='gsv_a')[0]
        schedule_time_text = schedule_time_html.text.strip()

        time_re = re.compile(r'(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$')
        schedule_time = time_re.search(schedule_time_text).group(0)

        return schedule_time

    def _get_actual_date(self):
        date = self._soup.find('div', {'id': 'gsv'}).ul.p.text.strip()
        return date
    
    def _get_groups_rows(self) -> list[dict]:
        groups_rows = list()

        for group_number in self.groups_range:
            row = self._soup.find('div', {'data-id': group_number})
            groups_rows.append({
                'group_number': group_number,
                'row': row,
            })
        return groups_rows
    
    def _format_schedules(self, groups_rows):
        groups_schedules = list()
    
        for group in groups_rows:
            group_number = group['group_number']
            electricity_states = group['row'].find_all('u')

            formatted_states = list()
            for time, electricity_state in enumerate(electricity_states):
                clear_state = electricity_state.text.strip()
                formatted_state = ChernivtsiParser.transform_electricity_state[clear_state]

                formatted_states.append({
                    'time': time,
                    'light': formatted_state,
                })
                
            groups_schedules.append({
                'group': group_number,
                'last_update': self.last_update,
                'schedule': formatted_states,
            })
        return groups_schedules
        
    def get_schedules(self):
        group_rows = self._get_groups_rows()
        schedules = self._format_schedules(group_rows)
        return schedules





# if __name__ == '__main__':
#     from pprint import pprint

#     parse_url = 'https://oblenergo.cv.ua/shutdowns/?next'
#     groups_range = range(1, 19)

#     p = ChernivtsiParser(groups_range, parse_url)
#     schedules = p.get_schedules()
#     pprint(schedules)