from urllib.request import urlopen
import json
from time import sleep
from abc import ABC, abstractmethod
from geopy.geocoders import Nominatim


class SpaceStation(ABC):

    @abstractmethod
    def register(self, observer):
        pass

    @abstractmethod
    def unregister(self, observer):
        pass

    @abstractmethod
    def notify(self, station_location):
        pass


class ConcreteSpaceStation(SpaceStation):

    def __init__(self):
        self.observers = set()
        self.stationLocation = ''

    def register(self, observer):
        self.observers.add(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    def notify(self, station_location):
        for observer in self.observers:
            observer.update(station_location)

    def update_station_location(self, station_location):
        self.stationLocation = station_location
        self.notify(station_location)

    def print_observers(self):
        print("List of current observers: " + str(self.observers))


class Observer(ABC):

    @abstractmethod
    def update(self, station_location):
        pass


class ConcreteScienceTeacher(Observer):

    def __init__(self):
        self.stationLocation = ''

    def update(self, station_location):
        self.stationLocation = station_location


def main():

    subject = ConcreteSpaceStation()
    subject.print_observers()
    first_observer = ConcreteScienceTeacher()
    subject.register(first_observer)
    subject.print_observers()

    try:
        while True:
            req = urlopen("http://api.open-notify.org/iss-now.json")
            new_info = json.loads(req.read())
            geolocator = Nominatim(user_agent="testing")
            location = geolocator.reverse((new_info['iss_position']['latitude'], new_info['iss_position']['longitude']))
            address = str(location.address)
            if address == "None":
                address = "over the ocean"
            updated_station_location = "(" + str(new_info['iss_position']['latitude']) + ", " + str(new_info['iss_position']['longitude']) + ") which is located: " + address

            # updating the location in the subject only
            subject.update_station_location(updated_station_location)

            # printing the location according to the observer, which gets updated accordingly
            print(first_observer.stationLocation)
            sleep(3)

    except KeyboardInterrupt:
        subject.unregister(first_observer)
        print("\nEnding space station tracking")
        subject.print_observers()
        return


if __name__ == "__main__":
    main()
