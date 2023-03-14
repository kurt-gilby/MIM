import googlemaps as gm
from googlemaps.exceptions import ApiError
class GoogleMapsAPICalls:
    
    def __init__(self,gm_api_key) -> None:
        self.gm_api_key = gm_api_key
        
    def connect_to_googlemaps(self):
        try:
            gmaps = gm.Client(self.gm_api_key)
        except ApiError as e:
            print(f'Google API Connection Error!: {e}')
        return gmaps
    
    def get_suggested_places_for_query(self, gm_client, query):
        try:
            results = gm_client.places_autocomplete(query)
            suggestions = [result['description'] for result in results]
        except ApiError as e:
            print(f'Error getting result from places query! {e}')
        return suggestions

