def calculate_total_score(consent, security, breach, children, sdf):
    total = (
        consent * 0.25 +
        security * 0.30 +
        breach * 0.20 +
        children * 0.15 +
        sdf * 0.10
    )
    return round(total, 2)


def calculate_penalty(data):
    penalty = 0

    if data["security"] < 60:
        penalty += 250

    if not data["breach_workflow"]:
        penalty += 200

    if data["children_data"] and not data["parental_consent"]:
        penalty += 200

    if data["is_sdf"] and not data["dpia_done"]:
        penalty += 150

    if data["consent"] < 50:
        penalty += 50

    return penalty


def calculate_risk(score, penalty):
    if penalty >= 400:
        return "Critical Risk"
    elif penalty >= 200:
        return "High Risk"
    elif score < 70:
        return "Moderate Risk"
    else:
        return "Low Risk"


# ✅ NEW FUNCTION (Added Only – No Original Logic Changed)
def calculate_section_status(data):
    # Section 8(5) – Security Safeguards
    if data["security"] >= 60:
        section_8_5 = "Compliant"
    else:
        section_8_5 = "Non-Compliant"

    # Section 8(6) – Breach Notification
    if data["breach_workflow"]:
        section_8_6 = "Compliant"
    else:
        section_8_6 = "Non-Compliant"

    # Section 9 – Children Data
    if data["children_data"] and not data["parental_consent"]:
        section_9 = "Non-Compliant"
    elif data["children_data"]:
        section_9 = "Compliant"
    else:
        section_9 = "Not Applicable"

    # Section 10 – SDF Obligations
    if data["is_sdf"] and not data["dpia_done"]:
        section_10 = "Non-Compliant"
    elif data["is_sdf"]:
        section_10 = "Compliant"
    else:
        section_10 = "Not Applicable"

    return {
        "section_8_5": section_8_5,
        "section_8_6": section_8_6,
        "section_9": section_9,
        "section_10": section_10,
    }