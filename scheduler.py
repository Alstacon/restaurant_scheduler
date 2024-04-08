import calendar
import json
import datetime


class OpeningHoursFormatter:
    """
    Accepts JSON-formatted opening hours of a restaurant as an input
    and returns the rendered human-readable format as a text output.
    """
    required_keys_for_day = ['type', 'value']
    days = list(map(lambda x: x.lower(), calendar.day_name))

    def __init__(self, opening_hours: dict[str, list[dict[str, str | int]]]) -> None:
        self.opening_hours = opening_hours

    def check_days(self) -> None:
        """
        Checking the validity of the days input data
        :return:
        """
        if len(set(map(lambda x: x.lower(), self.opening_hours.keys()))) < len(self.opening_hours.keys()):
            raise ValueError('''The keys should be unique. Days can't repeat in different entries.''')

        for day in self.opening_hours.keys():
            if day.lower() not in self.days:
                raise ValueError(f'The keys can only be the days of the week "{day}" is incorrect key.')

    def check_hours(self):
        """
        Checking the validity of the hours input data
        :return:
        """
        for day, events in self.opening_hours.items():
            if not isinstance(events, list):
                raise ValueError(f'''The entry on {day} should contain an array of working hours''')
            for event in events:
                if not isinstance(event, dict):
                    raise ValueError(f'''The entries on {day} must be a dict''')
                for key in self.required_keys_for_day:
                    if len(event.keys()) > 2:
                        raise ValueError('''The entry should contain only two keys: "type" and "value"''')
                    if key not in event:
                        raise ValueError(f'''The entry on {day} should contain {key} field for {event.get('type')}''')
                if not isinstance(event.get('value'), int):
                    raise ValueError(f'''The value for key {event.get('type')} on {day} should be an integer''')
                if event.get('value') <= 0 or event.get('value') > 86399:
                    raise ValueError(f'''The value for key {event.get('type')} on {day} is incorrect.''')

    def check_input_data(self) -> None:
        """
        Checking the validity of the input data
        :return:
        """
        if not isinstance(self.opening_hours, dict):
            raise ValueError('''Input data must be a dict''')
        if not self.opening_hours.items():
            print('''Input should contain any data to build schedule''')

        self.check_days()
        self.check_hours()

    def format_opening_hours(self) -> str:
        """
        Formats the opening hours data into a human-readable format
        :return: str formatted working hours
        """
        self.check_input_data()
        formatted_hours = []

        for day in self.days:
            hours = self.opening_hours.get(day, 'missed')
            if hours == 'missed':
                continue
            if not hours:
                formatted_hours.append(f'''{day.capitalize()}: Closed''')
            else:
                open_times = [hour["value"] for hour in hours if hour.get("type") == "open"]
                close_times = [hour["value"] for hour in hours if hour["type"] == "close"]

                if len(close_times) > len(open_times):
                    if close_times[0] != 3600:
                        open_times.insert(0, 3600)
                    else:
                        close_times.pop(0)

                formatted_open_times = [self.format_time(t) for t in open_times]
                if close_times:
                    formatted_close_times = [self.format_time(t) for t in close_times]
                else:
                    formatted_close_times = [self.format_time(3600)]

                formatted_hours.append(
                    f'''{day.capitalize()}: {', '.join(f'{open} - {close}' for open, close in zip(formatted_open_times, formatted_close_times))}''')

        return "\n".join(formatted_hours)

    @staticmethod
    def format_time(unix_time: int) -> str:
        """
        Formats a Unix timestamp into 12-hour clock format.
        :param unix_time: int
        :return: human-readable time
        """
        dt_object = datetime.datetime.fromtimestamp(unix_time, datetime.UTC)

        hours = dt_object.hour
        minutes = dt_object.minute

        part_of_the_day = 'AM' if hours < 12 else 'PM'
        hours = hours if hours <= 12 else hours - 12

        if minutes != 0:
            return f'{hours:01}:{minutes:01} {part_of_the_day}'
        return f'{hours:01} {part_of_the_day}'


if __name__ == "__main__":
    input_json = ''
    print('Enter JSON-formatted opening hours. At the end press Enter twice.')
    while True:
        line = input()
        if line:
            input_json += line
        else:
            break
    try:
        opening_hours_data = json.loads(input_json)
    except json.decoder.JSONDecodeError:
        raise ValueError('Invalid JSON data')
    formatter = OpeningHoursFormatter(opening_hours_data)
    print(formatter.format_opening_hours())
