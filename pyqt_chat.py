# based on https://github.com/pyqt/examples/blob/_/src/11%20PyQt%20Thread%20example/01_single_threaded.py

DEBUG = False

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


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

Try to be straight and to the point as much as possible. 

Do not ask students questions but try to answer their questions.

"""

dotenv.load_dotenv()

client = genai.Client()

# GUI:
app = QApplication([])
title = QLabel("Shai Bot")
title.setFont(QFont('Arial', 30))
title.setAlignment(Qt.AlignCenter)
text_title = QLabel("Ask Your Question Below")
text_title.setFont(QFont('Arial', 18))
text_title.setAlignment(Qt.AlignCenter)
text_area = QPlainTextEdit()
text_area.setFocusPolicy(Qt.FocusPolicy.NoFocus)
text_area.setFont(QFont('Arial', 18))
text_area.setMinimumWidth(1300)
text_area.setStyleSheet("""
background-color: #303234;
color: #FAF9F6;                    
""")
message = QLineEdit()
message.setFont(QFont('Arial', 18))
message.setStyleSheet("""
background-color: #303234;
color: #FAF9F6;                    
""")
layout = QVBoxLayout()
layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)
layout.addWidget(text_area, alignment=Qt.AlignmentFlag.AlignHCenter)
layout.addWidget(message)
window = QWidget()
window.setLayout(layout)
window.setStyleSheet("""
background-color: #000000""")
window.resize(1000,800)
window.show()

chat_history = ''

start_chat = "Greetings! I'm Shai Bot, I'm here to help you with your computer science related questions. I cannot give you direct answers, but I can guide you through solving the problems"

text_area.appendPlainText('\nShai Bot: ' + start_chat + '\n')

chat_history = start_chat

def query_and_retry(prompt):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )
        return response
    except Exception as e:
        text_area.appendPlainText(str(type(e)) + '\n' + str(e) + '\nRetrying...')
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
  
    
    text_area.appendPlainText('Shai Bot: ' + response_text + '\n')


    chat_history += user_prompt + '\n' + response_text  

# Signals:
message.returnPressed.connect(send_message)

app.exec()