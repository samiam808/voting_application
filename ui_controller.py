from PyQt6 import QtWidgets
from vote_gui import Ui_voter_menu
from logic import VotingLogic


class VotingController(QtWidgets.QMainWindow):
    """
    A class to control the interaction between the GUI and the voting logic.
    """

    def __init__(self):
        super().__init__()
        self.ui = Ui_voter_menu()  # Load the GUI
        self.ui.setupUi(self)  # Set up the UI components

        # Initialize voting logic
        self.logic = VotingLogic()

        # Make feedback labels hidden initially
        self.ui.vote_error.hide()
        self.ui.vote_success.hide()
        self.ui.already_voted.hide()

        # Connect the submit button to the vote submission function
        self.ui.vote_button.clicked.connect(self.submit_vote)

    def submit_vote(self) -> None:
        """
        Handle the vote submission process, including validation and recording.
        """
        nuid: str = self.ui.user_NUID.text().strip()  # Retrieve the NUID

        # Validate the NUID
        if not self.logic.is_valid_nuid(nuid):
            self.display_label('error')
            return

        # Determine the selected candidate
        if self.ui.vote_will.isChecked():
            candidate: str = 'Will'
        elif self.ui.vote_max.isChecked():
            candidate: str = 'Max'
        elif self.ui.vote_custom.isChecked():
            candidate = self.ui.custom_vote.text().strip()
            if not candidate:
                self.display_label('error')
                return
        else:
            self.display_label('error')
            return

        # Check if the voter has already voted
        if self.logic.has_voter_already_voted(nuid):
            self.display_label('already_voted')
        else:
            self.logic.record_vote(nuid, candidate)
            self.display_label('success')

        # Clear the custom vote field after submission
        self.ui.custom_vote.clear()

    def display_label(self, label_type: str) -> None:
        """
        Display the appropriate label based on the result of the operation.
        """
        # Hide all labels before showing the appropriate one
        self.ui.vote_error.hide()
        self.ui.vote_success.hide()
        self.ui.already_voted.hide()

        if label_type == 'error':
            self.ui.vote_error.show()
        elif label_type == 'success':
            self.ui.vote_success.show()
        elif label_type == 'already_voted':
            self.ui.already_voted.show()