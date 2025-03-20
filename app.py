import streamlit as st
import openai
import requests
import json
from youtube_transcript_api import YouTubeTranscriptApi

# Set API Keys
YOUTUBE_API_KEY = "AIzaSyCuUYGZTNiXccQSobvlPlSInOAmcViDhvc"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Function to extract video ID
def get_video_id(url):
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    return None

# Function to get transcript
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        full_text = " ".join([t['text'] for t in transcript])
        return full_text
    except Exception as e:
        return None

# Function to summarize text
def summarize_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize this text in simple Urdu language."},
                {"role": "user", "content": text}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "Summarization failed. Error: " + str(e)

# Streamlit UI
st.title("YouTube Video Urdu Summary Tool")
st.write("Paste a YouTube video link and get a summary in Urdu!")

video_url = st.text_input("Enter YouTube Video URL:")
if st.button("Generate Summary"):
    if video_url:
        video_id = get_video_id(video_url)
        if video_id:
            transcript = get_transcript(video_id)
            if transcript:
                summary = summarize_text(transcript)
                st.subheader("Summary in Urdu:")
                st.write(summary)
            else:
                st.error("Transcript not available for this video.")
        else:
            st.error("Invalid YouTube URL.")
    else:
        st.error("Please enter a YouTube video URL.")
