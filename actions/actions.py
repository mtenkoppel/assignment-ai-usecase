# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet
from datetime import datetime
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        AllSlotsReset()
        dispatcher.utter_message(text="Resetted all slots v2")

        return [AllSlotsReset()]


class ActionFindOffer(Action):

    def name(self) -> Text:
        return "action_find_offer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # variables for part 1
        city = tracker.get_slot("city")
        date = tracker.get_slot("arrival_date")
        num_nights = tracker.get_slot("num_nights")
        num_guests = tracker.get_slot("num_guests")

        # code to write date back to something more readble to user
        date = date[0:date.find("T")]
        date_time_obj = datetime.strptime(date, '%Y-%m-%d')
        human_readable_date = date_time_obj.strftime('%d %B %Y')

        price = self.calc_price(num_nights, num_guests, False)
        msg = f"A hotel in {city} arriving at {human_readable_date} for {num_nights} nights and {num_guests} guests costs {price} Euro."
        dispatcher.utter_message(text=msg)

        return []

    def calc_price(self, num_nights, num_guests, breakfast=False):
        price_per_night_per_guest = 75
        price_for_breakfast = 9
        price = price_per_night_per_guest * num_nights * num_guests
        if breakfast:
            price = price + (price_for_breakfast * num_nights *num_guests)
        return price


# action_process_offer
class ProcessOffer(Action):

    def name(self) -> Text:
        return "action_process_offer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # variables for part 1
        city = tracker.get_slot("city")
        date = tracker.get_slot("arrival_date")
        num_nights = tracker.get_slot("num_nights")
        num_guests = tracker.get_slot("num_guests")

        # code to write date back to something more readble to user
        date = date[0:date.find("T")]
        date_time_obj = datetime.strptime(date, '%Y-%m-%d')
        human_readable_date = date_time_obj.strftime('%d %B %Y')

        # variables for part 2
        person_name = tracker.get_slot("person_name")
        breakfast = tracker.get_slot("breakfast")
        payment_method = tracker.get_slot("payment_method")
        email = tracker.get_slot("email")
        price = 312
        breakfast_msg = "" if breakfast else "not"
        payment_method_msg = "on location" if payment_method else "online"

        price = self.calc_price(num_nights, num_guests, breakfast)

        msg = f"Summary: Reservation for {person_name} in hotel " \
              f"{city} from {human_readable_date} for {num_nights} " \
              f"with {num_guests} guests. Breakfast is {breakfast_msg} included. " \
              f"Payment is done {payment_method_msg}. Full price is {price} Euro."

        dispatcher.utter_message(text=msg)

        return []

    def calc_price(self, num_nights, num_guests, breakfast=False):
        price_per_night_per_guest = 75
        price_for_breakfast = 9
        price = price_per_night_per_guest * num_nights * num_guests
        if breakfast:
            price = price + (price_for_breakfast * num_nights *num_guests)
        return price


class ResetFormValues(Action):

    def name(self) -> Text:
        return "reset_form_values"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="[all values resetted: you may reinitiate a booking]")

        return [AllSlotsReset()]




class ValidateRestaurantForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_book_form"

    @staticmethod
    def hotels_db() -> List[Text]:
        """Database of supported hotels"""

        return ["amsterdam", "berlin", "hamburg", "paris", "madrid"]

    def validate_city(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate hotel value."""
        print(slot_value)
        if slot_value.lower() in self.hotels_db():
            # validation succeeded

            return {"city": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text=f"Unfortuately, there is not hotel in {slot_value}.")
            return {"city": None}
