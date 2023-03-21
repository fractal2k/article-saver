import os
from dotenv import load_dotenv

load_dotenv()

from clickup import Space, List, Task

import streamlit as st


knowledge_base_space = Space(id=os.getenv("CLICKUP_KNOWLEDGE_BASE_SPACE_ID"))
saved_articles_list = List(id=os.getenv("CLICKUP_SAVED_ARTICLES_LIST_ID"))
tags = knowledge_base_space.get_tags()

st.set_page_config(page_title="ClickUp Article Saver", page_icon="💾", layout="wide")
st.title("Save articles to knowledge base")

with st.form(key="Article Creation Form", clear_on_submit=True):
    article_name = st.text_input(
        label="Title", placeholder="Title of the article you want to save."
    )

    article_description = st.text_input(
        label="Description",
        placeholder="(Optional) Description of the article you want to save.",
    )

    article_url = st.text_input(
        label="URL", placeholder="URL of the article you want to save."
    )

    selected_tags = st.multiselect(
        label="Tags",
        options=[tag.name for tag in tags],
        help="Select all the relevant tags.",
    )

    submitted = st.form_submit_button("Save article")
    if submitted:
        try:

            if any(yt_link in article_url for yt_link in ["youtube", "youtu.be"]) and (
                "video" not in selected_tags
            ):
                selected_tags.append("video")
            elif ("twitter" in article_url) and ("twitter" not in selected_tags):
                selected_tags.append("twitter")

            saved_articles_list.create_task(
                Task(
                    name=article_name,
                    description=article_description,
                    status="To Read",
                    tags=selected_tags,
                    custom_fields=Task.custom_fields(
                        [{"name": "URL", "value": article_url}]
                    ),
                )
            )
            st.balloons()
            st.success(body="Article saved!", icon="✅")
        except Exception as e:
            st.error(body=str(e), icon="❗")
