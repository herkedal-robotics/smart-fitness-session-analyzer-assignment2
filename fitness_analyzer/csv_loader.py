import csv
from .participant import Participant
from .fitness_session import FitnessSession
from .observation import Observation
from .exceptions import InvalidIdentifierError, InvalidRecordError


from .validators import (
    validate_participant_id,
    validate_session_id,
    validate_timestamp,
    validate_heart_rate,
    validate_skin_response,
    validate_temperature,
    validate_activity_level,
    validate_signal_quality
)

def load_participants(filename):
    participants = {}
    rejected_records = []

    try:
        file = open(filename, "r", encoding="utf-8", newline="")

    except FileNotFoundError:
        print(f"File {filename} not found.")
        return participants, rejected_records

    except PermissionError:
        print(f"Permission to file {filename} denied.")
        return participants, rejected_records

    with file:
        reader = csv.DictReader(file)

        #for row in reader:
        try:
            for row_number, row in enumerate(reader, start=2):  # LOOP 1, CSV rows
                # now, ex. we want (id,name,heart_rate)
                # but we get (id,name,heart_rate, EXTRA)
                # DictReader produces {"id":"P001",
                #                      "name":"Rilakkuma",
                #                      "heart_rate":"80",
                #                      None: ["EXTRA"]}
                # so we want to reject those that have more fields than expected
                if None in row:
                    rejected_records.append({
                        "filename": filename,
                        "row_number": row_number,
                        "field": "row",
                        "reason": "Unexpected number of fields."})
                    continue



                has_missing_value = False

                for field in row:                               # LOOP 2, fields
                    if row[field] is None or row[field] == "":
                        rejected_records.append({
                            "filename": filename,
                            "row_number": row_number,
                            "field": field,
                            "reason": "Missing required value."})
                        has_missing_value = True
                        break                                   # break LOOP 2

                if has_missing_value:
                    continue                                    # continue LOOP 1

                # first check if the ID has valid format (Pxxx):
                try:
                    validate_participant_id(row["participant_id"])
                except InvalidIdentifierError as error:
                    rejected_records.append({
                        "filename": filename,
                        "row_number": row_number,
                        "field": "participant_id",
                        "reason": str(error)})
                    continue

                try:
                    field = "baseline_heart_rate"
                    baseline_heart_rate = int(row["baseline_heart_rate"])
                    field = "baseline_skin_response"
                    baseline_skin_response = float(row["baseline_skin_response"])
                    field = "baseline_temperature"
                    baseline_temperature = float(row["baseline_temperature"])
                except ValueError as error:
                    rejected_records.append({
                        "filename": filename,
                        "row_number": row_number,
                        "field": field,
                        "reason": str(error)})
                    continue


                # then we convert some data from str into int and float
                participant = Participant(
                    participant_id=row["participant_id"],
                    name=row["name"],
                    baseline_heart_rate=int(row["baseline_heart_rate"]),
                    baseline_skin_response=float(row["baseline_skin_response"]),
                    baseline_temperature=float(row["baseline_temperature"])
                )

                participants[participant.participant_id] = participant

        except csv.Error as error:
            print(f"CSV error in {filename}: {error}")


    return participants, rejected_records

# In terminal window:
# python -c "from csv_loader import load_participants; load_participants('data/participants.csv')"

# reader = csv.reader(file) gives us:
# ["P001", "Amina Noor", "68", "1.20", "32.4"]

# reader = csv.DictReader(file) gives us: 
# {'participant_id': 'P001', 'name': 'Amina Noor', 'baseline_heart_rate': '68', 'baseline_skin_response': '1.20', 'baseline_temperature': '32.4'}

def load_sessions(filename, participants):
    sessions = {}           # stores accepted data
    rejected_records = []   # stores rejected/invalid data

    try:
        file = open(filename, "r", encoding="utf-8", newline="")

    except FileNotFoundError:
        print(f"File {filename} not found.")
        return sessions, rejected_records

    except PermissionError:
        print(f"Permission to file {filename} denied.")
        return sessions, rejected_records

    with file:
        reader = csv.DictReader(file)

        #for row in reader:
        try:
            for row_number, row in enumerate(reader, start=2):
                #session_id = row["session_id"]
                #participant_id = row["participant_id"]

                # check if any field is missing or is empty:
                #if None in row.values() or "" in row.values():
                #    #print("Session has missing field/s.")
                #    print(f"Row {row_number} - Session has missing field/s.")
                #    continue

                # check if row has more fields than required:
                if None in row:
                    rejected_records.append({
                        "filename": filename,
                        "row_number": row_number,
                        "field": "row",
                        "reason": "Unexpected number of fields."})
                    continue


                # check if the row has a missing value
                has_missing_value = False  # assume there is no missing value

                for field in row:  # for every field in the row:                          # field = "activity_level"
                    if row[field] is None or row[field] == "":  # if field is missing:    # row["activity_level"]
                        # store information about the rejected row
                        rejected_records.append({               
                            "filename": filename,             
                            "row_number": row_number,         
                            "field": field,
                            "reason": "Missing required value."
                        })

                        has_missing_value = True  # remember that a missing value was found
                        break                                 

                if has_missing_value:
                    continue # skip this CSV row and move to the next one

                session_id = row["session_id"]
                participant_id = row["participant_id"]

                # check that session_id and participant_id have valid formats:
                try:
                    field = "session_id"
                    validate_session_id(session_id)
                    field = "participant_id"
                    validate_participant_id(participant_id)
                except InvalidIdentifierError as error:
                    #print(f"Invalid identifier: {error}")
                    #print(f"Row {row_number} - Invalid identifier: {error}")
                    rejected_records.append({
                        "filename": filename,
                        "row_number": row_number,
                        "field": field,
                        "reason": str(error)
                    })
                    continue

                #if session_id not in sessions:
                try:
                    participant = participants[participant_id]
                except KeyError:
                    #print(f"Participant with {participant_id} id does not exist.")
                    #print(f"Row {row_number} - Participant with {participant_id} id does not exist.")
                    rejected_records.append({
                        "filename": filename,
                        "row_number": row_number,
                        "field": "participant_id",
                        "reason": f"Participant with {participant_id} id does not exist."
                    })
                    continue

                #sessions[session_id] = FitnessSession(
                #    session_id = session_id,
                #    participant = participant
                # if we put obs here, we would only get one obs per session
                #)
                try:
                    field = "activity_level"
                    activity_level = float(row["activity_level"])
                    field = "timestamp"
                    timestamp = int(row["timestamp"])   # int("1") -> godkjent
                    field = "heart_rate"
                    heart_rate = int(row["heart_rate"]) # int("fast") -> ikke godkjent
                    field = "skin_response"
                    skin_response = float(row["skin_response"])
                    field = "temperature"
                    temperature = float(row["temperature"])
                    field = "signal_quality"
                    signal_quality = float(row["signal_quality"])
                except ValueError as error:
                    # error stores info about the error that occurred (with its message)
                    # so error = error object with message as part of its information
                    #print(f"Invalid data type: {error}")
                    #print(f"Row {row_number} - Invalid data type: {error}")
                    rejected_records.append({
                        "filename": filename,
                        "row_number": row_number,
                        "field": field,
                        "reason": str(error)})
                    continue
                
                try:
                    field = "activity_level"
                    validate_activity_level(activity_level)
                    field = "timestamp"
                    validate_timestamp(timestamp)
                    field = "heart_rate"
                    validate_heart_rate(heart_rate)
                    field = "skin_response"
                    validate_skin_response(skin_response)
                    field = "temperature"
                    validate_temperature(temperature)
                    field = "signal_quality"
                    validate_signal_quality(signal_quality)
                except InvalidRecordError as error:
                    #print(f"Invalid record: {error}")
                    #print(f"Row {row_number} - Invalid record: {error}")
                    rejected_records.append({
                        "filename": filename,
                        "row_number": row_number,
                        "field": field,
                        "reason": str(error)})
                    continue

                observation = Observation(
                    timestamp = timestamp,
                    heart_rate = heart_rate,
                    skin_response = skin_response,
                    temperature = temperature,
                    #activity_level = float(row["activity_level"]),
                    activity_level = activity_level,
                    signal_quality = signal_quality
                )
                if session_id not in sessions:
                    sessions[session_id] = FitnessSession(
                        session_id = session_id,
                        participant = participant)

                


                sessions[session_id].add_observation(observation)
                
        except csv.Error as error:
            print(f"CSV error in {filename}: {error}")          

    return sessions, rejected_records
