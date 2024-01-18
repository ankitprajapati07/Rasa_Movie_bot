from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import csv
import json


class ActionListMovie(Action):

    def name(self) -> Text:
        return "action_list_movie"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        genre = tracker.get_slot("genre")
        movies_in_genre = []

        with open("data/movie.csv") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=['movie_name', 'genre'])
            for row in reader:
                if row['genre'] == genre:
                    movies_in_genre.append(row['movie_name'])

        if movies_in_genre:
            message = "Here are some movies in the {} genre: {}".format(genre, ", ".join(movies_in_genre))
        else:
            message = "Sorry, I couldn't find any movies in that genre."

        dispatcher.utter_message(text=message)
        return []


class ActionListGenre(Action):

    def name(self) -> Text:
        return "action_list_genre"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Open the CSV file containing movie information
        with open('data/movie.csv', 'r') as file:
            reader = csv.reader(file)
            genre_list = []
            for inx, row in enumerate(reader):
                if inx != 0:
                    if row[1] not in genre_list:
                        genre_list.append(row[1])  # Assuming the genre is in the second column
        # Send the list of genres to the user
        if len(genre_list) > 0:
            message = f"We have movies in the following genres: {', '.join(genre_list)}"
        else:
            message = "Sorry, We do not have currently that genre of movies...!!"
        dispatcher.utter_message(text=message)

        return []

