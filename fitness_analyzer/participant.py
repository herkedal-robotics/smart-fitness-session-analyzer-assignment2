"""
store information about one person
"""
class Participant():
    def __init__(self,
                  participant_id,
                  name,
                  baseline_heart_rate,
                  baseline_skin_response,
                  baseline_temperature):
        self.participant_id = participant_id
        self.name = name
        self.baseline_heart_rate = baseline_heart_rate
        self.baseline_skin_response = baseline_skin_response
        self.baseline_temperature = baseline_temperature



#anna = Participant("P001", 78, 1.17, 32.76)

#print(anna.participant_id)
#print(anna.baseline_heart_rate)