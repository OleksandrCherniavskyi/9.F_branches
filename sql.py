from bardapi import Bard
from bard_token import token
import os
import streamlit as st
from streamlit_chat import message
#from streamlit import chat_message as message
os.environ["_BARD_API_KEY"] = token

st.title("Google Bard Clone")

def responce_api(promot):
    message=Bard().get_answer(str(promot))['content']
    return message

def user_input():
    input_text = st.text_input("Enter Your Prompt: ")
    return input_text

if 'generate' not in st.session_state:
    st.session_state['generate']=[]
if 'past' not in st.session_state:
    st.session_state['past']=[]

user_text = user_input()

if user_text:
    output = responce_api(user_text)
    st.session_state.generate.append(output)
    st.session_state.past.append(user_text)

if st.session_state['generate']:
    for i in range(len(st.session_state['generate'])-1, -1, -1):
        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
        message(st.session_state['generate'][i], key=str(i))
