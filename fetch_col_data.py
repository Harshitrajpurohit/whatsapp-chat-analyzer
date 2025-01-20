from pyexpat.errors import messages
from urlextract import URLExtract
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd

def fetch_data(character,df):
    if character == 'All':
        count = 0
        for msg in df['message']:
            count+= len(msg)

        link=[]
        for str in df['message']:
            link.extend(URLExtract().find_urls(str))

        return df.shape[0], count, len(link)
    else:
        count = 0
        data_student = df[df['user'] == character]
        for msg in data_student['message']:
            count += len(msg)

        link=[]
        for str in data_student['message']:
            link.extend(URLExtract().find_urls(str))


        return df[df['user'] == character].shape[0], count, len(link)


def most_active(df):
    count = df[df['user'] != 'group_notification']['user'].value_counts().head(10)
    return count

def word_cloud(character , df):
    filtered_messages = df[df['message'] != '<Media omitted>\n']
    if character == 'All':
        filtered_messages = filtered_messages[filtered_messages['user'] != 'group_notification']['message']
        return filtered_messages
    else:
        filtered_messages = filtered_messages[filtered_messages['user'] == character]['message']
        return filtered_messages

def timeline_chart(character , df):
    df['month_num'] = df['date'].dt.month
    df['complete_date'] = df['date'].dt.date

    if character == 'All':
        if len(df['month'].unique()) <= 1:
            grouped_df = df.groupby('complete_date')['message'].count()
            timeline = grouped_df.reset_index()
        else:
            grouped_df = df.groupby(['year', 'month_num', 'month'])['message'].count()
            timeline = grouped_df.reset_index()
            time = []
            for i in range(timeline.shape[0]):
                time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
            timeline['complete_date'] = time
    else:
        if len(df['month'].unique()) <= 1:
            grouped_df = df[df['user'] == character].groupby('complete_date')['message'].count()
            timeline = grouped_df.reset_index()
        else:
            grouped_df = df[df['user'] == character].groupby(['year', 'month_num', 'month'])['message'].count()
            timeline = grouped_df.reset_index()
            time = []
            for i in range(timeline.shape[0]):
                time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
            timeline['complete_date'] = time

    return timeline

def weekly_timeline_chart(character , df):

    if(character != 'All'):
        df = df[df['user'] == character]

    week_day = df['date'].dt.day_name().value_counts()
    return week_day

def active_heatmap(character, df):

    if(character != 'All'):
        df = df[df['user'] == character]

    a = []
    for i in range(df['hour'].shape[0]):
        if str(df['hour'][i]).zfill(2) == '23':
            a.append(str(df['hour'][i]).zfill(2) + "/" + str(00).zfill(2))
        else:
            a.append(str(df['hour'][i]).zfill(2) + "/" + str((df['hour'][i]) + 1).zfill(2))
    df['period'] = a

    week_day = df['date'].dt.day_name()

    pivot_tab = df.pivot_table(index=week_day, columns='period', values='message', aggfunc='count').fillna(0)

    return pivot_tab