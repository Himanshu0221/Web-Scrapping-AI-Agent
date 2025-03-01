import streamlit as st
from scrapegraphai.graphs import SmartScraperGraph
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables
load_dotenv()

# Set up the Streamlit app
st.title("Web Scraping AI Agent 🕵️‍♂️")
st.caption("This app allows you to scrape a website using OpenAI API")

# Retrieve OpenAI API Key from .env file
openai_access_token = os.getenv("OPENAI_API_KEY")

if openai_access_token:
    model = st.radio(
        "Select the model",
        ["gpt-3.5", "gpt-4"],
        index=0,
    )
    
    graph_config = {
        "llm": {
            "api_key": openai_access_token,
            "model": model,
            "provider": "openai",  # Explicitly set provider
        },
    }
    
    # Get the URL of the website to scrape
    url = st.text_input("Enter the URL of the website you want to scrape")
    user_prompt = st.text_input("What do you want the AI agent to scrape from the website?")
    
    if url and user_prompt:
        smart_scraper_graph = SmartScraperGraph(
            prompt=user_prompt,
            source=url,
            config=graph_config
        )
        
        # Scrape the website
        if st.button("Scrape"):
            with st.spinner("Scraping in progress..."):
                try:
                    # Test Playwright in headless mode
                    with sync_playwright() as p:
                        browser = p.chromium.launch(headless=True)
                        page = browser.new_page()
                        page.goto(url)
                        st.write("Page title:", page.title())
                        browser.close()
                    
                    # Run AI scraper
                    result = smart_scraper_graph.run()
                    st.success("Scraping completed successfully!")
                    st.write(result)
                except Exception as e:
                    st.error(f"Error occurred: {e}")
    else:
        st.warning("Please enter both a valid URL and a prompt before scraping.")
else:
    st.error("API key not found. Please ensure your .env file contains OPENAI_API_KEY.")
