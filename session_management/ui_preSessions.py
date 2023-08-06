import wx
from .openai_request import openai_request

class SessionUI(wx.Frame):
    def __init__(self, db, log, title="Chat UI", parent=None):
        super(SessionUI, self).__init__(parent, title=title, size=(500,500))
        
        self.db = db
        self.log = log

        self.InitUI()


    def InitUI(self):
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        # Display area
        self.display_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(self.display_area, 1, flag=wx.EXPAND)

        # Input area
        self.input_box = wx.TextCtrl(panel)
        send_button = wx.Button(panel, label="Send")
        send_button.Bind(wx.EVT_BUTTON, self.send_input)

        # Put input area and send button into a horizontal box sizer
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.input_box, 1, flag=wx.EXPAND)
        hbox.Add(send_button, 0)

        # Add hbox to the main box sizer
        box.Add(hbox, 0, flag=wx.EXPAND)

        panel.SetSizer(box)
        self.Show()

    def send_input(self, event):
        # Get user input from the text box
        user_input = self.input_box.GetValue()

        # Get the current session ID and model
        current_session_id, current_model = self.db.get_current_session_and_model()
        if current_session_id is None or current_model is None:
            # There is no current session or model. Handle this error however you'd like.
            # For example, you could show an error message and return early:
            wx.MessageBox("No session selected!", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Call openai_request
        response = self.openai_request(current_session_id, current_model, user_input)

        # Log the response
        self.log.log_response(current_session_id, response)

        # Display the response in the UI
        self.display_response(response)

        # Clear the input box
        self.input_box.Clear()



    def display_response(self, response):
        # Display the response in the display area
        self.display_area.AppendText("AI: " + response + "\n")
