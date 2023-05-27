from Core import Controller
from Core import MSDatabase as ms
from Models.Patient import Patient

class PatientController(Controller.Controller):
    def get_patient(self, db: ms.Session, patient_id: int):
        return db.query(Patient.Patient).filter(Patient.Patient.patientID == patient_id).first()
