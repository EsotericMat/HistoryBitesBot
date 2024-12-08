import wikipedia
import re
from datetime import datetime


def get_events():
    today_string = datetime.now().strftime("%B %d")
    text = wikipedia.page(today_string).content
    return text


def extract_events_and_births(text):
    # Define regex patterns to capture events and births by their respective section headers
    events_pattern = r'==\s*Events\s*==.*?(?==\s*(Births|Deaths)\s*==)'
    births_pattern = r'==\s*Births\s*==.*?(?==\s*(Events|Deaths)\s*==)'

    # Use regex to find the events and births sections
    events_section = re.search(events_pattern, text, re.DOTALL)
    births_section = re.search(births_pattern, text, re.DOTALL)

    # Extract individual events and births
    if events_section:
        # Extract events
        events = re.findall(r'^\d{4}\s*–\s*.*', events_section.group(), re.MULTILINE)
    else:
        events = []

    if births_section:
        # Extract births
        births = re.findall(r'^\d{4}\s*–\s*.*', births_section.group(), re.MULTILINE)
    else:
        births = []

    return events, births
