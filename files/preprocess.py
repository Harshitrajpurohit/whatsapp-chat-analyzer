# string data to dataframe
import re
import pandas as pd
from datetime import datetime

def process(string):
    AmPm_pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s|\u202F)?[apAP][mM]\s-\s'
    hour24_pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message = []
    dates = []
    if re.match(AmPm_pattern,string):
        message = re.split(AmPm_pattern, string)[1:]
        dt = re.findall(AmPm_pattern, string)
        for date in dt:
            normalized_timestamp = date.replace('\u202f', ' ')
            input_format = "%d/%m/%y, %I:%M %p - "
            output_format = "%d/%m/%y, %H:%M - "
            datetime_obj = datetime.strptime(normalized_timestamp, input_format)
            dates.append(datetime_obj.strftime(output_format))
        df = pd.DataFrame({"user_message": message, 'message_date': dates})
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    else:
        message = re.split(hour24_pattern, string)[1:]
        dates = re.findall(hour24_pattern, string)
        df = pd.DataFrame({"user_message": message, 'message_date': dates})
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    user = []
    message = []

    for m in df['user_message']:
        entry = re.split('([\w\W]+?):\s', m)
        if (entry[1:]):
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append('group_notification')
            message.append(entry[0])

    df['user'] = user
    df['message'] = message
    df.drop(columns=['user_message'], inplace=True)
    df.rename(columns={'message_date': 'date'}, inplace=True)

    df['year'] = (df['date']).dt.year;
    df['month'] = (df['date']).dt.month_name();
    df['day'] = (df['date']).dt.day;
    df['hour'] = (df['date']).dt.hour;
    df['minute'] = (df['date']).dt.minute;

    return df




