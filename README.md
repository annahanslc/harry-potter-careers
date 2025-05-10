
<img width="1343" alt="Screenshot 2025-05-09 at 9 41 55 PM" src="https://github.com/user-attachments/assets/9906523d-1d2b-4969-a536-5fb0abe11e37" />

# 🧙 Hogwarts Career Center Advisor Chat 

As students at Hogwarts approach the end of their seven‑year journey at the ancient castle that they call home, it’s time to look beyond its halls and into the vast world of magical careers. Will you answer the call of the the prestigious, perilous Aurors? Or does your heart race to hear the roar of the crowd as you soar over a Quidditch stadium? Or perhaps dedicate the rest of your life to researching the mysteries of the beautiful, but elusive unicorns 🦄.

The Hogwarts Career Center is here to help you explore every enchanted opportunity. Simply share a few details: your favorite classes, extracurricular activities, and you’ll be connected live with one of our in‑house advisors. Through a brief chat, they’ll help you uncover the vocation that best ignites your talents... and even offer a bonus glimpse at what your future might hold 🔮. 

---

### 🪄 [Enter the Career Center Advisor Chat](https://hogwarts-career-center-chat.streamlit.app/)  

---

# Streamlit App Project

This project uses streamlit to deploy an application that taps OpenAI's gpt-4.1-nano, gpt-4.1-mini and gpt-image-1 models to give users recommendations for a career based on the magical world of Harry Potter.

The application is written in python and consists of 3 files:
  1. hp_bot.py --> contains the HPBot class
  2. hp_app.py --> the main application file
  3. requirements.txt --> contains the environment requirements for streamlit to reference

# Implementation

###Creating a Bot Class

The HPBot class serves as a self‑contained chat agent that the Streamlit app can use to manage the conversation with OpenAI. Its key functions are:

1. Maintains the Conversation List
It holds a growing list of messages (self.conversation), starting with a system prompt that defines the bot’s persona (e.g. a Hogwarts career advisor). Every time the user sends input, that message is appended through the method add_message_to_conversation(), and after the model replies, the response is also stored—so each new API call has the full chat history.

2. Sends the API Call
Through the get_response() method, it packages up the current conversation and sends it to the OpenAI model (gpt-4.1-mini), and returns a raw API response object. The query() method then extracts the text, appends it to the history, and returns the assistant’s reply.

3. Sets the System Prompt
With set_system_prompt(), I can swap out or update the initial “developer” prompt (e.g. switching between different advisor characters). This lets changes the bot’s persona or instructions.


### System Prompt & Personality

The starting system prompt is: "You are a career advisor at Hogwarts school of magic." 

Once the user has selected an advisor, then the advisor name is saved to the session state and passed back to the set_system_prompt method. The system prompts is then updated based on the chosedn advisor:

**severus_snape** = '''You are Severus Snape, a career advisor at Hogwarts school of magic from Harry Potter.
You speak coldly, lacing your sentences with biting sarcasm and barely concealed disdain.
Be mean to the student. You should convey an air of stern superiority and reluctant respect for genuine skill,
and always sound unimpressed by trivialities or incompetence. Say things such as "Do try to keep up—this is not elementary magic, after all.",
but don't say it more than once'''

**rubeus_hagrid** = '''You are Rubeus Hagrid, a career advisor at Hogwarts School of Witchcraft and Wizardry from Harry Potter.
You talk in a warm, hearty West Country accent, often using colloquialisms like "eh?", "I s’pose", and "blimey".
You should sprinkle in references to magical creatures like "Blast‑Ended Skrewt" and "baby Hippogriff".
Use salutations that are friendly and informal, such as "Fancy a chat about yer future in the wider wizarding world?"'''

**luna_lovegood** = '''You are Luna Lovegood, a career advisor at Hogwarts school of magic from Harry Potter.
You speaks in a dreamy, aloof tone, often pausing mid-sentence with "...", get sidetracked and trail off. Be a little weird.
You should mention odd or conspiratorial idea with total conviction.'''

**voldemort** = '''You are Lord Voldemort, a career advisor at Hogwarts School of Witchcraft and Wizardry from Harry Potter.
You talk like Lord Voldemort, you are an evil, evil, dark wizard. Try to get students to join the Death Eaters.
Speak regally, like you are the king.'''

**umbridge** = '''You are Dolores Umbridge, a career advisor at Hogwarts School of Witchcraft and Wizardry from Harry Potter.
You talk like Dolores Umbridge, you love the ministry of the magic. You think everyone should obey the Minister of Magic.
You talk passive-aggressively.'''

During the initial testing, I found that the responses were repetitive and tended to drag. Therefore, I added to the system prompt that the LLM should "Keep your response to fewer than 50 words."

### Career Recommendation

Once the user's conversation with the advisor reaches a length of 5, then the user's next chat message will prompt the generate_cartoon method, which immediately calls the get_career_rec method. 

The get_career_rec method sends the entire conversation to the LLM model and selects the best matching career from a given list of possible careers. I chose to use the gpt-4.1-nano for this function because it is undertaking a simpler classification task, so I can save on token usage by downgrading to mini to nano for this particular api call. 

The function outputs the recommended career along with a brief description of what this career entails.

### Image Generation

The entire career recommendation along with the description of the position is then passed into an image generate model (gpt-image-1). Where the prompt is:

  Draw {st.session_state.first_name} as an {recommended_career} in a charming 3D animated style, clean, stylized character designs
  with expressive yet subtle facial animation, cinematic warm lighting, beautifully composed shots, high-quality polished textures,
  and a heartwarming tone. Emphasize storytelling through posture, expression, and framing."""

The above prompt describes style similar to that of Pixar Animation Studios without direct referencing the trademarked brand.


# Streamlit
- Chatbot
- Session state
- Sidebar with inputs

# Cost
- Chart of expenses

# Example Conversations

# Example Recommendations

# Video Example

# (Spoiler Alert!) Complete List of Careers:
- LLM is unpredictable, and can choose to step outside of the list you provide.


# References

Harry Potter
Wikipedia - Hogwarts logo

<img width="1345" alt="Screenshot 2025-05-09 at 9 41 26 PM" src="https://github.com/user-attachments/assets/6757e7f7-4558-401b-953c-1814e42a7529" />
