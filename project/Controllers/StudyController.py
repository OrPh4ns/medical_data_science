from Core import Controller
from Core import MSDatabase as ms
from Models.Study import Study


class StudyController(Controller.Controller):
    def get_study(self, db: ms.Session, study_id: int):
        # Query the database for a Study object with the specified study_id
        return db.query(Study).filter(Study.studyUID == study_id).first()