from lib import format_date

class RouteInfo:
    def __init__(self, route_data):
        self.cityFrom = route_data.get('cityFrom')
        self.cityTo = route_data.get('cityTo')
        self.airline = route_data.get('airline')
        self.flight_no = route_data.get('flight_no')
        self.bags_recheck_required = route_data.get('bags_recheck_required')
        self.vehicle_type = route_data.get('vehicle_type')
        self.local_arrival = format_date(route_data.get('local_arrival'))
        self.utc_arrival = format_date(route_data.get('utc_arrival'))
        self.local_departure = format_date(route_data.get('local_departure'))
        self.utc_departure = format_date(route_data.get('utc_departure'))