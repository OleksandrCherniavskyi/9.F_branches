from bardapi import Bard
from bard_token import token
import os
from dotenv import load_dotenv
os.environ["_BARD_API_KEY"] = token


load_dotenv()

bard = Bard()

print("* Welcome to Bard Chat! *")

while True:
  user_input = input("\U0001F464 You: ")
  print("")
  print("\U0001F916 Bard:", bard.get_answer(user_input.strip())['content'])
  print("-" * 100)


