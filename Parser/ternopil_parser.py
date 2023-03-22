from datetime import datetime
import pytz
from pprint import pprint

from bs4 import Tag


# from Parser.base_parser import BaseParser
from base_parser import BaseParser

class TernopilParser(BaseParser):
    city_name = 'Тернопіль'
    city_id = 'ternopil'
    transform_electricity_state = {
        '#92d050': 'on',
        '#ff5050': 'off',
        '#ffff00': 'maybe',
    }
    def __init__(self, parse_url):
        self.parse_url = parse_url

    def value(self, r):
        if (r == 'I'):
            return 1
        if (r == 'V'):
            return 5
        if (r == 'X'):
            return 10
        if (r == 'L'):
            return 50
        if (r == 'C'):
            return 100
        if (r == 'D'):
            return 500
        if (r == 'M'):
            return 1000
        return -1
 
    def roman_to_decimal(self, str):
        res = 0
        i = 0
    
        while (i < len(str)):
            # Getting value of symbol s[i]
            s1 = self.value(str[i])
            if (i + 1 < len(str)):
                # Getting value of symbol s[i + 1]
                s2 = self.value(str[i + 1])
                # Comparing both values
                if (s1 >= s2):
                    # Value of current symbol is greater
                    # or equal to the next symbol
                    res = res + s1
                    i = i + 1
                else:
                    # Value of current symbol is greater
                    # or equal to the next symbol
                    res = res + s2 - s1
                    i = i + 2
            else:
                res = res + s1
                i = i + 1
        return abs(res)

    def get_current_time(self):
        time_zone = pytz.timezone('Europe/Kyiv')
        currnet_time = datetime.now(time_zone)
        return currnet_time

    def get_current_weekday(self, time):
        current_weekday = time.strftime('%A')
        return current_weekday

    def translate_weekday(self, weekday):
        # weekday = weekday.strip().lower()
        weekday = weekday.strip()
        days = {
            "monday": "понеділок",
            "tuesday": "вівторок",
            "wednesday": "середа",
            "thursday": "четвер",
            "friday": "п'ятниця",
            "saturday": "субота",
            "sunday": "неділя"
        }
        return days.get(weekday, '')

    def split_time(self, time, delimeter='.'):
        hour = time.split(delimeter)[0].lstrip('0')
        if not hour:
            hour = '0'
        return hour


    def format_time_interval(self, interval):
        start_hour = int(self.split_time(interval[0][0]))
        end_hour = int(self.split_time(interval[0][1]))
        
        electricity_state = interval[1]
        formatted_elecrticity_state = self.transform_electricity_state[electricity_state]

        times = list()
        for time in range(start_hour, end_hour):
            times.append(self.get_states_pattern(
                time=time,
                electricity_state=formatted_elecrticity_state
            ))
        
        return times

    
    def parse(self):
        soup = self.get_soup()
        soup.prettify(formatter=lambda s: s.replace(u'\xa0', ' '))
        full_table = soup.find('tbody')

        table_size = len(full_table)
        schedules_days = list()
        schedules_day = list()
        for index, row in enumerate(full_table):
            if not isinstance(row, Tag):
                continue

            schedules_day.append(row)
            if row.find('td', {'colspan': 9}, style=False) or index == table_size - 2:
                schedules_day.pop()
                schedules_days.append(schedules_day)
                del schedules_day
                schedules_day = list()

        current_time = self.get_current_time()
        current_weekday = self.get_current_weekday(current_time)
        current_weekday_ukr = self.translate_weekday(current_weekday)
        
        current_schedules_raw = None
        for schedule_daygroup in schedules_days:
            days = schedule_daygroup[0].td.text.strip().lower().strip('дні: ').replace(u'\xa0', '')
            if current_weekday_ukr in days:
                current_schedules_raw = schedule_daygroup
                current_schedules_raw.pop(0)
                break
        
        start_times = current_schedules_raw.pop(0).find_all('td')
        start_times.pop(0)
        start_times = [time.text.strip('-') for time in start_times]

        end_times = current_schedules_raw.pop(0).find_all('td')
        end_times.pop(0)
        end_times = [time.text.rstrip('.') for time in end_times]

        time_intervals = list(zip(start_times, end_times))

        group_numbers = list()
        all_light_states = list()
        for schedule in current_schedules_raw:
            current_schedule = schedule.find_all('td')
            group_number = current_schedule.pop(0).text.strip()
            group_number = self.roman_to_decimal(group_number)
            group_numbers.append(group_number)

            light_states = list()
            for light_state in current_schedule:
                light_states.append(light_state['style'].strip('background-color: ').strip(';'))

            all_light_states.append(light_states)
            del light_states
        
        formatted_light_states = list()
        for group_index, light_state in enumerate(all_light_states):
            states_with_times = list(zip(time_intervals, light_state))

            current_states = list()
            for state in states_with_times:
                current_states.extend(self.format_time_interval(state))

            formatted_light_states.append(self.get_groups_pattern(
                group_number=group_numbers[group_index],
                schedule=current_states,
                # last_update
            ))
            del current_states
        
        schedules = self.get_schedules_pattern(
            city_id=self.city_id,
            city_name=self.city_name,
        )
        schedules['groups'] = formatted_light_states

        pprint(schedules)

        





if __name__ == '__main__':
    parse_url = 'https://www.toe.com.ua/index.php/hrafik-pohodynnykh-vymknen-spozhyvachiv'
    parser = TernopilParser(parse_url)
    parser.parse()