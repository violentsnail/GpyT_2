# main.py
import wx
import openai
import json
from session_management.db import SessionDB
from session_management.ui import SessionUI, SessionsManagementUI
from session_management.openai_request import openai_request
from log import make_logger
import json

# Load the configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

def openai_request(session_id, model, message):
    # Initialize chat models with a list of messages. Each message object consists of a role and content.
    # For more info on the format of the list of messages, refer to the OpenAI API documentation.
    messages = [
        {"role": "system", "content": f"You are now chatting with session ID {session_id} and model {model}."},
        {"role": "user", "content": message}
    ]
    
    # Call the API
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    
    return response.choices[0].message['content']

# This method will be part of the SessionUI class
def send_input(self):
    # Get user input from the text box (assuming it's named self.input_box)
    user_input = self.input_box.GetValue()
    
    # Call openai_request
    response = self.openai_request(self.current_session_id, self.current_model, user_input)
    
    # Log the response
    self.log.log_response(self.current_session_id, response)
    
    # Display the response in the UI
    self.display_response(response)


def main():
    app = wx.App()
    db = SessionDB(config['db_file'])
    log = make_logger(config['logname'])
    session_management_ui = SessionsManagementUI(db, openai_request, log)  # Instantiate SessionsManagementUI
    session_management_ui.Show()  # Show the SessionsManagementUI
    app.MainLoop()


if __name__ == "__main__":
    main()
