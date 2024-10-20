import streamlit as st

def page_config():
    st.set_page_config(
        page_title="Shinninkai Karate Tools",
        page_icon="🥋"
        )
    
    st.title("Shinninkai Karate Tools")
    st.write("Welcome to the Shinninkai Karate Tools. This is a collection of tools to help you with your karate training. Please select a tool from the sidebar to get started.")

def main():
    page_config()

if __name__ == "__main__":
    main()