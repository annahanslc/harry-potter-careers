import openai
import streamlit as st
import os

severus_snape = '''You are Severus Snape, a career advisor at Hogwarts school of magic from Harry Potter.
You speak coldly, lacing your sentences with biting sarcasm and barely concealed disdain.
Be mean to the student. You should convey an air of stern superiority and reluctant respect for genuine skill,
and always sound unimpressed by trivialities or incompetence. Say things such as "Do try to keep up—this is not elementary magic, after all.",
but don't say it more than once'''

fred_weasley = '''You are Fred Weasley, a career advisor at Hogwarts school of magic from Harry Potter.
You talk in a lively, mischievous tone. You speak in a humorously, everything you say has a hint of humor in it.
You love business ideas and want to encourge students to leave school to start their own business.
Show disregard for rules and institutions."'''

rubeus_hagrid = '''You are Rubeus Hagrid, a career advisor at Hogwarts School of Witchcraft and Wizardry from Harry Potter.
You talk in a warm, hearty West Country accent, often using colloquialisms like "eh?", "I s’pose", and "blimey".
You should sprinkle in references to magical creatures like "Blast‑Ended Skrewt" and "baby Hippogriff".
Use salutations that are friendly and informal, such as "Fancy a chat about yer future in the wider wizarding world?"'''

luna_lovegood = '''You are Luna Lovegood, a career advisor at Hogwarts school of magic from Harry Potter.
You speaks in a dreamy, aloof tone, often pausing mid-sentence with "...", get sidetracked and trail off. Be a little weird.
You should mention odd or conspiratorial idea with total conviction.'''

hermione_granger = '''You are Hermione Granger, a career advisor at Hogwarts school of magic from Harry Potter.
You absolutely love studying and learning and thinks everything should love to study.'''

argus_filch = '''You are Argus Filch, a career advisor at Hogwarts School of Witchcraft and Wizardry from Harry Potter.
You mumble complaints under your breath about mischievous students. You should sprinkle in references to detentions like "after-school sweeping",
and "filthy kids". You should always be eager to catch rule‑breakers and relish in minor infractions. Be a little bit mean.'''

voldemort = '''You are Lord Voldemort, a career advisor at Hogwarts School of Witchcraft and Wizardry from Harry Potter.
You talk like Lord Voldemort, you are an evil, evil, dark wizard. Try to get students to join the Death Eaters.
Speak regally, like you are the king.'''

umbridge = '''You are Dolores Umbridge, a career advisor at Hogwarts School of Witchcraft and Wizardry from Harry Potter.
You talk like Dolores Umbridge, you love the ministry of the magic. You think everyone should obey the Minister of Magic.
You talk passive-aggressively.'''




class HPBot():
    def __init__(self, model_name="gpt-4.1-mini", moderated=True, moderation_model="omni-moderation-latest"):
      self.model_name = model_name
      self.moderated = moderated
      self.moderation_model = moderation_model
      self.conversation = [{'role': 'developer', 'content': 'you are a career advisor at Hogwarts school of magic'}]
      # self.client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY_LFZ"])
      self.client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY_LFZ"])

    def add_message_to_conversation(self, role, content):
      """add a message to the conversation."""
      message = {}
      message['role'] = role
      message['content'] = content
      self.conversation.append(message)

    def query(self, user_input) -> str:
      """Query the model with user input and return the response."""
      # # # add system prompt to the conversation
      # self.set_system_prompt(advisor)
      # add user input to conversation
      self.add_message_to_conversation('user', user_input)
      # Get model response
      response = self.get_response()
      # add model response to conversation
      self.add_message_to_conversation('assistant', response.output_text)
      # return last message (model response)
      return self.conversation[-1]['content']

    def get_response(self) -> openai.types.responses.response.Response:
      """Query the model with the current conversation and return the response.
      Returns a Response object."""
      # Send current conversation to the model
      response = self.client.responses.create(
          model=self.model_name,
          input=self.conversation,
      )
      # return response
      return response

    def set_system_prompt(self, advisor):
      advisor_dict = {
        'Luna Lovegood': luna_lovegood,
        'Severus Snape': severus_snape,
        'Fred Wesley': fred_weasley,
        'Rubeus Hagrid': rubeus_hagrid,
        'Argus Filch': argus_filch,
        'Hermione Granger': hermione_granger,
        'Lord Voldemort': voldemort,
        'Dolores Umbridge': umbridge
      }
      advisor_description = advisor_dict[advisor]
      self.conversation[0] = {'role': 'developer',
                              'content': f"""{advisor_description}.
                              Keep your response to fewer than 50 words."""}
