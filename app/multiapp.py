import streamlit as st
from apps.user_engagement_analysis import app as engagement_app
from apps.user_experience_analysis import app as experience_app
from apps.user_satisfaction_analysis import app as satisfaction_app

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        app = st.sidebar.selectbox("Select Analysis", self.apps, format_func=lambda app: app['title'])
        app['function']()

# Create the app
multi_app = MultiApp()

# Add all your apps here
multi_app.add_app("User Engagement Analysis", engagement_app)
multi_app.add_app("User Experience Analysis", experience_app)
multi_app.add_app("User Satisfaction Analysis", satisfaction_app)

# Run the app
multi_app.run()