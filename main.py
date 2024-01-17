from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.config import Config
import joblib
import pandas as pd
Config.set('graphics', 'width', '250')
Config.set('graphics', 'height', '550')


class RentPredictionApp(App):
    def pred(self, seller, bed_c, layout_, propertytyp, localit, area_c, furnish, bath_c, city_):
        dfH = pd.read_csv('Hyderabad_rent.csv')
        dfD = pd.read_csv('Delhi_rent.csv')
        dfM = pd.read_csv('Mumbai_rent.csv')
        dfC = pd.read_csv('Chennai_rent.csv')
        dfK = pd.read_csv('Kolkata_rent.csv')
        dfB = pd.read_csv('Bangalore_rent.csv')
        dfs = [dfH, dfD, dfM, dfC, dfK, dfB]
        cities = ['Hyderabad', 'Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore']
        for df, city in zip(dfs, cities):
            df['city'] = city
        df = pd.concat(dfs)
        localit = localit.lower()
        if localit in df['locality'].values:
            locality_index = df.index[df['locality'] == localit][0]
            locality_c = df.at[locality_index, 'locality']
        else:
            locality_c = 695

        seller_dict = {'Agent': 0, 'Builder': 1, 'Owner': 2}
        seller_c = seller_dict[seller]

        layout_dict = {'RK': 0, 'BHK': 1}
        layout_c = layout_dict[layout_]

        property_dict = {'Villa': 4, 'Independent House': 2, 'Apartment': 0, 'Independent Floor': 1,
                         'Studio Apartment': 3}
        property_c = property_dict[propertytyp]

        furnish_dict = {'Furnished': 0, 'Semifurnished': 1, 'Unfurnished': 2}
        furnish_c = furnish_dict[furnish]

        city_dict = {'Hyderabad': 3, 'Delhi': 2, 'Mumbai': 5, 'Chennai': 1, 'Kolkata': 4, 'Bangalore': 0}
        city_c = city_dict[city_]

        final_pred = [seller_c, bed_c, layout_c, property_c, locality_c, area_c, furnish_c, bath_c, city_c]
        with open('model.joblib', 'rb') as f:
            model = joblib.load(f)
        rent = round(model.predict([final_pred])[0])
        return rent

    # Define clear_inputs method
    def clear_inputs(self, instance):
        self.seller_type_option.text = "Agent"
        self.bedroom_option.text = "1"
        self.layout_option.text = "BHK"
        self.property_type_option.text = "Apartment"
        self.locality_input.text = ""
        self.area_input.text = ""
        self.furnishing_option.text = "Furnished"
        self.bathroom_option.text = "1"
        self.city_option.text = "Bangalore"
        self.rent_display.text = ""

    def build(self):
        layout = GridLayout(cols=2, spacing=10, padding=20)

        # Add Seller Type input
        layout.add_widget(Label(text="Seller Type"))
        self.seller_type_option = Spinner(text="Agent", values=("Builder", "Agent", "Owner"))
        layout.add_widget(self.seller_type_option)

        # Add Bedrooms input
        layout.add_widget(Label(text="Bedrooms"))
        self.bedroom_option = Spinner(text="1", values=("1", "2", "3", "4", "5", "6", "7"))
        layout.add_widget(self.bedroom_option)

        # Add Layout Type input
        layout.add_widget(Label(text="Layout Type"))
        self.layout_option = Spinner(text="BHK", values=("RK", "BHK"))
        layout.add_widget(self.layout_option)

        # Add Property Type input
        layout.add_widget(Label(text="Property Type"))
        self.property_type_option = Spinner(text="Apartment", values=(
        "Villa", "Independent House", "Apartment", "Independent Floor", "Studio Apartment"))
        layout.add_widget(self.property_type_option)

        # Add Locality input
        layout.add_widget(Label(text="Locality"))
        self.locality_input = TextInput(multiline=False)
        layout.add_widget(self.locality_input)

        # Add Area input
        layout.add_widget(Label(text="Area (sqft)"))
        self.area_input = TextInput(multiline=False)
        layout.add_widget(self.area_input)

        # Add Furnishing input
        layout.add_widget(Label(text="Furnishing"))
        self.furnishing_option = Spinner(text="Furnished", values=("Furnished", "Semifurnished", "Unfurnished"))
        layout.add_widget(self.furnishing_option)

        # Add Bathrooms input
        layout.add_widget(Label(text="Bathrooms"))
        self.bathroom_option = Spinner(text="1", values=("1", "2", "3", "4", "5"))
        layout.add_widget(self.bathroom_option)

        # Add City input
        layout.add_widget(Label(text="City"))
        self.city_option = Spinner(text="Hyderabad",
                                   values=("Bangalore", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"))
        layout.add_widget(self.city_option)

        # Add Button to calculate rent
        self.calculate_button = Button(text="Predict Rent", background_color=(0, 1, 0, 1))
        self.calculate_button.bind(on_press=self.show_rent)
        layout.add_widget(self.calculate_button)

        # Add Clear Button
        self.clear_button = Button(text="Clear", background_color=(1, 0, 0, 1))
        self.clear_button.bind(on_press=self.clear_inputs)
        layout.add_widget(self.clear_button)

        # Add Label to display Rent
        self.rent_display = Label(text="")
        layout.add_widget(self.rent_display)

        return layout

    def show_rent(self, instance):
        seller = self.seller_type_option.text
        bed_c = int(self.bedroom_option.text)
        layout_ = self.layout_option.text
        propertytyp = self.property_type_option.text
        localit = self.locality_input.text
        area_c = int(self.area_input.text)
        furnish = self.furnishing_option.text
        bath_c = int(self.bathroom_option.text)
        city_ = self.city_option.text
        rent = self.pred(seller, bed_c, layout_, propertytyp, localit, area_c, furnish, bath_c, city_)
        self.rent_display.text = "Predicted Rent is Rs. " + str(rent)


RentPredictionApp().run()