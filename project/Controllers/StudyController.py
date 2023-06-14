from Core import Controller
from Core import MSDatabase as ms
from Models.Study import Study


class StudyController(Controller.Controller):
    def get_study(self, db: ms.Session, study_id: int):
        return db.query(Study).filter(Study.studyUID == study_id).first()