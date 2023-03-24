import googlemaps as gm
from googlemaps.exceptions import ApiError
import geocoder

class GoogleMapsAPICalls:
    
    def __init__(self,gm_api_key) -> None:
        self.gm_api_key = gm_api_key
        
    def connect_to_googlemaps(self):
        try:
            gmaps = gm.Client(self.gm_api_key)
        except ApiError as e:
            print(f'Google API Connection Error!: {e}')
        return gmaps
    
    def get_suggested_places_for_query(self, gm_client, query,current_location_dict):
        country = {'country' : current_location_dict['country_short']}    
        state = current_location_dict['state']
        city = current_location_dict['city']
        query = state + ' ' + city + ' ' + query
        try:
            results = gm_client.places_autocomplete(query, components = country)
            suggestions = [result['description'] for result in results]
            suggestion_ids = [result['place_id'] for result in results]

        except ApiError as e:
            print(f'Error getting result from places query! {e}')
        suggestions_dict= dict(zip(suggestion_ids,suggestions))
        return suggestions_dict
    
    def get_places_lat_lng(self, gm_client, selected_palces_ids):
        places_lat_lng_dict ={}
        lat_lng_dict = {}
        for selected_place_id in selected_palces_ids:
            try:
                place_details = gm_client.place(place_id=selected_place_id)
                place_id = place_details['result']['place_id']
                lat_lng_dict['lat'] = place_details['result']['geometry']['location']['lat']
                lat_lng_dict['lng'] = place_details['result']['geometry']['location']['lng']
                places_lat_lng_dict[place_id] = lat_lng_dict
            except ApiError as e:
                print(f'Error retriving lat and lng! {e}')
        return places_lat_lng_dict
    
    
    def get_current_location_details(self,gm_client):
        current_location_lat_lng_tup = tuple(geocoder.ip('me').latlng)
        locations_results = gm_client.reverse_geocode(current_location_lat_lng_tup)
        locations_results_index=0
        address_key = 'address_components'
        address_type_key = 'types'
        address_name_key = 'long_name'
        address_short_name_key = 'short_name'
        address_types = ['locality','administrative_area_level_1','country']
        country_list = []
        state_list =[]
        city_list =[]
        current_location_details_dict = {}
        for location_result in locations_results:
            for address_item in location_result[address_key]:
                for address_type in address_item[address_type_key]:
                    if address_type in address_types:
                        if address_type == address_types[2]:
                            if address_item[address_name_key] not in country_list:
                                country_list.append(address_item[address_name_key])
                                country_list.append(address_item[address_short_name_key])
                        elif address_type == address_types[1]:
                            if address_item[address_name_key] not in state_list:
                                state_list.append(address_item[address_name_key])
                        elif address_type == address_types[0]:
                            if address_item[address_name_key] not in city_list:
                                city_list.append(address_item[address_name_key])
            locations_results_index += 1
        current_location_details_dict['country'] = country_list[0]
        current_location_details_dict['country_short'] = country_list[1]
        current_location_details_dict['state'] = state_list[0]
        current_location_details_dict['city'] = city_list[0]
        return current_location_details_dict

