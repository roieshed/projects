from dateutil import parser
import re
import datetime
def get_availability(calender_json_string, date, start= None, end= None):
    print(date)
    x = filter(lambda x: bool(re.match(f'{date}', x['dates'][0])), calender_json_string)
    for i in x:
        print(i)
        
    
    # calender_json_string.sort(key=lambda x: x["dates"][0])
    # first_meeting = calender_json_string['dates'][0]
    # print(calender_json_string)

get_availability(
[
{"occupation":"second", "dates":("2022-01-20 20:46:48", "'2022-01-30 15:46:48.193251'")},
{"occupation":"7", "dates":("2022-01-92 16:46:48", "'2022-01-30 15:46:48.193251'")},
{"occupation":"first", "dates":("2019-01-30 15:45:48", "'2022-01-30 15:46:48.193251'")},
{"occupation":"8", "dates":("2042-01-01 15:45:48", "'2022-01-30 15:46:48.193251'")},
{"occupation":"fourth", "dates":("2022-01-30 15:45:48", "'2022-01-30 15:46:48.193251'")},
{"occupation":"third", "dates":("2022-01-25 18:45:48", "'2022-01-30 15:46:48.193251'")},
{"occupation":"sixth", "dates":("2022-01-30 15:46:40", "'2022-01-30 15:46:48.193251'")},
{"occupation":"fifth", "dates":("2022-01-30 15:45:49", "'2022-01-30 15:46:48.193251'")}
], '2022-01-30'
)