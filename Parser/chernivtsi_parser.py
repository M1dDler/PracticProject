import re

# from Parser.base_parser import BaseParser

from Parser.base_parser import BaseParser
    

class ChernivtsiParser(BaseParser):
    city_name = 'Чернівці'
    city_id = 'chernivtsi'
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
    
    def _get_actual_time(self):
        # parsing if time goest to updates normally
        # schedule_time_html = self._soup.find_all(id='gsv_a')[0]
        # schedule_time_text = schedule_time_html.text.strip()

        # time_re = re.compile(r'(2[0-3]|[01]?[0-9]):([0-5]?[0-9])$')
        # schedule_time = time_re.search(schedule_time_text).group(0)
        schedule_time = '00:00'

        return schedule_time

    def _get_actual_date(self):
        date = self._soup.find('div', {'id': 'gsv'}).ul.p.text.strip()
        return date
    
    def _get_groups_rows(self) -> list[dict]:
        groups_rows = list()

        for group_number in self.groups_range:
            group_number_str = str(group_number)
            row = self._soup.find('div', {'data-id': group_number, 'id': 'inf' + group_number_str})
            groups_rows.append({
                'group_number': group_number_str,
                'row': row,
            })
        return groups_rows
    
    def _format_schedules(self, groups_rows):
        groups_schedules = self.get_schedules_pattern(
            city_id=self.city_id,
            city_name=self.city_name,
        )
    
        for group in groups_rows:
            group_number = group['group_number']
            electricity_states = group['row'].find_all('u')

            formatted_states = list()
            for time, electricity_state in enumerate(electricity_states):
                clear_state = electricity_state.text.strip()
                formatted_state = self.transform_electricity_state[clear_state]

                formatted_states.append(self.get_states_pattern(
                    time=time,
                    electricity_state=formatted_state,
                ))
                
            groups_schedules['groups'].append(self.get_groups_pattern(
                group_number=group_number,
                last_update=self.last_update,
                schedule=formatted_states,
            ))
        return groups_schedules
        
    def get_schedules(self):
        group_rows = self._get_groups_rows()
        schedules = self._format_schedules(group_rows)
        return schedules
