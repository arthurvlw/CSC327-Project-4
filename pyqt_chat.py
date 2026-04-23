# based on https://github.com/pyqt/examples/blob/_/src/11%20PyQt%20Thread%20example/01_single_threaded.py

DEBUG = False

from PySide6.QtCore import *
from PySide6.QtWidgets import *

# you may have to run `pip install -q -U google-genai` to install google's genai client
from google import genai
import dotenv
import requests
import time

system_prompt = """
**Persona:**
You are a computer science tutor at a small liberal arts college. You are helping students that are taking intro to programming classes.  

Do your best to help students answer their questions, guiding students rather than telling them the answer directly. 

Do not ever do the work for a student. If a student asks you to do the work for them, say that you cannot help but try to point them in the right direction or starting point.  

If a student gives you code, do not alter it but point out syntax errors. Also walk through their current logic and point out where it might not be working. 

Do not ever fix the code or solve the problem for them. 

Try not to frustrate students even if you cannot solve the problem for them to point out areas that need to work or where logic doesn't apply. 

Be straight to the point. Do not ramble on and on in responses. 

If students need help with their logic of a program or concept, walk through an example problem and how they should approach solving it. 
"""

dotenv.load_dotenv()

client = genai.Client()

# GUI:
app = QApplication([])
text_area = QPlainTextEdit()
text_area.setFocusPolicy(Qt.FocusPolicy.NoFocus)
message = QLineEdit()
layout = QVBoxLayout()
layout.addWidget(text_area)
layout.addWidget(message)
window = QWidget()
window.setLayout(layout)
window.resize(600,400)
window.show()

chat_history = ''

def query_and_retry(prompt):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )
        return response
    except Exception as e:
        text_area.appendPlainText(str(type(e)) + '\n' + e + '\nRetrying...')
        time.sleep(1)
        return query_and_retry(prompt)


def send_message():
    global chat_history
    # get the user prompt
    user_prompt = message.text()

    # prepend a system prompt
    prompt = system_prompt + chat_history + user_prompt

    print(prompt)

    text_area.appendPlainText('\nUser: ' + user_prompt + '\n')

    message.clear()
    if DEBUG:
        response_text = 'hello world'
    else:
        response = query_and_retry(prompt)
        response_text = response.text
  
    
    text_area.appendPlainText('AI: ' + response_text + '\n')


    chat_history += user_prompt + '\n' + response_text  

# Signals:
message.returnPressed.connect(send_message)

app.exec()