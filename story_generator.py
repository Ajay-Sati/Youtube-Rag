# CONFIGURING  API KEY
#to configure the api, I first need to read the .env file and get data from there, and then  configure it
# we use python-dotenv library there we have load_dotenv function , we will use it.

# show library in requirements.txt , install using pip install -r requirements.txt.

# import function from the library.
from dotenv import load_dotenv

load_dotenv() # this command will read data from .env file , now let's configure it

# to configure we need to import  os module too
import os
from google import genai  # to config gen AI
from google.genai import types

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API Key not found in .env file.")

#configuring the client
client = genai.Client(api_key=api_key)

#JUST TO CHECK IS API IS CONFIGURED PROPERLY OR NOT,
# response = client.models.generate_content(
#     model='gemini-2.5-flash-lite',
#     contents='What is a car? Explain in 400 words.')
#print(response.text)



def create_advanced_prompt(style: str) -> str:

    # --- Base prompt ---
    base_prompt = f"""
    **Your Persona:** You are a friendly and engaging storyteller. Your goal is to tell a story that is fun and easy to read.
    **Your Main Goal:** Write a story in simple, clear, and modern English.
    **Your Task:** Create one single story that connects all the provided images in order.
    **Style Requirement:** The story must fit the '{style}' genre.
    **Core Instructions:**
    1.  **Tell One Single Story:** Connect all images into a narrative with a beginning, middle, and end.
    2.  **Use Every Image:** Include a key detail from each image.
    3.  **Creative Interpretation:** Infer the relationships between the images.
    4.  **Nationality**: Use only Indian Names,Characters, Places , Persona Etc.
    **Output Format:**
    -   **Title:** Start with a simple and clear title.
    -   **Length:** The story must be between 4 and 5 paragraphs.
    """

    # --- Add Style-Specific Instructions ---
    style_instruction = ""
    if style == "Morale":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[MORAL]:` followed by the single-sentence moral of the story."
    elif style == "Mystery":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[SOLUTION]:` that reveals the culprit and the key clue."
    elif style == "Thriller":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[TWIST]:` that reveals a final, shocking twist."

    return base_prompt + style_instruction



#API IS CONFIGURED PROPERLY ,
# NOW LETS CREATE AN FUNCTION THAT WE WILL CALL IN OUR MAIN  FILE(APP.PY)
def generate_story_from_images(images, style):
    if not (1<= len(images)<=10):
        return "Validation error : Please provide  between 1  and 10 images."

    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        # contents=[images,'Write an short story about the images'])
        contents=[images, create_advanced_prompt(style)])
    return response.text




# function to generate speech out of it.
from gtts import gTTS
from io import BytesIO

def narrate_story(story_text):
    try:
        tts = gTTS(text=story_text, lang='en', slow=False)# Creates a Google Text-to-Speech (gTTS) object.
                                     #speaks at normal speed, if true speaks at faster speed.
        audio_fp = BytesIO() # Makes a temporary “file” to store audio but nothing is saved to your hard drive.
        tts.write_to_fp(audio_fp) # Converts the text into speech audio and stores the MP3 data directly into audio_fp
        audio_fp.seek(0)  # Moves the file pointer back to the start of the BytesIO object.
        # This is necessary so that when you later read/play the file, it starts from the beginning rather than the end.
        return audio_fp
    except Exception as e:
        error_msg = f"An unexpected error occurred during the API call: {e}"
        return error_msg
