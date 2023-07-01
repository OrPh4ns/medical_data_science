from Core import Controller
from Core import MSDatabase as ms
from Models.Patient import Patient


class PatientController(Controller.Controller):
    def get_patient(self, db: ms.Session, patient_id: int):
        # Query the database for a Patient object with the specified patient_id
        return db.query(Patient).filter(Patient.patientID == patient_id).first()
