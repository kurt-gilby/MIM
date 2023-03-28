import json
import tkinter as tk
from google_maps_api_value import GoogleMapsApiValue
from google_maps_api_calls import GoogleMapsAPICalls
from googlemaps.exceptions import ApiError
from PIL import ImageTk, Image
from io import BytesIO
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
        self.selection_box_height = file_data["SELECTION_BOX_HEIGTH"]
        self.search_entry_label = file_data["SEACH_ENTRY_LABEL"]
        self.suggestion_box_label = file_data["SUGGESTION_BOX_LABEL"]
        self.selection_box_label = file_data["SELECTION_BOX_LABEL"]
        self.cmd_button_text = file_data["CALCULATE_AND_DISPLAY_TEXT"]
        self.canvas_width = file_data["CANVAS_WIDTH"]
        self.canvas_heigth = file_data["CANVAS_HEIGTH"]
        self.root = tk.Tk()
        self.anchor = tk.W
        self.widgets = []
        self.on_search_suggestions_dict = {}
        self.on_selection_places_dict = {}
        self.places_lat_long_dict ={}
        self.current_location_details_dict = {}
        self.gmacs = None
        self.gm_client = None
        self.places_lat_lst = []
        self.places_lng_lst = []


    def connect_to_googlemaps(self):
        try:
            gmav = GoogleMapsApiValue()
            gm_api_key = gmav.get_gm_api_key()
            gmacs = GoogleMapsAPICalls(gm_api_key)
            gm_client = gmacs.connect_to_googlemaps()
        except ApiError as e:
            print(f'Google API Connection Error!: {e}')
        self.gmacs = gmacs
        self.gm_client = gm_client
    
    def get_current_locations_details(self):
        try:
            self.current_location_details_dict = self.gmacs.get_current_location_details(self.gm_client)
        except ApiError as e:
            print(f'Error with googlemaps API call!: {e}')
    
    def set_app_title(self):
        self.root.title(self.title)

    def set_app_size(self):
        self.root.geometry(f'{self.width}x{self.height}')

    def add_search_input(self):
        search_label = tk.Label(self.root,text=self.search_entry_label)
        search_label.pack(anchor=self.anchor)
        search_input= tk.Entry(self.root, width=self.item_width)
        search_input.pack(anchor=self.anchor)
        self.widgets.append(search_input)
        search_input.bind("<KeyRelease>", self.on_search_input_update)
            
    def on_search_input_update(self, event):
        entry = event.widget.get()
        if len(entry) > 9:
            try:
                suggestions_dict = self.gmacs.get_suggested_places_for_query(self.gm_client,entry,self.current_location_details_dict)
            except ApiError as e:
                print(f'Error with googlemaps API call!: {e}')
            self.widgets[1].delete(0,tk.END)
            for suggestion in suggestions_dict:
                if suggestion not in self.on_search_suggestions_dict:
                    self.on_search_suggestions_dict[suggestion] = suggestions_dict[suggestion]
                self.widgets[1].insert(tk.END,suggestions_dict[suggestion])
    
    def move_suggestion_to_selection(self,event):
        suggestion_box = event.widget
        selection_box = self.widgets[2]
        selections = suggestion_box.curselection()
        for selection_index in reversed(selections):
            selection_value = suggestion_box.get(selection_index)
            for key, value in self.on_search_suggestions_dict.items():
                if value == selection_value:
                    self.on_selection_places_dict[key] = selection_value
                    break
            suggestion_box.delete(selection_index)
            selection_box.insert(0, selection_value)

    def add_suggestions_list(self):
        suggestion_box_label = tk.Label(self.root,text=self.suggestion_box_label)
        suggestion_box_label.pack(anchor=self.anchor)
        suggestion_box_input= tk.Listbox(self.root, width=self.item_width, selectmode="browse",height=self.selection_box_height)
        suggestion_box_input.pack(anchor=self.anchor)
        self.widgets.append(suggestion_box_input)
        suggestion_box_input.bind("<Button-1>", self.move_suggestion_to_selection)
    
    def add_selections_list(self):
        selections_box_label = tk.Label(self.root,text=self.selection_box_label)
        selections_box_label.pack(anchor=self.anchor)
        selections_box_input= tk.Listbox(self.root, width=self.item_width,height=self.selection_box_height)
        selections_box_input.pack(anchor=self.anchor)
        self.widgets.append(selections_box_input)

    def set_places_lat_lng_list(self, param_dict):
        for place_id, lat_lng_dict in param_dict.items():
            for lat_lng, value in lat_lng_dict.items():
                if 'lat' in lat_lng:
                    self.places_lat_lst.append(value)
                elif 'lng' in lat_lng:
                    self.places_lng_lst.append(value)
    
    def get_places_mid_lat_lng(self):
        total_lat = sum(self.places_lat_lst)
        count_lat = len(self.places_lat_lst)
        total_lng = sum(self.places_lng_lst)
        count_lng = len(self.places_lng_lst)
        average_lat = total_lat/count_lat
        average_lng = total_lng/count_lng
        self.places_lat_lst.append(average_lat)
        self.places_lng_lst.append(average_lng)
    
    #TODO Get the static map to work
    def display_map_with_markers(self):
        marker_coordinates = list(zip(self.places_lat_lst,self.places_lng_lst))
        mid_point_coordinates = marker_coordinates[-1]
        mid_point_pair = f'{mid_point_coordinates[0]},{mid_point_coordinates[-1]}'
        try:
            static_map_img = self.gm_client.static_map(size = [100,100], zoom = 10, center = mid_point_pair)
        except Exception as e:
            print(f'Error occured while generating the static map : {e}')
        




    
    def find_midpoint(self, places_lat_long_dict):
        self.set_places_lat_lng_list(places_lat_long_dict)
        self.get_places_mid_lat_lng()
        self.display_map_with_markers()

        
        

    def calculate_middle_and_display(self):
        selected_palces_ids = list(self.on_selection_places_dict.keys())
        try:
            self.places_lat_long_dict = self.gmacs.get_places_lat_lng(self.gm_client,selected_palces_ids)
        except ApiError as e:
                print(f'Error with googlemaps API call!: {e}')
        self.find_midpoint(self.places_lat_long_dict)


    def add_calculate_middle_and_display_buttion(self):
        cmd_button = tk.Button(self.root, text=self.cmd_button_text, width=self.item_width, command=self.calculate_middle_and_display)
        cmd_button.pack(anchor=self.anchor)
        self.widgets.append(cmd_button)
    
    def add_canvas_for_gmap_display(self):
        gmap_display_canvas = tk.Canvas(self.root, width=self.canvas_width,height=self.canvas_heigth, bd=2,bg='white',highlightthickness=1,highlightbackground='white')
        gmap_display_canvas.pack(pady=10)
        self.widgets.append(gmap_display_canvas)





    def load_mim_app_gui(self):
        self.connect_to_googlemaps()
        self.get_current_locations_details()
        self.set_app_title()
        self.set_app_size()
        self.add_search_input()
        self.add_suggestions_list()
        self.add_selections_list()
        self.add_calculate_middle_and_display_buttion()
        self.add_canvas_for_gmap_display()
        self.root.mainloop()
        






    

