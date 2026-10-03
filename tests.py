from fitness_analyzer.observation import Observation
from fitness_analyzer.participant import Participant
from fitness_analyzer.fitness_session import FitnessSession
from fitness_analyzer.session_analyzer import SessionAnalyzer
from fitness_analyzer.csv_loader import load_participants, load_sessions


def test_observation_validation():
    valid_observation = Observation(
        timestamp=0,
        heart_rate=75,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.5,
        signal_quality=0.95,
    )

    invalid_observation = Observation(
        timestamp=1,
        heart_rate=275,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.5,
        signal_quality=0.95,
    )

    assert valid_observation.is_valid() is True
    assert invalid_observation.is_valid() is False

    print("Observation validation test passed!")


test_observation_validation()


def test_get_results():
    participant = Participant(
        participant_id="P001",
        name="Test Participant",
        baseline_heart_rate=90,
        baseline_skin_response=2.0,
        baseline_temperature=36.5
    )

    session = FitnessSession(
        session_id="FIT-2026-001",
        participant=participant
    )
    observation1 = Observation(
        timestamp=0,
        heart_rate=130,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.7,
        signal_quality=0.9
    )

    observation2 = Observation(
        timestamp=1,
        heart_rate=150,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.7,
        signal_quality=0.9
    )

    observation3 = Observation(
        timestamp=2,
        heart_rate=140,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.7,
        signal_quality=0.9
    )

    session.add_observation(observation1)
    session.add_observation(observation2)
    session.add_observation(observation3)

    analyzer = SessionAnalyzer(session)
    result = analyzer.get_results()

    assert result["invalid_observations"] == 0
    assert result["minimum_heart_rate"] == 130
    assert result["maximum_heart_rate"] == 150
    assert result["average_heart_rate"] == 140
    assert result["heart_rate_change"] == 50
    assert result["average_temp_change"] == 0
    #assert result["average_activity_level"] == 0.7
    assert abs(result["average_activity_level"] - 0.7) < 0.000001
    assert result["classification"] == "high_activity"

    print("Get_results test passed!")


test_get_results()


def test_invalid_observation_is_excluded():
    participant = Participant(
        participant_id="P002",
        name="Test Participant",
        baseline_heart_rate=70,
        baseline_skin_response=2.0,
        baseline_temperature=36.5
    )

    session = FitnessSession(
        session_id="FIT-2026-002",
        participant=participant
    )

    valid_observation1 = Observation(
        timestamp=0,
        heart_rate=100,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.4,
        signal_quality=0.9
    )

    valid_observation2 = Observation(
        timestamp=1,
        heart_rate=100,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.4,
        signal_quality=0.9
    )

    valid_observation3 = Observation(
        timestamp=2,
        heart_rate=100,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.4,
        signal_quality=0.9
    )

    invalid_observation = Observation(
        timestamp=3,
        heart_rate=265,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.9,
        signal_quality=0.9
    )

    session.add_observation(valid_observation1)
    session.add_observation(valid_observation2)
    session.add_observation(valid_observation3)
    session.add_observation(invalid_observation)

    analyzer = SessionAnalyzer(session)
    result = analyzer.get_results()

    assert result["valid_observations"] == 3
    assert result["invalid_observations"] == 1

    assert result["minimum_heart_rate"] == 100
    assert result["maximum_heart_rate"] == 100
    assert result["average_heart_rate"] == 100
    assert result["heart_rate_change"] == 30
    assert result["average_temp_change"] == 0
    assert abs(result["average_activity_level"] - 0.4) < 0.000001
    assert result["classification"] == "moderate_activity"

    print("Invalid observation exclusion test passed!")

test_invalid_observation_is_excluded()


def test_insufficient_data():
    participant = Participant(
        participant_id="P003",
        name="Test Participant",
        baseline_heart_rate=70,
        baseline_skin_response=2.0,
        baseline_temperature=36.5
    )
    session = FitnessSession(
        session_id="FIT-2026-003",
        participant=participant
    )
    invalid_observation = Observation(
        timestamp=0,
        heart_rate=265,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.4,
        signal_quality=0.2
    )
    session.add_observation(invalid_observation)

    analyzer = SessionAnalyzer(session)
    result = analyzer.get_results()

    assert result["valid_observations"] == 0
    assert result["invalid_observations"] == 1
    assert result["average_heart_rate"] is None
    assert result["heart_rate_change"] is None
    assert result["minimum_heart_rate"] is None
    assert result["maximum_heart_rate"] is None
    assert result["average_temp_change"] is None
    assert result["average_activity_level"] is None
    assert result["classification"] == "insufficient_data"
    print("Insufficient data test passed!")

test_insufficient_data()


def test_recovery_classification():
    participant = Participant(
        participant_id="P004",
        name="Test Participant",
        baseline_heart_rate=70,
        baseline_skin_response=2.0,
        baseline_temperature=36.5
    )
    session = FitnessSession(
        session_id="FIT-2026-004",
        participant=participant
    )
    observation1 = Observation(
        timestamp=0,
        heart_rate=160,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.8,
        signal_quality=0.9
    )
    observation2 = Observation(
        timestamp=1,
        heart_rate=150,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.6,
        signal_quality=0.9
    )
    observation3 = Observation(
        timestamp=2,
        heart_rate=140,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.4,
        signal_quality=0.9
    )

    session.add_observation(observation1)
    session.add_observation(observation2)
    session.add_observation(observation3)

    analyzer = SessionAnalyzer(session)
    result = analyzer.get_results()

    assert result["participant_id"] == "P004"
    assert result["valid_observations"] == 3
    assert result["invalid_observations"] == 0
    assert result["average_heart_rate"] == 150
    assert result["heart_rate_change"] == 80
    assert result["minimum_heart_rate"] == 140
    assert result["maximum_heart_rate"] == 160
    assert result["average_temp_change"] == 0
    assert abs(result["average_activity_level"] - 0.6) < 0.000001
    assert result["classification"] == "recovery"
    print("Recovery classification test passed!")

test_recovery_classification()


def test_resting_classification():
    participant = Participant(
        participant_id="P005",
        name="Test Participant",
        baseline_heart_rate=70,
        baseline_skin_response=2.0,
        baseline_temperature=36.5
    )
    session = FitnessSession(
        session_id="FIT-2026-005",
        participant=participant
    )
    observation1 = Observation(
        timestamp=0,
        heart_rate=100,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.2,
        signal_quality=0.9
    )
    observation2 = Observation(
        timestamp=1,
        heart_rate=80,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.2,
        signal_quality=0.9
    )
    observation3 = Observation(
        timestamp=2,
        heart_rate=60,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.2,
        signal_quality=0.9
    )

    session.add_observation(observation1)
    session.add_observation(observation2)
    session.add_observation(observation3)

    analyzer = SessionAnalyzer(session)
    result = analyzer.get_results()

    assert result["participant_id"] == "P005"
    assert result["valid_observations"] == 3
    assert result["invalid_observations"] == 0
    assert result["average_heart_rate"] == 80
    assert result["heart_rate_change"] == 10
    assert abs(result["average_activity_level"] - 0.2) < 0.000001
    assert result["classification"] == "resting"

    print("Resting classification test passed!")

test_resting_classification()

def test_load_valid_participants():
    participants, rejected_records = load_participants(
        "data/participants.csv"
    )

    assert len(participants) == 3
    assert len(rejected_records) == 0

    assert "P001" in participants
    assert "P002" in participants
    assert "P003" in participants

    print("Valid participants CSV test passed!")

test_load_valid_participants()

def test_load_valid_sessions():
    participants, participant_rejected = load_participants(
        "data/participants.csv"
    )
    sessions, rejected_records = load_sessions(
        "data/fitness_sessions.csv",
        participants
    )
    assert len(sessions) == 5
    assert len(rejected_records) == 0
    assert "FIT-2026-001" in sessions
    assert "FIT-2026-002" in sessions
    assert "FIT-2026-003" in sessions
    assert "FIT-2026-004" in sessions
    assert "FIT-2026-005" in sessions

    print("Valis sessions CSV test passed!")

test_load_valid_sessions()

def test_load_invalid_sessions():
    participants, participant_rejected = load_participants(
        "data/participants.csv"
    )
    sessions, rejected_records = load_sessions(
        "data/fitness_sessions_invalid.csv",
        participants
    )

    assert len(sessions) == 1
    assert len(rejected_records) == 10
    assert "FIT-2026-101" in sessions

    print("Invalid sessions CSV test passed!")

test_load_invalid_sessions()


def test_missing_sessions_file():
    participants, participant_rejected = load_participants(
        "data/participants.csv"
    )
    sessions, rejected_records = load_sessions(
        "data/does_not_exist.csv",
        participants
    )
    assert sessions == {}
    assert rejected_records == []
    print("Missing sessions file test passed!")

test_missing_sessions_file()

def test_heart_rate_boundaries():
    observation_minimum = Observation(
        timestamp=0,
        heart_rate=35,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.5,
        signal_quality=0.9
    )
    observation_maximum = Observation(
        timestamp=1,
        heart_rate=205,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.5,
        signal_quality=0.9
    )
    observation_below = Observation(
        timestamp=2,
        heart_rate=34,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.5,
        signal_quality=0.9
    )
    observation_above = Observation(
        timestamp=3,
        heart_rate=206,
        skin_response=2.0,
        temperature=36.5,
        activity_level=0.5,
        signal_quality=0.9
    )

    assert observation_minimum.is_valid() is True
    assert observation_maximum.is_valid() is True
    assert observation_below.is_valid() is False
    assert observation_above.is_valid() is False

    print("Heart rate boundary test passed!")

test_heart_rate_boundaries()