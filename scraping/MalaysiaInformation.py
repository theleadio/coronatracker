from DatabaseConnector import db_malaysia_patient_cases, db_malaysia_states

# Root entity for the aggregate
class MalaysiaInformation:

    def __init__(self, date):
        this.date = date

    def dbStatesConnect(self):
        db_malaysia_states.connect()

    def dbPatientConnect(self):
        db_malaysia_patient_cases.connect()

    def stateInsert(data_dict, target_table):
        db_malaysia_states.insert(data_dict, target_table)

    def patientInsert(data_dict, target_table):
        db_malaysia_patient_cases.insert(data_dict, target_table)
