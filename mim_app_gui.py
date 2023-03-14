import json
import tkinter as tk
from google_maps_api_value import GoogleMapsApiValue
from google_maps_api_calls import GoogleMapsAPICalls
from googlemaps.exceptions import ApiError
class MIMAppGUI:

    def __init__(self) -> None:
        with open("parameters.json", 'r') as open_file:
            try:
                file_data = json.load(open_file)
            except:
                print(f'Error reading "parameters.json"!')
        self.title = file_data["APP_TITLE"]
        self.width = file_data["APP_WIDTH"]
        self.item_width = file_data["ITEM_WIDTH"]
        self.height = file_data["APP_HEIGHT"]
        self.search_entry_label = file_data["SEACH_ENTRY_LABEL"]
        self.suggestion_box_label = file_data["SUGGESTION_BOX_LABEL"]
        self.selection_box_label = file_data["SELECTION_BOX_LABEL"]
        self.root = tk.Tk()
        self.anchor = tk.W
        self.widgets = []
        self.suggestions = []
    
    def set_app_title(self):
        self.root.title(self.title)

    def set_app_size(self):
        self.root.geometry(f'{self.width}x{self.height}')
    
    def on_search_input_update(self, event):
        entry = event.widget.get()
        if len(entry) > 9:
            try:
                gmav = GoogleMapsApiValue()
                gm_api_key = gmav.get_gm_api_key()
                gmacs = GoogleMapsAPICalls(gm_api_key)
                gm_client = gmacs.connect_to_googlemaps()
                suggestions = gmacs.get_suggested_places_for_query(gm_client,entry)
            except ApiError as e:
                print(f'Error with googlemaps API call!: {e}')
            self.widgets[1].delete(0,tk.END)
            for suggestion in suggestions:
                self.widgets[1].insert(tk.END,suggestion)
                

    def add_search_input(self):
        search_label = tk.Label(self.root,text=self.search_entry_label)
        search_label.pack(anchor=self.anchor)
        search_input= tk.Entry(self.root, width=self.item_width)
        search_input.pack(anchor=self.anchor)
        self.widgets.append(search_input)
        search_input.bind("<KeyRelease>", self.on_search_input_update)
    
    def add_suggestions_list(self):
        suggestion_box_label = tk.Label(self.root,text=self.suggestion_box_label)
        suggestion_box_label.pack(anchor=self.anchor)
        suggestion_box_input= tk.Listbox(self.root, width=self.item_width)
        suggestion_box_input.pack(anchor=self.anchor)
        self.widgets.append(suggestion_box_input)
    
    def add_selections_list(self):
        selections_box_label = tk.Label(self.root,text=self.selection_box_label)
        selections_box_label.pack(anchor=self.anchor)
        selections_box_input= tk.Listbox(self.root, width=self.item_width)
        selections_box_input.pack(anchor=self.anchor)
        self.widgets.append(selections_box_input)  



    def load_mim_app_gui(self):
        self.set_app_title()
        self.set_app_size()
        self.add_search_input()
        self.add_suggestions_list()
        self.add_selections_list()
        self.root.mainloop()
        






    

