import streamlit as st
from hp_bot import HPBot
from openai import OpenAI
import base64

# access api key saved in streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY_LFZ"])

# for local testing
# import os
# client = OpenAI(api_key=os.environ["OPENAI_API_KEY_LFZ"])

# check for the SuperBot state, if new session, then initiate bot.
if 'bot' not in st.session_state:
  # if not there, then create the SuperBot
  st.session_state.bot = HPBot()

# create a function to update session states with variables obtained from user inputs
def update_inputs():
  st.session_state.first_name = first_name
  st.session_state.advisor = advisor
  st.session_state.favorite_subject = favorite_subject
  st.session_state.extracurricular = extracurricular

# create a function to update the set system prompt function with the advisor name
def update_advisor():
  st.session_state['bot'].set_system_prompt(st.session_state.advisor)

# create a function to clear the chat conversation
def clear_chat():
  st.session_state['bot'].conversation = [{'role': 'developer', 'content': f'you are {st.session_state.advisor}, a career advisor at Hogwarts school of magic'}]

# create a function to initiate the chat and call necessary functions
def start_chat():
  # if there is an existing chat, then clear the chat first
  if len(st.session_state.bot.conversation) > 1:
    clear_chat()
  update_inputs()
  update_advisor()
  st.session_state.initiate = f"""
        My name is {st.session_state.first_name},
        my favorite subjects are {st.session_state.favorite_subject}, and my
        extracurricular activities include {st.session_state.extracurricular}.
        """
  st.session_state['bot'].query(st.session_state.initiate)

# create a function to have the LLM recommend a career based on the chat conversation so far
def get_career_rec():
  career_list = ['Auror', 'Magical Law Enforcement Squad', 'Wizard Judge / Clerk',
    'Minister of Magic', 'Professor at School of Magic', 'Healer at Hospital for Magical Maladies and Injuries',
    'Wandmaker', 'Broommaker', 'Potions Master', 'Butterbeer Brewer', 'Reporter for the Magical Newspaper',
    'Magical Creatures Photographer', 'Dragon Handler', 'Professional Quidditch Player'
    'SPEW (Society for the Promotion of Elfish Welfare) Lobbyist',
    'Bank Teller', 'Cauldron Quality Inspector', 'Translator of Ancient Magical Texts',
    'Chocolate Frog Patisserie', 'Emergency Troll Removal Squad', 'Unicorn Tracker']
  response = client.responses.create(
    model='gpt-4.1-nano',
    input=[{'role': 'developer',
           'content': f"""Based on this conversation: {st.session_state.bot.conversation[2:]}, pick the the wizarding career from the
           following list of possible careers: {career_list} that best fits the student . Tell the student which career you recommend
           and give a brief description. For example, if the recommended career is "Auror", then your response would be
           "I recommend that you become an Auror - a highly trained wizard or witch employed by the Ministry of Magic’s
           Department of Magical Law Enforcement. Their duties include investigating and apprehending Dark wizards,
           dismantling dark artifacts, and protecting the magical community from threats. Aurors undergo rigorous training in advanced defensive and
           offensive spells—such as Stunning Charms, Disarming Charms, and Counter‑Curses—and must demonstrate exceptional skill, courage, and discretion in the field."
           At the end of your recommendation ask the student to wait 1-2 minutes as their picture is being generated...
           """}]
  )
  return response.output_text

# create a function to generate the image
def generate_cartoon():
  recommended_career = get_career_rec()
  st.write(recommended_career)

  # prompt for image generation, prompt is designed to output pixar-like image without directly referencing it.
  prompt= f"""
  Draw {st.session_state.first_name} as an {recommended_career} in a charming 3D animated style, clean, stylized character designs
  with expressive yet subtle facial animation, cinematic warm lighting, beautifully composed shots, high-quality polished textures,
  and a heartwarming tone. Emphasize storytelling through posture, expression, and framing."""

  result = client.images.generate(
    model='gpt-image-1',
    prompt=prompt,
    size="1024x1024",
    background='transparent',
    quality='low'
  )
  image_base64 = result.data[0].b64_json
  image_bytes = base64.b64decode(image_base64)

  st.session_state.image = True
  return image_bytes

# create a function to pass in the chat prompt into the query
def query_bot():
  if len(st.session_state.bot.conversation) > 5:
    pronoun_dict = {'Severus Snape': 'he', 'Luna Lovegood': 'she', 'Rubeus Hagrid': 'he', 'Lord Voldemort': 'he', 'Dolores Umbridge': 'she'}
    with st.spinner(f"""
                    Suddenly, {st.session_state.advisor} freezes, and shivers as if entering a trance...
                    it looks like {pronoun_dict[st.session_state.advisor]} is having a vision about your wizarding career... """):
      st.image(generate_cartoon(), width=500)
      clear_chat()
  else:
    with st.spinner(f"{st.session_state.advisor} is pondering over your message..."):
      response = st.session_state['bot'].query(st.session_state.prompt)
    return response

# create a sidebar to house all the initial user inputs
with st.sidebar:
  # get the Hogwarts logo
  st.image('https://upload.wikimedia.org/wikipedia/commons/d/d4/Hogwarts-Crest.png?20210328175300', width=100)
  st.title("Hogwarts Career Center: Chat with an Advisor")

  st.header("Tell the advisor about yourself.")

  first_name = st.text_input("What is your first name?")
  st.divider()
  st.subheader('Who is your Career Advisor?')
  advisor = st.radio('Select your Career Advisor\'s name.',
                    ['Severus Snape', 'Luna Lovegood', 'Rubeus Hagrid', 'Lord Voldemort', 'Dolores Umbridge'])
  st.divider()
  st.subheader('What is your favorite subject?')
  favorite_subject = st.selectbox('Select your favorite subject', ('None', 'Transfiguration', 'Charms', 'Potions', 'History of Magic',
                                                                    'Defense Against the Dark Arts', 'Astronomy', 'Herbology'))
  st.divider()
  st.subheader('What extracurricular activities do you participate in?')

  extracurricular = {}
  extracurricular['quidditch team'] = st.checkbox("House Quidditch Team")
  extracurricular['dueling club'] = st.checkbox("Dueling Club")
  extracurricular['dumbledore army'] = st.checkbox("Dumbledore's Army (the DA)")
  extracurricular['wizard chess club'] = st.checkbox("Wizard Chess Club")
  extracurricular['leadership roles'] = st.checkbox("Leadership roles (e.g. Prefect)")

  extracurricular_list = [key for key, value in extracurricular.items() if value]

  st.divider()
  st.write("""Chat with your advisor 3 times to get your career recommendation and a picture of your future self.""")
  st.button("Chat with Advisor", on_click=start_chat)

#
if st.session_state.image == True:
  st.write('Thank you for visiting the Hogwarts Career Center. May your ambitions soar higher than a Nimbus 2000!')
else:
  st.chat_input("Talk to the bot here", key="prompt", on_submit=query_bot)

# create a new function to show the messages in the conversation
def show_messages():
  for message in st.session_state.bot.conversation[2:]:
    # can use the special chat message object to save the messages
    # each item is a dictionary
    if message['role'] == 'assistant':
      icon_dict = {'Severus Snape': '🤨', 'Luna Lovegood': '👩🏼', 'Rubeus Hagrid': '🧔🏻‍♂️', 'Lord Voldemort': '👽', 'Dolores Umbridge': '👵'}
      icon = icon_dict[st.session_state.advisor]
    if message['role'] == 'user':
      icon = '🧑‍🎓'
    with st.chat_message(message['role'], avatar=icon):
      if message['role'] is not 'developer':
        # markdown will allow emoji and boldings, etc.
        st.markdown(message['content'])


show_messages()
