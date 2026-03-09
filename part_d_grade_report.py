# Part D - AI-Augmented Task
# Improved version of the AI-generated grade report function
# Uses defaultdict, dict comprehension, type hints, and safe .get() access

from collections import defaultdict


# ---- AI's original output (pasted as-is for reference) ----
# (See assignment document for full AI output and evaluation notes)

def merge_grade_report_ai(sem1: dict, sem2: dict) -> dict:
    """AI-generated version - has some issues noted in the document."""
    all_subjects = set(sem1.keys()) | set(sem2.keys())
    common_subjects = set(sem1.keys()) & set(sem2.keys())
    combined = {}
    for sub in all_subjects:
        grades = []
        if sub in sem1:
            grades.append(sem1[sub])
        if sub in sem2:
            grades.append(sem2[sub])
        combined[sub] = sum(grades) / len(grades)
    gpa1 = sum(sem1.values()) / len(sem1) if sem1 else 0
    gpa2 = sum(sem2.values()) / len(sem2) if sem2 else 0
    trend = "improving" if gpa2 > gpa1 else "declining" if gpa2 < gpa1 else "stable"
    return {
        "combined_gpa": sum(combined.values()) / len(combined),
        "trend": trend,
        "common_subjects": list(common_subjects),
    }


# ---- Improved version ----

def merge_grade_report(
    sem1: dict[str, float],
    sem2: dict[str, float]
) -> dict:
    """
    Merges two semester grade dicts and returns a report.

    Args:
        sem1: {subject: grade} for semester 1
        sem2: {subject: grade} for semester 2

    Returns:
        dict with combined_gpa, grade_trend, common_subjects,
        per-subject averages, and per-semester GPA
    """
    # Handle edge cases: both empty
    if not sem1 and not sem2:
        return {
            'combined_gpa': 0.0,
            'grade_trend': 'no data',
            'common_subjects': [],
            'subject_averages': {},
            'sem1_gpa': 0.0,
            'sem2_gpa': 0.0
        }

    all_subjects = set(sem1.keys()) | set(sem2.keys())

    # Group grades per subject using defaultdict
    subject_grades = defaultdict(list)
    for sub in all_subjects:
        if sub in sem1:
            subject_grades[sub].append(sem1.get(sub, 0))
        if sub in sem2:
            subject_grades[sub].append(sem2.get(sub, 0))

    # Per-subject average using dict comprehension
    subject_averages = {
        sub: round(sum(grades) / len(grades), 2)
        for sub, grades in subject_grades.items()
    }

    # GPA per semester (safe for single semester case)
    sem1_gpa = round(sum(sem1.values()) / len(sem1), 2) if sem1 else 0.0
    sem2_gpa = round(sum(sem2.values()) / len(sem2), 2) if sem2 else 0.0

    combined_gpa = round(
        sum(subject_averages.values()) / len(subject_averages), 2
    ) if subject_averages else 0.0

    # Trend: based on GPA change between semesters
    if not sem1:
        trend = 'no prior semester'
    elif not sem2:
        trend = 'no second semester'
    elif sem2_gpa > sem1_gpa + 0.1:
        trend = 'improving'
    elif sem2_gpa < sem1_gpa - 0.1:
        trend = 'declining'
    else:
        trend = 'stable'

    common_subjects = sorted(set(sem1.keys()) & set(sem2.keys()))

    return {
        'combined_gpa': combined_gpa,
        'grade_trend': trend,
        'common_subjects': common_subjects,
        'subject_averages': subject_averages,
        'sem1_gpa': sem1_gpa,
        'sem2_gpa': sem2_gpa
    }


# ---- Demo ----
if __name__ == "__main__":
    print("=" * 55)
    print("  Part D - Grade Report Merger")
    print("=" * 55)

    sem1 = {'Math': 7.5, 'Physics': 6.8, 'English': 8.0, 'Chemistry': 6.5}
    sem2 = {'Math': 8.2, 'Physics': 7.5, 'English': 8.0, 'Biology': 7.0}

    print("\n--- Normal case ---")
    report = merge_grade_report(sem1, sem2)
    for k, v in report.items():
        print(f"  {k}: {v}")

    print("\n--- Edge case: empty sem1 ---")
    report_edge = merge_grade_report({}, sem2)
    for k, v in report_edge.items():
        print(f"  {k}: {v}")

    print("\n--- Edge case: both empty ---")
    report_empty = merge_grade_report({}, {})
    for k, v in report_empty.items():
        print(f"  {k}: {v}")
