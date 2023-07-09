from Core import Controller
from Core import MSDatabase as ms
from Models.Patient import Patient


class PatientController(Controller.Controller):
    """
    Retrieves a patient record from the database based on the provided patient ID.

    Args:
        self: The instance of the PatientController class.
        db: The database session object.
        patient_id: The ID of the patient to retrieve.

    Returns:
        The patient record matching the provided patient ID, or None if not found.
    """
    def get_patient(self, db: ms.Session, patient_id: int):
        return db.query(Patient).filter(Patient.patientID == patient_id).first()
