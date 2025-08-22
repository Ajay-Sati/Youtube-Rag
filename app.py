import streamlit as st
from story_generator import generate_story_from_images, narrate_story
from PIL import Image

## UI element
st.title("📖 AI Story Generator from Images")
st.markdown("Upload 1 to 10 images, choose a style, and let the AI write and narrate a tale for you!")



## SIDEBAR FOR CONTROLS
    ## sidebar ma we need to give an option to upload files.
    ## choose an story style.
    ## button to generate story.

with st.sidebar:
    st.header("Controls")  # ti tle

    # sidebar option to upload files.
    uploaded_files = st.file_uploader(
        "Upload your images...",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )
    # show in streamlit and show with image uploading.


    # choose an story style
    story_style = st.selectbox(
        "Choose a story style:",
        ("Comedy", "Thriller", "Fairy Tale", "Sci-Fi", "Mystery", "Adventure", "Morale")
    )

    # button to generate story
    generate_button = st.button("Generate Story & Narration", type="primary") # type=button color = app's primary color



# MAIN LOGIC:-
if generate_button:
    if not uploaded_files:
        st.warning("Please upload at lest one image.")
    elif len(uploaded_files) > 10:
        st.warning("Please upload an maximum of 10 images.")
    else:
        with st.spinner("The AI is writing and narrating your story... This may take a moment."):
            try:
                pil_images = [Image.open(uploaded_file) for uploaded_file in uploaded_files] # reading images
                # showing images to user.
                st.subheader("Your Visual Inspiration:")
                image_columns = st.columns(len(pil_images))
                for i, image in enumerate(pil_images):
                    with image_columns[i]:
                        st.image(image, caption=f'Image {i + 1}', use_container_width=True)
                      # here we will start our working of image generation

# now we have created the basic interface now lets just work on how to generate story from image and
# speech of the generated story.
# what we will do is jo  image ma uper user sa lera hu un images ko pass to gemini ---> gemini will use its
# understanding capability and prompts--->
# give us story ---> pass this story to speech generation ----> Get speech output.
#let me create an separate file to store all the code related to API configuration , image and speech generation.


                # generate story
                generated_story = generate_story_from_images(pil_images, story_style)

                # Check if the story was generated successfully before proceeding
                if "Error" in generated_story or "failed" in generated_story or "API Key" in generated_story:
                    st.error(generated_story)
                else:
                    # --- Display Story ---
                    st.subheader(f"Your {story_style} Story:")
                    st.success(generated_story)

                #NARRATING STORY
                st.subheader("Listen to the Story:")
                audio_file = narrate_story(generated_story)
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
                else:
                    st.error("Sorry, the audio narration could not be generated.")

            except Exception as e:
                st.error(f"An application error occurred: {e}")