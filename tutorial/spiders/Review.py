"""Review class for reviews pulled from the Internet."""


class Review():
    """Review class for reviews pulled from the web."""

    def __init__(self, text, business_name=None, date=None, rating=None):
        """Constructor: review text only required."""
        self.review_text = text
        self.business_name = business_name
        self.rating = rating
        self.date = date

    def __str__(self):
        """Return string representation of object."""
        return self.review_text
