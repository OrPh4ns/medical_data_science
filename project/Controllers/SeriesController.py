from Core import Controller
from Core import MSDatabase as ms
from Models.Series import Series


class SeriesController(Controller.Controller):
    def get_series(self, db: ms.Session, series_id: int):
        return db.query(Series).filter(Series.seriesUID == series_id).first()