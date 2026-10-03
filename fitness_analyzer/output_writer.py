from pathlib import Path
import csv
from .session_analyzer import SessionAnalyzer


def create_output_folder(output_directory):
    output_folder = Path(output_directory)
    output_folder.mkdir(exist_ok=True)
    return output_folder

def write_analysis_summary(output_folder, results):
    output_file = output_folder / "analysis_summary.csv"

    with open(output_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames = results[0].keys()
            # results = [{"session_id":"FIT-2026-001",
            #             "participant_id":"P001",
            #             ...},
            #            {"session_id":"FIT-2026-002",
            #             "participant_id":"P002",
            #             ...}]
            # results[0] -> first dictionary
            # .keys() -> gets its column names
            # -> those will be the CSV header
        )
        writer.writeheader()
        writer.writerows(results)

    return output_file


# sessions = {
#    "FIT-2026-001": FitnessSession(...),
#    "FIT-2026-002": FitnessSession(...),
#    "FIT-2026-003": FitnessSession(...),
#    "FIT-2026-004": FitnessSession(...),
#    "FIT-2026-005": FitnessSession(...)
# }
# --> ANALYZE ONE SESSION: 
# a = SessionAnalyzer(sessions["FIT-2026-001"])
# a.get_results()

def write_analysis_report(output_folder, sessions):
    output_file = output_folder / "analysis_report.txt"

    with open(output_file,"w",encoding="utf-8") as file:
        for session in sessions.values():
            analyzer = SessionAnalyzer(session)
            report = analyzer.nicely_presented_results()

            file.write(report)
            file.write("\n\n")

    return output_file


def write_rejected_records(output_folder, rejected_records):
    output_file = output_folder / "rejected_records.txt"

    with open(output_file,"w",encoding="utf-8") as file:
        for record in rejected_records:
            file.write(
                f"File: {record['filename']}, "
                f"Row: {record['row_number']}, "
                f"Field: {record['field']}, "
                f"Reason: {record['reason']}\n"                
            )
    return output_file