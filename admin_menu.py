from admin_sqlite import DB_connection
from inputs import Inputs
from datetime import datetime
from datetime import date

class Admin:
    # Initialize the admin menu
    def __init__(self, db_path) -> None:
        self.db = DB_connection(db_path)
        while True:
            self.option = self.login()
            if self.option == "1":
                print("Πάτησες το 1!")
            elif self.option == "2":
                print("Πάτησες το 2!")
            elif self.option == "3":
                self.check_in()
            elif self.option == "-1":
                return

    # Menu to get the option from the admin
    def login(self):
        login = Inputs.input_method(
            "\n1: Show all the bookings concerning a specific time period.\
            \n2: Show the 5 reviews with the worst scores and the rooms they concern.\
            \n3: Check in.\
            \n4: Check out.\
            \n-1: Exit\n", "Not a valid option.",
            ["1", "2", "3", "4", "-1"])
        return login

    # Function to check in a client
    def check_in(self):
        booking_id, _ = Inputs.input_number("Enter booking id: ", "Not a number!")
        if len(self.db.retrieval_query(f"SELECT * FROM Booking WHERE booking_id = {int(booking_id)}")) != 0:
            arrival_date = self.db.retrieval_query(f"SELECT arrival FROM Booking WHERE booking_id = {int(booking_id)}")[0][0]
            arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d').date()
            if arrival_date <= date.today():
                room_id = int(self.db.get_a_room(booking_id))
                check_in_date = date.today()
                check_out_date = 'NULL'
                self.db.inster_fills(booking_id, room_id, check_in_date, check_out_date)
            else:
                print("Your booking is for", arrival_date)
        else:
            print("There is no such booking!") 


if __name__ == "__main__":
    menu = Admin("database.db")
