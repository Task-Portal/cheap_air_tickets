from datetime import datetime


def format_date(date_str):
    try:
        datetime_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        formatted_date = datetime_obj.strftime("%d/%m/%Y, %H:%M:%S")

        return formatted_date
    except ValueError:
        return date_str
