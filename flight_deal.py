from route_info import RouteInfo
from lib import format_date
class FlightDeal:
    def __init__(self, data):
        self.cityFrom = data.get('cityFrom')
        self.cityTo = data.get('cityTo')        
        self.quality = data.get('quality')
        self.distance = data.get('distance')
        self.duration = self.format_duration( data.get('duration', {}).get('total'))
        self.price = data.get('price')
        self.airlines = data.get('airlines')
        self.route = [RouteInfo(route) for route in data.get('route', [])]
        self.deep_link = data.get('deep_link')
        self.availability_seats = data.get('availability', {}).get('seats')
        self.facilitated_booking_available = data.get('facilitated_booking_available')
        self.has_airport_change = data.get('has_airport_change')
        self.technical_stops = data.get('technical_stops')
        self.throw_away_ticketing = data.get('throw_away_ticketing')
        self.hidden_city_ticketing = data.get('hidden_city_ticketing')
        self.virtual_interlining = data.get('virtual_interlining')
        self.local_arrival = format_date(data.get('local_arrival'))
        self.utc_arrival = format_date(data.get('utc_arrival'))
        self.local_departure = format_date(data.get('local_departure'))
        self.utc_departure = format_date(data.get('utc_departure'))
        
    
    def format_duration(self, seconds):
        days = seconds // (3600 * 24)
        hours = (seconds % (3600 * 24)) // 3600
        minutes = (seconds % 3600) // 60
        return f"{days}d {hours}h {minutes}m"   
    
 