import openai
import os

class Chatbot:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_response(self, user_input):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    
    def extract_event_details(self, response):
        # Dummy function to extract event details from the response
        event_details = {}

        try:
            parts = response.split(';')
            event_details = {
                "summary": parts[0].split(":")[1].strip(),
                "start_time": parts[1].split(":")[1].strip(),
                "end_time": parts[2].split(":")[1].strip(),
            }
        except Exception as e:
            print(f"Error parsing response: {e}")

        return event_details