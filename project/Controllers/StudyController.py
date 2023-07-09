from Core import Controller
from Core import MSDatabase as ms
from Models.Study import Study


class StudyController(Controller.Controller):
    """
    Retrieves a study record from the database based on the provided study ID.

    Args:
        self: The instance of the StudyController class.
        db: The database session object.
        study_id: The ID of the study to retrieve.

    Returns:
        The study record matching the provided study ID, or None if not found.
    """
    def get_study(self, db: ms.Session, study_id: int):
        return db.query(Study).filter(Study.studyUID == study_id).first()