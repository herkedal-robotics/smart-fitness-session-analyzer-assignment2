class SessionAnalyzer:
    def __init__(self, session):
        self.session = session

    def count_valid_observations(self):
        valid_count = 0
        invalid_count = 0
        for observation in self.session.observations:
            if observation.is_valid():
                valid_count += 1
            else:
                invalid_count += 1
        return valid_count, invalid_count
    
    def average_heart_rate(self):
        #length = len(self.session.observations)
        total = 0
        count = 0
        for i in range(len(self.session.observations)):
            if self.session.observations[i].is_valid():
                total += self.session.observations[i].heart_rate
                count += 1
        if count == 0:
            return None
        return total/count

    def heart_rate_change(self):
        #average - base
        average = self.average_heart_rate()
        if average is None:
            return None
        baseline = self.session.participant.baseline_heart_rate
        #change = average - baseline
        return average - baseline

    def average_activity_level(self):
        # sum of activity_level / number of valid values
        total = 0
        count = 0
        for i in range(len(self.session.observations)):
            if self.session.observations[i].is_valid():
                total += self.session.observations[i].activity_level
                count += 1
        if count == 0:
            return None
        return total/count

    def min_max_heart_rate(self):
        heart_rates_list = []
        count = 0
        for i in range(len(self.session.observations)):
            if self.session.observations[i].is_valid():
                heart_rates_list.append(self.session.observations[i].heart_rate)
                count += 1
        if count == 0:
            return None
        min_heart_rate = min(heart_rates_list) 
        max_heart_rate = max(heart_rates_list)
        return min_heart_rate,max_heart_rate #ex (60,100)

    """
    def minimum_heart_rate(self):
        result = self.min_max_heart_rate()
        if result is None:
            return None
        minimum,maximum = result
        return minimum

    def maximum_heart_rate(self):
        result = self.min_max_heart_rate()
        if result is None:
            return None
        minimum,maximum = result
        return maximum
    """

    def average_temp_change(self):
        """
        first calculate the average temperature
        then subtract it from baseline
        """
        #length = len(self.session.observations)
        total = 0
        count = 0
        for i in range(len(self.session.observations)):
            if self.session.observations[i].is_valid():
                total += self.session.observations[i].temperature
                count += 1
        if count == 0:
            return None
        average = total/count
        return average - self.session.participant.baseline_temperature      

    """
    def classify_session(self):
        valid, invalid = self.count_valid_observations()
        if valid == 0:
            return "insufficient_data"
        if self.average_activity_level() < 0.3 and abs(self.heart_rate_change) <=15:
            return "resting"
        if self.average_activity_level() >= 0.3 and self.average_activity_level() < 0.6 and self.heart_rate_change() < 30:
            return "moderate_activity"
        if self.average_activity_level() >= 0.6 and self.heart_rate_change() >= 30:
            return "high_activity"
        if self.session.observations[9].heart_rate < self.session.observations[0].heart_rate:
            return "recovery"
        return "something_else"
    """
    def classify_session(self):
        valid, invalid = self.count_valid_observations()
        if valid < 3:
            return "insufficient_data"
        activity = self.average_activity_level()
        hr_change = self.heart_rate_change()

        # Collect valid observations
        valid_observations = []
        for observation in self.session.observations:
            if observation.is_valid():
                valid_observations.append(observation)

        # Check recovery
        if len(valid_observations) >= 3:
            first = valid_observations[0]
            last = valid_observations[-1]

            activity_drop = first.activity_level - last.activity_level
            heart_rate_drop = first.heart_rate - last.heart_rate

            if activity_drop >= 0.3 and heart_rate_drop >= 20:
                return "recovery"

        # Check resting
        if activity < 0.3 and abs(hr_change) <= 15:
            return "resting"
        # Check moderate activity
        if activity >= 0.3 and activity < 0.6:
            return "moderate_activity"
        # Check high activity
        if activity >= 0.6:
            return "high_activity"
        return "unclassified"

    def classification_explanation(self):
        classification = self.classify_session()

        if classification == "insufficient_data":
            return "Not enough valid observations were available."
        if classification == "recovery":
            return "Heart rate and activity levels declined at the end of the session."
        if classification == "resting":
            return "Average activity was low, average heart rate was close to baseline."
        if classification == "moderate_activity":
            return "Average activity level was between 0.3-0.6."
        if classification == "high_activity":
            return "Average activity level was over 0.6."
        return "Session did not match any current classification rules."

    def get_results(self):
        valid,invalid = self.count_valid_observations()

        heart_rate_range = self.min_max_heart_rate()

        if heart_rate_range is None:
            minimum = None
            maximum = None
        else:
            minimum, maximum = heart_rate_range

        results = {
            "session_id": self.session.session_id,
            "participant_id": self.session.participant.participant_id,
            "valid_observations": valid,
            "invalid_observations": invalid,
            "minimum_heart_rate": minimum,
            "maximum_heart_rate": maximum,
            "average_heart_rate": self.average_heart_rate(),
            "heart_rate_change": self.heart_rate_change(),
            "average_temp_change": self.average_temp_change(),
            "average_activity_level": self.average_activity_level(),
            "classification": self.classify_session(),
            "classification_explanation": self.classification_explanation()
            
        }
        return results

    # THIS WAS GOOD FOR ASSIGNMENT1:
    #def nicely_presented_results(self):
    #    results = self.get_results()
    #    print("Participant: ", results["participant_id"])
    #    print("Valid observations: ", results["valid_observations"])
    #    print("Invalid observations: ", results["invalid_observations"])
    #    print("")
    #    print("Minimum heart rate: ", format_number(results["minimum_heart_rate"]), "bpm")
    #    print("Maximum heart rate: ", format_number(results["maximum_heart_rate"]), "bpm")
    #    print("Average heart rate: ", format_number(results["average_heart_rate"]), "bpm")
    #    print("Heart rate change: ", format_number(results["heart_rate_change"]), "bpm")
    #    print("Average temp change: ", format_number(results["average_temp_change"]), "C")
    #    print("Average activity level: ", format_number(results["average_activity_level"]))
    #    print("")
    #    print("Classification: ", results["classification"])
    #    print("Explanation:", results["classification_explanation"])

    #THIS IS GOOD FOR ASSIGNMENT2:
    def nicely_presented_results(self):
        results = self.get_results()

        report = (
            f"Session: {results['session_id']}\n"
            f"Participant: {results['participant_id']}\n"
            f"Valid observations: {results['valid_observations']}\n"
            f"Invalid observations: {results['invalid_observations']}\n"
            f"\n"
            f"Minimum heart rate: {format_number(results['minimum_heart_rate'])} bpm\n"
            f"Maximum heart rate: {format_number(results['maximum_heart_rate'])} bpm\n"
            f"Average heart rate: {format_number(results['average_heart_rate'])} bpm\n"
            f"Heart rate change: {format_number(results['heart_rate_change'])} bpm\n"
            f"Average temp change: {format_number(results['average_temp_change'])} C\n"
            f"Average activity level: {format_number(results['average_activity_level'])}\n"
            f"\n"
            f"Classification: {results['classification']}\n"
            f"Explanation: {results['classification_explanation']}"
        )

        return report


def format_number(value):
    if value is None:
        return "N/A"
    return f"{value:.2f}"