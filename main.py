# main.py
import customtkinter
from tkintermapview import TkinterMapView
#import tkinter.simpledialog as simpledialog
from NN import NearestNeighbor  
import csv
import os

customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "TSP SOLVER"
    WIDTH = 800
    HEIGHT = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Set Marker",
                                                command=self.set_marker_event)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear Markers",
                                                command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.button_find_optimal_path = customtkinter.CTkButton(master=self.frame_left,
                                                        text="Find Optimal Path",
                                                        command=self.find_optimal_path)
        self.button_find_optimal_path.grid(pady=(20, 0), padx=(20, 20), row=2, column=0)

    

        

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="Search city")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        self.map_widget.set_address("India")
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Load existing data from the CSV file if it exists
        self.city_data = self.load_city_data()


    # Search city 
    def search_event(self, event=None):
        App.address = self.entry.get()
        self.map_widget.set_address(App.address)
        latitude, longitude = self.map_widget.get_position()
        print(f"Coordinates of {App.address}: Latitude: {latitude}, Longitude: {longitude}")
    

    # Set marker 
    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        city_name = App.address
        if city_name:
            self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))
            self.city_data[city_name] = current_position
            self.save_city_data()
            print("Set marker at: ", "city:", city_name, current_position[0], current_position[1] )

    
    # Clear marker and delete csv file
    def clear_marker_event(self):
        # Delete the CSV file
        if os.path.exists('city_data.csv'):
            os.remove('city_data.csv')
            print("'city_data.csv' file removed successfully!")

        # Clear markers from the map
        for marker in self.marker_list:
            marker.delete()

        # Clear marker list
        self.marker_list = []

        # Clear city data
        self.city_data = {}

    def load_city_data(self):
        try:
            with open('city_data.csv', 'r') as file:
                reader = csv.reader(file)
                city_data = {row[0]: (float(row[1]), float(row[2])) for row in reader}
        except FileNotFoundError:
            city_data = {}
        return city_data

    def save_city_data(self):
        with open('city_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for city, (latitude, longitude) in self.city_data.items():
                writer.writerow([city, latitude, longitude])




    def find_optimal_path(self):
        # Extract coordinates of cities
        city_coordinates = list(self.city_data.values())
        print("Co-ordinates of given cities: ", city_coordinates)

        # Calculate distances between cities (for simplicity, using Euclidean distance)
        distances = [[((x1 - x2)**2 + (y1 - y2)**2)**0.5 for x1, y1 in city_coordinates] for x2, y2 in city_coordinates]

        # Create NearestNeighbor instance
        nn_solver = NearestNeighbor(distances)

        # Find optimal path
        optimal_path, _ = nn_solver.tsp_nearest_neighbor()

        # Draw the optimal path on the map
        for i in range(len(optimal_path) - 1):
            start_city = list(self.city_data.keys())[optimal_path[i]]
            end_city = list(self.city_data.keys())[optimal_path[i+1]]
            print("Optimal path:", start_city, "->", end_city)







    
        

    

    

        

    

   


    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()