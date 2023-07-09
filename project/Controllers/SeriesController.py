from Core import Controller
from Core import MSDatabase as ms
from Models.Series import Series


class SeriesController(Controller.Controller):
    """
    Retrieves a series record from the database based on the provided series ID.

    Args:
        self: The instance of the SeriesController class.
        db: The database session object.
        series_id: The ID of the series to retrieve.

    Returns:
        The series record matching the provided series ID, or None if not found.
    """
    def get_series(self, db: ms.Session, series_id: int):
        return db.query(Series).filter(Series.seriesUID == series_id).first()