# Smart Fitness Session Analyzer (Option A)

**Student:** Beata, s376634

## Description

This program analyzes simulated fitness sessions from CSV files. It checks and validates measurements, calculates minimum, maximum and average values, compares measurements with each participant's baseline, and classifies each session. It also reports invalid observations and rejected CSV records.

The program is an extension of the Smart Fitness Session Analyzer from Assignment I.

## Input files

The program uses the official CSV files:

- `data/participants.csv`
- `data/fitness_sessions.csv`
- `data/fitness_sessions_invalid.csv`

The participant file contains participant information and baseline measurements. The session files contain fitness observations. Observations are grouped by session ID and connected to an existing participant.

## Package and class design

The main program is organized in the `fitness_analyzer` package.

- `Participant` - stores the participant's information and baseline measurements.
- `Observation` - stores one sensor reading and checks whether it is valid.
- `FitnessSession` - brings together a participant and their observations.
- `SessionAnalyzer` - calculates results, classifies the session and creates the report.
- `csv_loader` - reads and validates the CSV input files.
- `validators` - contains identifier and measurement validation functions.
- `exceptions` - contains custom exception classes.
- `output_writer` - creates and writes the output files.

**Composition:** The classes work together. `FitnessSession` stores a participant and their observations. `SessionAnalyzer` uses the session to calculate results and classify it. I used composition instead of inheritance because the participant, observations, session and analyzer have different jobs. None of them needs to be a special type of another class. Therefore, inheritance and method overriding are not needed in this project.

**Encapsulation:** `FitnessSession` stores the observation list in `_observations`. The `observations` property allows reading the observations, while `add_observation()` is used to add new observations.

## Validation

Participant IDs must have the format `P` followed by three digits, for example `P001`.

Fitness session IDs must have the format `FIT-XXXX-YYY`, for example `FIT-2026-001`.

The program also checks for:

- missing required values
- unexpected number of fields
- values that cannot be converted to the required type
- unknown participant IDs
- invalid identifier formats
- impossible or out-of-range measurements

The following measurement rules are used:

- timestamp must be non-negative
- heart rate must be between 35 and 205 bpm
- skin response must be non-negative
- temperature must be between 25 and 42 degrees Celsius
- activity level must be between 0 and 1
- signal quality must be between 0 and 1

The heart-rate and temperature limits were chosen by student for this program.

Signal quality below `0.7` is treated as poor-quality data. These observations are not used in the session analysis.

Rejected CSV records are stored with the source filename, row number, field and reason for rejection.

## Assumptions and classification rules

Only valid observations are used in calculations.
Insufficient data and recovery are checked first:

- **Insufficient data:** fewer than three valid observations.
- **Recovery:** at least three valid observations, with a heart-rate drop of at least 20 bpm and an activity drop of at least 0.3 from the first to the last valid observation.
- **Resting:** average activity below 0.3 and average heart rate within 15 bpm of baseline.
- **Moderate activity:** average activity from 0.3 to below 0.6.
- **High activity:** average activity of at least 0.6.

## Error handling

The program uses targeted error handling so that it can continue safely when possible.

It handles errors such as:

- `FileNotFoundError`
- `PermissionError`
- `ValueError`
- `KeyError`
- `csv.Error`

The program also defines and uses two custom exceptions:

- `InvalidIdentifierError`
- `InvalidRecordError`

## Output files

The program creates the output folder if it does not already exist and writes:

```text
output/
├── analysis_summary.csv
├── analysis_report.txt
└── rejected_records.txt
```

`analysis_summary.csv` contains one row per session.

`analysis_report.txt` contains a readable explanation of the analysis results.

`rejected_records.txt` contains information about rejected CSV rows and the reason why it was rejected.

Running the program again replaces the previous output files.

## Run the program and tests

Clone the repository and open its folder:

```bash
git clone https://github.com/herkedal-robotics/smart-fitness-session-analyzer-assignment2.git
cd smart-fitness-session-analyzer-assignment2
```

To analyze the valid fitness-session file on Windows:

```powershell
python main.py --profiles data/participants.csv --sessions data/fitness_sessions.csv --output output
```

To analyze the intentionally invalid fitness-session file:

```powershell
python main.py --profiles data/participants.csv --sessions data/fitness_sessions_invalid.csv --output output
```

On Linux/macOS, `python3` can be used instead of `python`.

Run the tests with:

```powershell
python tests.py
```

or:

```bash
python3 tests.py
```

No third-party packages are required. The project uses Python and the standard library.

## Example completion summary

For the valid session file:

```text
Accepted rows: 29
Rejected rows: 0
Processed sessions: 5
Created: output\analysis_summary.csv
Created: output\analysis_report.txt
Created: output\rejected_records.txt
```

For the intentionally invalid session file:

```text
Accepted rows: 1
Rejected rows: 10
Processed sessions: 1
Created: output\analysis_summary.csv
Created: output\analysis_report.txt
Created: output\rejected_records.txt
```

## Tests

The tests cover:

- observation validation
- analysis calculations
- invalid observation exclusion
- insufficient data
- recovery classification
- resting classification
- loading valid participant data
- loading valid session data
- loading intentionally invalid session data
- missing files
- boundary values

## Known limitations

The data is simulated. Classification uses fixed thresholds and does not provide medical or fitness advice. Recovery is based on the first and last valid observations rather than a detailed trend analysis.