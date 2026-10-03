from fitness_analyzer.csv_loader import load_participants, load_sessions
from fitness_analyzer.session_analyzer import SessionAnalyzer
from fitness_analyzer.output_writer import (
    create_output_folder,
    write_analysis_summary,
    write_analysis_report,
    write_rejected_records
)
import argparse

parser = argparse.ArgumentParser(
    description="Analyze fitness session from CSV files."
)

parser.add_argument(
    "--profiles",
    required=True,
    help="Path to participants CSV file."
)

parser.add_argument(
    "--sessions",
    required=True,
    help="Path to fitness sessions CSV file."
)

parser.add_argument(
    "--output",
    required=True,
    help="Path to output folder."
)

args = parser.parse_args()

participants, participants_rejected = load_participants(
    #"data/participants.csv"
    args.profiles
)

sessions, sessions_rejected = load_sessions(
    #"data/fitness_sessions.csv",
    args.sessions,
    participants
)

accepted_rows = 0

# every accepted row becomes an observation, 
# so we can use this knowledge to count accepted rows:
for session in sessions.values():
    accepted_rows += len(session.observations)

rejected_records = participants_rejected + sessions_rejected

results = []

for session in sessions.values():
    analyzer = SessionAnalyzer(session)
    results.append(analyzer.get_results())


#print("Sessions:", len(sessions))
#print("Results:", len(results))
#print("Rejected:", len(rejected_records))

print("Accepted rows:", accepted_rows)
print("Rejected rows:", len(rejected_records))
print("Processed sessions:", len(sessions))

#output_folder = create_output_folder("output")
output_folder = create_output_folder(args.output)

summary_file = write_analysis_summary(output_folder,results)

print("Created:", summary_file)

report_file = write_analysis_report(output_folder, sessions)

print("created:", report_file)

rejected_file = write_rejected_records(output_folder, rejected_records)

print("Created:", rejected_file)