import streamlit as st
import os
from hp_bot import HPBot
from openai import OpenAI
import base64

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY_LFZ"])
# client = OpenAI(api_key=os.environ["OPENAI_API_KEY_LFZ"])


if 'bot' not in st.session_state:
  # if not there, then create the SuperBot
  st.session_state.bot = HPBot()


def update_inputs():
  st.session_state.first_name = first_name
  st.session_state.advisor = advisor
  st.session_state.favorite_subject = favorite_subject
  st.session_state.extracurricular = extracurricular

def update_advisor():
  st.session_state['bot'].set_system_prompt(st.session_state.advisor)

# create a function to clear the chat conversation
def clear_chat():
  st.session_state['bot'].conversation = [{'role': 'developer', 'content': 'you are a career advisor at Hogwarts school of magic'}]

def start_chat():
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


def generate_cartoon():
  prompt= f"""
  Draw a cute cartoon depicting {st.session_state.first_name}
  in the wizarding career as described in this conversation:
  {st.session_state.bot.conversation[2:]}"""

  result = client.images.generate(
    model='gpt-image-1',
    prompt=prompt,
    size="1024x1024",
    background='transparent',
    quality='low'
  )
  image_base64 = result.data[0].b64_json
  image_bytes = base64.b64decode(image_base64)
  return image_bytes


def query_bot():
  if len(st.session_state.bot.conversation) > 4:
    with st.spinner(f"""
                    Suddenly, {st.session_state.advisor} freezes, and shivers as if entering a trance...
                    it looks like he is having a vision about your wizarding career... please wait..."""):
      st.image(generate_cartoon(), width=400)
      clear_chat()
  else:
    with st.spinner(f"{st.session_state.advisor} is pondering over your message..."):
      response = st.session_state['bot'].query(st.session_state.prompt)
    return response


with st.sidebar:
  st.image('https://upload.wikimedia.org/wikipedia/commons/d/d4/Hogwarts-Crest.png?20210328175300', width=100)
  st.title("Hogwarts Career Center: Chat with an Advisor")

  st.header("Tell the advisor about yourself.")

  first_name = st.text_input("Enter your first name:")
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


  st.button("Start Chat with Advisor", on_click=start_chat)


st.chat_input("Talk to the bot here", key="prompt", on_submit=query_bot)

# create a new function to show the messages in the conversation
def show_messages():
  for message in st.session_state.bot.conversation[2:]:
    # can use the special chat message object to save the messages
    # each item is a dictionary
    if message['role'] == 'assistant':
      icon_dict = {'Severus Snape': '🤨', 'Luna Lovegood': '👩🏼', 'Rubeus Hagrid': '🧔🏻‍♂️', 'Lord Voldemort': '👽', 'Dolores Umbridge': '🪶'}
      icon = icon_dict[st.session_state.advisor]
    if message['role'] == 'user':
      icon = '🪄'
    with st.chat_message(message['role'], avatar=icon):
      if message['role'] is not 'developer':
        # markdown will allow emoji and boldings, etc.
        st.markdown(message['content'])


show_messages()
