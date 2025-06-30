"""
DTO module for representing catalogue data.
"""
class Catalogue:
    """
    Data Transfer Object for a catalogue.

    :param name: Name of the catalogue
    :param description: Description of the catalogue
    :param start_date: Start date of the catalogue (YYYY-MM-DD)
    :param end_date: End date of the catalogue (YYYY-MM-DD)
    :param status: Status of the catalogue (active/inactive/upcoming/expired)
    :param catalogue_id: Optional ID for existing catalogues.
    """
    def __init__(self, name, description, start_date, end_date, status, catalogue_id=None):
        
        self.catalogue_id = catalogue_id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def to_dict(self):
        """Converts the Catalogue object to a dictionary for JSON serialization."""
        return {
            "catalogue_id": self.catalogue_id,
            "name": self.name,
            "description": self.description,
            "start_date": str(self.start_date), 
            "end_date": str(self.end_date),
            "status": self.status
        }