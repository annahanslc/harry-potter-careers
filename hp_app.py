import streamlit as st
from hp_bot import HPBot

if 'bot' not in st.session_state:
  # if not there, then create the SuperBot
  st.session_state.bot = HPBot()

expander = st.expander("Student Questionnaire", expanded=True)

# def ask_questions():
with expander:
  st.header('Welcome to the Hogwarts Career Center')
  first_name = st.text_input("Enter your first name:")
  st.divider()
  st.subheader('Who is your Career Advisor?')
  advisor = st.radio('Select your Career Advisor\'s name.',
                    ['Hermione Granger', 'Luna Lovegood', 'Severus Snape', 'Fred Wesley', 'Rubeus Hagrid', 'Argus Filch'])
  st.divider()
  st.subheader('What is/are your favorite core subject(s)?')
  favorite_class = st.multiselect('Select your favorite subject', ['Transfiguration', 'Charms', 'Potions', 'History of Magic',
                                                                            'Defense Against the Dark Arts', 'Astronomy', 'Herbology'])
  st.divider()
  st.subheader('What extracurricular activities do you participate in?')

  extracurricular = {}
  extracurricular['quidditch team'] = st.checkbox("House Quidditch Team")
  extracurricular['dueling club'] = st.checkbox("Dueling Club")
  extracurricular['dumbledore army'] = st.checkbox("Dumbledore's Army (the DA)")
  extracurricular['the slug club'] = st.checkbox("The Slug Club")
  extracurricular['wizard chess club'] = st.checkbox("Wizard Chess Club")
  extracurricular['leadership roles'] = st.checkbox("Leadership roles (e.g. Prefect)")
  extracurricular['animal care volunteer'] = st.checkbox("Animal-Care Volunteer")

  extracurricular_list = [key for key, value in extracurricular.items() if value]




def test_function():
  expander.expanded = False
  container = st.container(border=True)

  container.write(f'{st.session_state.first_name}')
  container.write(f'{st.session_state.advisor}')
  container.write(f'{st.session_state.favorite_class}')
  container.write(f'{st.session_state.extracurricular}')


# don't need to pass in anything, because we will just grab it from the session_state
def query_bot():
  response = st.session_state['bot'].query(st.session_state.prompt)
  # add the moderator to prevent inappropriate messages
  if st.session_state['bot'].moderate(st.session_state.prompt):
    st.write(response)

# create a new function to show the messages in the conversation
def show_messages():
  for message in st.session_state.bot.conversation[1:]:
    # can use the special chat message object to save the messages
    # each item is a dictionary
    with st.chat_message(message['role']):
      if message['role'] is not 'developer':
        # markdown will allow emoji and boldings, etc.
        st.markdown(message['content'])

def update_char():
  st.write("update char")

# the key will allow its value to be saved in the session state under that key
advisor_consulted = st.button(label="Talk to your Advisor", on_click=update_char)

# start_page()

show_messages()

if advisor_consulted:
  st.chat_input("Talk to the bot here", key="prompt", on_submit=query_bot)
