from bardapi import Bard
from bard_token import token


import os

os.environ["_BARD_API_KEY"] = token

message = input("Enter Your Prompt: ")


print(Bard().get_answer(str(message)))
print(Bard().get_answer(str(message))['content'])
