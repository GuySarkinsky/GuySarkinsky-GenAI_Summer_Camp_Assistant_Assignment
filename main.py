from openai import OpenAI

import os

from prompts import (
    router_promp,
    question_prompt,
    application_prompt,
    system_role_description,
    wellcome_text
)

from Sunny_Meadows_Summer_Camp import (summer_camp_details, summer_camp_details_short)


# Load the API key from the environment variable
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()

chat_log = []
chat_log_user = []



def sent_to_gpt(chat_log):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.2,
    messages=chat_log)
    assistant_response = response.choices[0].message.content
    return assistant_response


chat_log.append({"role": "system", "content": system_role_description})

def chat_content(user_message):
    chat_log.append({"role": "user", "content": router_promp + user_message})
    router_response = sent_to_gpt(chat_log)
    if router_response == "inquiry":
            prompt_with_details = question_prompt(user_message, summer_camp_details_short)
    elif router_response == "sign-up":
            prompt_with_details = application_prompt(user_message, summer_camp_details_short)
            
    chat_log_user.append({"role": "user", "content": prompt_with_details})
    response_question = sent_to_gpt(chat_log_user)
    print("Summer Camp Assistant: \n", response_question.strip("\n").strip() + "\n") 
    
print(wellcome_text) 
    
    
while True:
  try:    
    print("Please enter your question: \n")
    user_message = input()
    if user_message.lower() == "quit":
        break
    else:
       chat_content(user_message)
    
  except Exception as e:
      print(f"An error occurred: {e}")