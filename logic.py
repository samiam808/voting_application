import csv
import os

class VotingLogic:
    """
    A class for handling the core logic of the voting application.
    """

    def __init__(self, csv_file_path='election.csv'):
        self.csv_file_path = csv_file_path
        self.initialize_csv()

    def initialize_csv(self) -> None:
        """
        Create the CSV file if it doesn't already exist.
        """
        if not os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['NUID', 'Candidate'])

    def is_valid_nuid(self, nuid: str) -> bool:
        """
        Check if the provided NUID is valid (8-digit numeric string).
        """
        return nuid.isdigit() and len(nuid) == 8

    def has_voter_already_voted(self, nuid: str) -> bool:
        """
        Check if a voter with the given NUID has already voted.

        Returns:
            bool: If the user already voted returns True, otherwise returns False
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
