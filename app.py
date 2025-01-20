import streamlit as st
from files import fetch_col_data
from files import preprocess
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from wordcloud import WordCloud


st.set_page_config(layout="wide")

st.title("Chat Analyzer")
dataframe = pd.DataFrame()
file = st.file_uploader("Upload Your WhatsApp File")
if file is not None:
    file = file.getvalue()
    data = file.decode('utf-8')
    dataframe = preprocess.process(data)
    select_box = st.selectbox("Choose Tabs",['Analysis','Table'])
    if select_box == 'Table':
        st.dataframe(dataframe)
    elif select_box == 'Analysis':
        user_name = dataframe['user'].unique().tolist()
        user_name.remove('group_notification')
        user_name.insert(0, 'All')
        character = st.selectbox("Pick User",user_name)

        num_of_msgs, no_words, num_links = fetch_col_data.fetch_data(character, dataframe)
        st.write("\n\n")

        col1, col2, col3 = st.columns(3, border = True)

        with col1:
            st.header('Total Messages')
            st.title(num_of_msgs)
        with col2:
            st.header('Total Words')
            st.title(no_words)
        with col3:
            st.header('Total Urls')
            st.title(num_links)

        if character == 'All':
            st.header("Most Active User")
            count = fetch_col_data.most_active(dataframe)
            col1, col2 = st.columns(2, gap = 'large')

            with col1:
                fig, ax = plt.subplots(figsize = (4,2))
                sb.barplot(x=count.index, y=count.values, ax=ax, palette='viridis')
                ax.set_xlabel('Users',size = 7)
                ax.set_ylabel('Messages', size = 7)
                ax.set_xticklabels(count.index, rotation=45, ha='right',size = 5)
                ax.tick_params(axis='y', labelsize=5)
                st.pyplot(fig)
            with col2:
                st.dataframe(count, width = 400)


        st.header("Word Cloud Visualization")
        filtered_messages = fetch_col_data.word_cloud(character, dataframe)
        wordcloud = WordCloud(width=500, height=210, min_font_size=2, background_color='white')
        fig, ax = plt.subplots()
        ax.imshow(wordcloud.generate(" ".join(filtered_messages)), interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)


        st.header("Timeline")
        timeline = fetch_col_data.timeline_chart(character, dataframe)
        fig, ax = plt.subplots(figsize = (12,6))
        ax.plot(timeline['complete_date'], timeline['message'], marker = 'o', linestyle='-', color='red')
        plt.xticks(rotation = 45, size = 8)
        plt.yticks(size=8)
        ax.set_xlabel('Months', size=10)
        st.pyplot(fig)


        st.header("Weekly Massages")
        weekly_timeline = fetch_col_data.weekly_timeline_chart(character , dataframe)
        fig, ax = plt.subplots(figsize = (12,6))
        ax.bar(weekly_timeline.index,weekly_timeline.values)
        plt.xticks(rotation = 45, size = 8)
        plt.yticks(size=8)
        ax.set_xlabel('Weekdays', size=10)
        st.pyplot(fig)

        st.header("24 Hour Heatmap")
        pivot_table = fetch_col_data.active_heatmap(character, dataframe)
        fig, ax = plt.subplots(figsize = (12,6))
        ax = sb.heatmap(pivot_table)
        plt.xticks(rotation = 45, size = 8)
        plt.yticks(rotation = 0, size = 8)
        ax.set_xlabel('Period',size = 10)
        ax.set_ylabel('Weekdays', size=10)
        st.pyplot(fig)

