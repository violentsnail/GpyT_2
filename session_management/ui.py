import wx
from .db import SessionDB
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
        
        # Get current session and model
        current_session_id, current_model = self.db.get_current_session_and_model()

        # Call openai_request
        response = openai_request(current_session_id, current_model, user_input)
        
        # Log the responsesd
        self.log.log_response(current_session_id, response)
        
        # Display the response in the UI
        self.display_response(response)

        # Clear the input box
        self.input_box.Clear()

    def display_response(self, response):
        # Display the response in the display area
        self.display_area.AppendText("AI: " + response + "\n")


class SessionsManagementUI(wx.Frame):
    def __init__(self, db, openai_request, log, title="Session Management UI"):
        super(SessionsManagementUI, self).__init__(None, title=title, size=(500,500))
        
        self.db = db
        self.openai_request = openai_request
        self.log = log

        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        # List of sessions
        self.sessions_list = wx.ListCtrl(panel, size=(200, 100), style=wx.LC_REPORT)
        self.sessions_list.InsertColumn(0, "Session ID")
        self.sessions_list.InsertColumn(1, "Model")
        box.Add(self.sessions_list, 1, flag=wx.EXPAND)

        # Session buttons
        create_button = wx.Button(panel, label="Create Session")
        create_button.Bind(wx.EVT_BUTTON, self.create_session)
        open_button = wx.Button(panel, label="Open Session")
        open_button.Bind(wx.EVT_BUTTON, self.open_session)
        delete_button = wx.Button(panel, label="Delete Session")
        delete_button.Bind(wx.EVT_BUTTON, self.delete_session)
        box.Add(create_button)
        box.Add(open_button)
        box.Add(delete_button)

        panel.SetSizer(box)
        self.Show()

        self.update_sessions_list()

    def update_sessions_list(self):
        self.sessions_list.DeleteAllItems()  # Remove existing items first
        sessions = self.db.get_all_sessions()
        for session in sessions:
            index = self.sessions_list.InsertItem(self.sessions_list.GetItemCount(), str(session.id))
            self.sessions_list.SetItem(index, 1, session.model)

    def create_session(self, event):
            dialog = CreateSessionDialog(self)
            if dialog.ShowModal() == wx.ID_OK:
                session_name = dialog.name_text.GetValue()
                model = dialog.model_text.GetValue()
                self.db.create_session(session_name, model)  # Assume create_session method takes session_name and model as parameters
                self.update_sessions_list()

    def open_session(self, event):
        # Open the selected session in a new window
        selected_item = self.sessions_list.GetFocusedItem()
        if selected_item == -1:  # No item selected
            wx.MessageBox("No session selected!", "Error", wx.OK | wx.ICON_ERROR)
            return
        session_id = int(self.sessions_list.GetItemText(selected_item))  # Convert string to int
        session_ui = SessionUI(self.db, self.log, session_id)
        session_ui.Show()

    def delete_session(self, event):
        # Delete the selected session
        selected_item = self.sessions_list.GetFocusedItem()
        if selected_item == -1:  # No item selected
            wx.MessageBox("No session selected!", "Error", wx.OK | wx.ICON_ERROR)
            return
        session_id = int(self.sessions_list.GetItemText(selected_item))  # Convert string to int
        self.db.delete_session(session_id)
        # Update the sessions list
        self.update_sessions_list()

class CreateSessionDialog(wx.Dialog):
    def __init__(self, parent):
        super(CreateSessionDialog, self).__init__(parent, title="Create Session", size=(200,150))

        self.panel = wx.Panel(self)
        self.layout = wx.BoxSizer(wx.VERTICAL)

        self.name_label = wx.StaticText(self.panel, label="Session Name:")
        self.name_text = wx.TextCtrl(self.panel)

        self.model_label = wx.StaticText(self.panel, label="Model:")
        self.model_text = wx.TextCtrl(self.panel)

        self.create_button = wx.Button(self.panel, label="Create")
        self.create_button.Bind(wx.EVT_BUTTON, self.on_create)
        self.cancel_button = wx.Button(self.panel, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

        self.layout.Add(self.name_label)
        self.layout.Add(self.name_text)
        self.layout.Add(self.model_label)
        self.layout.Add(self.model_text)
        self.layout.Add(self.create_button)
        self.layout.Add(self.cancel_button)

        self.panel.SetSizerAndFit(self.layout)

    def on_create(self, event):
        self.EndModal(wx.ID_OK)

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)