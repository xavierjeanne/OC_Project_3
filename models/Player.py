class Player:
    """Represents a chess player with personal information"""

    def __init__(self, last_name, first_name, birth_date, national_id):
        """Initialize a player with their personal details

        Args:
            last_name (str): Player's last name
            first_name (str): Player's first name
            birth_date (str): Player's birth date
            national_id (str): Player's national identification number
        """
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.national_id = national_id

    def to_dict(self):
        """Convert player data to dictionary format for storage

        Returns:
            dict: Player data in dictionary format
        """
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        """Create a Player instance from dictionary data

        Args:
            data (dict): Dictionary containing player data

        Returns:
            Player: New Player instance with loaded data, or None if data is None
        """
        if data is None:
            return None
        return cls(
            last_name=data["last_name"],
            first_name=data["first_name"],
            birth_date=data["birth_date"],
            national_id=data["national_id"]
        )
