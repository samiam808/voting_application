from PyQt6 import QtWidgets
from ui_controller import VotingController  # Import the controller class


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)  # Create the application instance
    window = VotingController()  # Create the voting controller (main window)
    window.show()  # Display the window
    sys.exit(app.exec())  # Execute the application event loop