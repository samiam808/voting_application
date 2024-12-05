from PyQt6 import QtWidgets  # For the gui
from vote_gui import Ui_voter_menu  # The code for the gui
import csv  # To help with saving data
import os  # For file operations


class VotingApplication(QtWidgets.QMainWindow):
    """
    A class with all the logic for ensuring the voting system works as intended
    """

    def __init__(self):
        super().__init__()
        self.ui = Ui_voter_menu()  # Open the UI
        self.ui.setupUi(self)  # Set up UI

        # Make the feedback hidden at first
        self.ui.vote_error.hide()
        self.ui.vote_success.hide()
        self.ui.already_voted.hide()

        # Add functionality to the submit button
        self.ui.vote_button.clicked.connect(self.submit_vote)

        # Create CSV file if it does not already exist and adds the NUID and their vote
        self.csv_file_path: str = 'election.csv'
        if not os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["NUID", "Candidate"])

    def submit_vote(self) -> None:
        """
        Make sure votes get recorded and ensures the NUID is unique and 8 digits
        """
        nuid: str = self.ui.user_NUID.text().strip()  # Get the NUID input

        # Validate the NUID
        if not nuid.isdigit() or len(nuid) != 8:
            self.display_label("error")
            return

        # Determine the selected candidate
        if self.ui.vote_will.isChecked():
            candidate: str = "Will"
        elif self.ui.vote_max.isChecked():
            candidate: str = "Max"
        elif self.ui.vote_custom.isChecked():
            candidate = self.ui.custom_vote.text().strip()
            if not candidate:
                self.display_label("error")
                return
        else:
            self.display_label("error")
            return

        # Check if the voter has already voted
        if self.has_voter_already_voted(nuid):
            self.display_label("already_voted")
        else:
            self.record_vote(nuid, candidate)
            self.display_label("success")

        # Clear the custom vote field
        self.ui.custom_vote.clear()

    def has_voter_already_voted(self, nuid: str) -> bool:
        """
        Check if a voter with the given NUID has already voted.

        Make sure the NUID is 8 digits long and they are all numbers

        Returns:
            bool: True if the voter has already voted, False otherwise.
        """
        with open(self.csv_file_path, 'r') as file:
            vote_records = csv.reader(file)
            next(vote_records)  # Skip the header row
            return any(row[0] == nuid for row in vote_records)

    def record_vote(self, nuid: str, candidate: str) -> None:
        """
        Record the voter's NUID and selected candidate into the CSV file.
        """
        with open(self.csv_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nuid, candidate])

    def display_label(self, label_type: str) -> None:
        """
        Display the appropriate label based on the operation outcome.
        """
        # Hide all labels before displaying the correct one
        self.ui.vote_error.hide()
        self.ui.vote_success.hide()
        self.ui.already_voted.hide()

        if label_type == "error":
            self.ui.vote_error.show()
        elif label_type == "success":
            self.ui.vote_success.show()
        elif label_type == "already_voted":
            self.ui.already_voted.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)  # Create the application instance
    window = VotingApplication()  # Create the voting application window
    window.show()  # Display the window
    sys.exit(app.exec())  # Execute the application event loop