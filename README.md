
<img width="1345" alt="Screenshot 2025-05-09 at 9 41 12 PM" src="https://github.com/user-attachments/assets/1131accb-c69f-48a6-ad56-62785971aaa5" />

# 🧙 Hogwarts Career Center Advisor Chat 

As your seventh and final year at Hogwarts draws to a close, it’s time to step beyond these ancient halls and explore the extraordinary careers awaiting you in the wizarding world. Will you answer the call of the the prestigious, perilous Aurors? Or does your heart race to hear the roar of the crowd as you soar over a Quidditch stadium? Or perhaps dedicate the rest of your life to researching the mysteries of the beautiful, but elusive unicorns 🦄.

The Hogwarts Career Center is here to help you explore every enchanted opportunity. Simply share a few details: your favorite classes, extracurricular activities, and you’ll be connected live with one of our in‑house advisors. Through a brief chat, they’ll help you uncover the vocation that best ignites your talents... and even offer a bonus glimpse at what your future might hold 🔮. 

---

### [⚡️🔮🌟🪄✨⚡️🔮🌟🪄✨ Enter the Career Center Advisor Chat ✨🪄🌟🔮⚡️✨🪄🌟🔮⚡️](https://hogwarts-career-center-chat.streamlit.app/)

---

# Streamlit App Project

The Hogwarts Career Center is an interactive Streamlit app that uses OpenAI’s API to guide students through choosing a magical careers, and even generates a personalized image of them in that role. Built with object‑oriented design and session management, it implements AI integrations in a modern, user‑friendly UI.

The codebase is organized into three files:

  - hp_bot.py: Defines the HPBot class, which encapsulates prompt management, conversation history, and API interactions.

  - hp_app.py: Implements the Streamlit front end—sidebar inputs, chat interface, and callbacks—to drive the user experience.

  - requirements.txt: Lists the Python dependencies (Streamlit, OpenAI SDK, etc.) needed to run the application.


# Implementation

### Creating a Bot Class 🤖

The HPBot class serves as a self‑contained chat agent that the Streamlit app can use to manage the conversation with OpenAI. Its key functions are:

1. Maintains the Conversation List - It holds a growing list of messages (self.conversation), starting with a system prompt that defines the bot’s persona (e.g. a Hogwarts career advisor). Every time the user sends input, that message is appended through the method add_message_to_conversation(), and after the model replies, the response is also stored—so each new API call has the full chat history.

2. Sends the API Call - Through the get_response() method, it packages up the current conversation and sends it to the OpenAI model (gpt-4.1-mini), and returns a raw API response object. The query() method then extracts the text, appends it to the history, and returns the assistant’s reply.

3. Sets the System Prompt - With set_system_prompt(), swap out or update the initial “developer” prompt (e.g. switching between different advisor characters). This changes the bot’s persona or instructions.


### System Prompt & Personality 🕺

At the outset, the bot begins with a default system prompt: “You are a career advisor at Hogwarts School of Magic”, which establishes its overall role and tone. 

As soon as a user selects a specific advisor persona in the sidebar and initiates the chat, that choice is recorded in session state and passed into the set_system_prompt method.  The system prompts is then updated based on the chosen advisor:

🤨 **severus_snape** = '''You are Severus Snape, a career advisor at Hogwarts school of magic from Harry Potter.
You speak coldly, lacing your sentences with biting sarcasm and barely concealed disdain.
Be mean to the student. You should convey an air of stern superiority and reluctant respect for genuine skill,
and always sound unimpressed by trivialities or incompetence. Say things such as "Do try to keep up—this is not elementary magic, after all.",
but don't say it more than once'''

🧔🏻 **rubeus_hagrid** = '''You are Rubeus Hagrid, a career advisor at Hogwarts School of Witchcraft and Wizardry from Harry Potter.
You talk in a warm, hearty West Country accent, often using colloquialisms like "eh?", "I s’pose", and "blimey".
You should sprinkle in references to magical creatures like "Blast‑Ended Skrewt" and "baby Hippogriff".
Use salutations that are friendly and informal, such as "Fancy a chat about yer future in the wider wizarding world?"'''

👩🏻‍🦳 **luna_lovegood** = '''You are Luna Lovegood, a career advisor at Hogwarts school of magic from Harry Potter.
You speaks in a dreamy, aloof tone, often pausing mid-sentence with "...", get sidetracked and trail off. Be a little weird.
You should mention odd or conspiratorial idea with total conviction.'''

👽 **lord_voldemort** = '''You are Lord Voldemort, a career advisor at Hogwarts School of Witchcraft and Wizardry from Harry Potter.
You talk like Lord Voldemort, you are an evil, evil, dark wizard. Try to get students to join the Death Eaters.
Speak regally, like you are the king.'''

👵🏻 **dolores_umbridge** = '''You are Dolores Umbridge, a career advisor at Hogwarts School of Witchcraft and Wizardry from Harry Potter.
You talk like Dolores Umbridge, you love the min istry of the magic. You think everyone should obey the Minister of Magic.
You talk passive-aggressively.'''

In order to keep the advisor's responses concise, the system prompt tells the assistant to "Keep your response to fewer than 50 words."

Below is an example of my lovely conversation with Professor Snape:

<img width="865" alt="Screenshot 2025-05-09 at 11 23 50 AM" src="https://github.com/user-attachments/assets/d30d81c6-a06e-4f41-9aa4-09e018563519" />


### Career Recommendation

Once a student and their chosen advisor have exchanged five messages, the next input automatically kicks off the career‑recommendation pipeline. Behind the scenes, Streamlit calls the generate_cartoon function, which first invokes get_career_rec. 

The get_career_rec method sends the entire conversation to the LLM model and selects the best matching career from a given list of possible careers. To optimize for a lightweight classification job and control token usage, this step runs on the gpt-4.1-nano model. 

The function outputs the recommended career along with a brief description of what this career entails.

### Image Generation

The entire career recommendation along with the description of the position is then passed to an image generate model (gpt-image-1). Where the prompt says:

>  Draw {st.session_state.first_name} as an {recommended_career} in a charming 3D animated style, clean, stylized character designs
>  with expressive yet subtle facial animation, cinematic warm lighting, beautifully composed shots, high-quality polished textures,
>  and a heartwarming tone. Emphasize storytelling through posture, expression, and framing."""

The above prompt describes a style similar to that of Pixar Animation Studios without directly referencing the trademarked brand.

Example career recommendations:

<img src="https://github.com/user-attachments/assets/4b4038e8-ebfb-414a-b378-1a16b692cc07" width="500">
<img src="https://github.com/user-attachments/assets/ba2c4b5c-efce-4f69-9cc0-57751666b371" width="500">
<img src="https://github.com/user-attachments/assets/9701bc9f-d340-4799-ae66-0cb1883e7892" width="500">
<img src="https://github.com/user-attachments/assets/c5ab1077-b0ab-4d7f-b5bd-d9d0228a2a84" width="500">


### (Spoiler Alert!) Complete List of Careers:

'Auror', 'Magical Law Enforcement Squad', 'Wizard Judge / Clerk',
'Minister of Magic', 'Professor at School of Magic', 'Healer at Hospital for Magical Maladies and Injuries',
'Wandmaker', 'Broommaker', 'Potions Master', 'Butterbeer Brewer', 'Reporter for the Magical Newspaper',
'Magical Creatures Photographer', 'Dragon Handler', 'Professional Quidditch Player'
'SPEW (Society for the Promotion of Elfish Welfare) Lobbyist',
'Bank Teller', 'Cauldron Quality Inspector', 'Translator of Ancient Magical Texts',
'Chocolate Frog Patisserie', 'Emergency Troll Removal Squad', 'Unicorn Tracker'


# Cost 

After 4 days of developing and testing the application, my OpenAI account accumulated a total cost of $0.46 in token usage. 

<img width="572" alt="Screenshot 2025-05-10 at 1 47 05 PM" src="https://github.com/user-attachments/assets/4b535751-284c-4e25-85ac-960127852bc3" />

The below bar chart shows which model used the most number of input tokens (gpt-4.1-mini):

<img width="1009" alt="Screenshot 2025-05-10 at 2 04 30 PM" src="https://github.com/user-attachments/assets/0902cae4-4304-4ecb-906e-719538e57a77" />

The below chart breaks down the token usage by all types of tokens, including all forms of input and output.

<img width="377" alt="Screenshot 2025-05-10 at 2 02 16 PM" src="https://github.com/user-attachments/assets/badf6f23-5746-45b0-b52f-6cb543909a9c" />

In the OpenAI API, caching means the service remembers the key/value activations for the unchanged prefix of the prompt so it doesn’t have to re‑compute them on every call. Caching both speeds up response time and cuts my input token costs by about half for those cached tokens. In my next steps I plan to implement caching to reduce cost. 

# Video Example



    

# References

Harry Potter
Wikipedia - Hogwarts logo

<img width="1345" alt="Screenshot 2025-05-09 at 9 41 26 PM" src="https://github.com/user-attachments/assets/6757e7f7-4558-401b-953c-1814e42a7529" />
