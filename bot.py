
import asyncio
import re
import os

from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup

from flight_search import FlightSearch
from getIATA_code import get_IATA_code
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())


class MyStates(StatesGroup):
    fly_from = State()  # statesgroup should contain states
    fly_to = State()
    price = State()
    date_from = State()
    date_to = State()
    fly_from_code = State()
    fly_to_code = State()


async def send_flight_deals(bot, message, flight_deals):
    for index, deal in enumerate(flight_deals):
        formatted_message = (
            f"\n<b>Flight Deal #{index+1}:</b>\n"
            f"From: {deal.cityFrom} to: {deal.cityTo}\n"
            f"Price: {deal.price} euro. Duration: {deal.duration}\n"
            f"Quality: {deal.quality}\n"
            f"Distance: {deal.distance} km\n"
            f"Airlines: {', '.join(deal.airlines)}\n"
            f"Availability Seats: {deal.availability_seats}\n"
            f"Facilitated Booking Available: {deal.facilitated_booking_available}\n"
            f"Has Airport Change: {deal.has_airport_change}\n"
            f"Technical Stops: {deal.technical_stops}\n"
            f"Throw Away Ticketing: {deal.throw_away_ticketing}\n"
            f"Hidden City Ticketing: {deal.hidden_city_ticketing}\n"
            f"Virtual Interlining: {deal.virtual_interlining}\n"
            f"Local Arrival: {deal.local_arrival}\n"
            f"UTC Arrival: {deal.utc_arrival}\n"
            f"Local Departure: {deal.local_departure}\n"
            f"UTC Departure: {deal.utc_departure}\n"
            f"<b>Route:</b>\n"
        )

        for route in deal.route:
            formatted_message += (
                f"  - From {route.cityFrom} to {route.cityTo}, \n"
                f"Airline: {route.airline}, Flight No: {route.flight_no}, \n"
                f"Departure: {route.utc_departure}, Arrival: {route.utc_arrival}\n"
            )

        formatted_message += f"<a href='{deal.deep_link}'>Details</a>\n"

        await bot.send_message(message.chat.id, formatted_message, parse_mode="html")


@bot.message_handler(commands=['start'])
async def start_ex(message):

    await bot.set_state(message.from_user.id, MyStates.fly_from, message.chat.id)
    await bot.send_message(message.chat.id, 'Hi, write me fly_from')


@bot.message_handler(state="*", commands='cancel')
async def any_state(message):

    await bot.send_message(message.chat.id, "Your state was cancelled.")
    await bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.fly_from)
async def name_get(message):

    if not message.text.isalpha():
        await bot.send_message(message.chat.id, 'Please enter a valid input.')
        return
    town_code = get_IATA_code(message.text)

    if not town_code:
        await bot.send_message(message.chat.id, 'We could not find this town, please choose another one. ')
        return

    await bot.send_message(message.chat.id, f'Now write me a fly_to')
    await bot.set_state(message.from_user.id, MyStates.fly_to, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['fly_from'] = message.text
        data['fly_from_code'] = town_code


@bot.message_handler(state=MyStates.fly_to)
async def ask_age(message):

    if not message.text.isalpha():
        await bot.send_message(message.chat.id, 'Please enter a valid input.')
        return

    town_code = get_IATA_code(message.text)

    if not town_code:
        await bot.send_message(message.chat.id, 'We could not find this town, please choose another one. ')
        return

    await bot.send_message(message.chat.id, "Your price: ?")
    await bot.set_state(message.from_user.id, MyStates.price, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['fly_to'] = message.text
        data['fly_to_code'] = town_code


@bot.message_handler(state=MyStates.price)
async def ask_age(message):

    if not message.text.isnumeric():
        await bot.send_message(message.chat.id, 'Please enter a valid input.')
        return

    await bot.send_message(message.chat.id, "Date from: (dd/mm/yyyy)?")
    await bot.set_state(message.from_user.id, MyStates.date_from, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['price'] = float(message.text)


@bot.message_handler(state=MyStates.date_from)
async def ask_age(message):

    if not bool(re.match("[0-9]{2}/[0-9]{2}/[0-9]{4}", message.text)):
        await bot.send_message(message.chat.id, 'Please enter a valid input.(dd/mm/yyyy)')
        return

    await bot.send_message(message.chat.id, "Date to: (dd/mm/yyyy)?")
    await bot.set_state(message.from_user.id, MyStates.date_to, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['date_from'] = message.text


@bot.message_handler(state=MyStates.date_to)
async def ready_for_answer(message):

    if not bool(re.match("[0-9]{2}/[0-9]{2}/[0-9]{4}", message.text)):
        await bot.send_message(message.chat.id, 'Please enter a valid input.(dd/mm/yyyy)')
        return

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        fs = FlightSearch()
        result = fs.search_flights(
            data['fly_to_code'], data['fly_from_code'], data['price'], data['date_from'], message.text)

        if not result:
            await bot.send_message(message.chat.id, "We could not find any trips for this information:\n<b>Fly from: {fly_from}\nfly_to: {fly_to}\ndate from: {date_from}\ndate to: {date_to}\nprice: {price}</b>".format(
                fly_from=data['fly_from'], fly_to=data['fly_to'], date_from=data['date_from'],
                date_to=message.text, price=data['price'],
            ), parse_mode="html")
        else:
            await bot.send_message(message.chat.id, "Ready, take a look:\n<b>Fly from: {fly_from}\nfly_to: {fly_to}\ndate from: {date_from}\ndate to: {date_to}\nprice: {price}</b>".format(
                fly_from=data['fly_from'], fly_to=data['fly_to'], date_from=data['date_from'],
                date_to=message.text, price=data['price'],
            ), parse_mode="html")

            await send_flight_deals(bot, message, result)

    await bot.delete_state(message.from_user.id, message.chat.id)


bot.add_custom_filter(asyncio_filters.StateFilter(bot))


asyncio.run(bot.polling())
