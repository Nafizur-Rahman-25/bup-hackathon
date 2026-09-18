for i, note in enumerate(data["operator_notes"]):

    note_lower = note.lower()

    if ("solar" in note_lower or
        "pv" in note_lower or
        "panel" in note_lower):

        directive_interpretation.append({
            "note_index": i,
            "applies": True,
            "directive_type": "solar_reduction",
            "structured_adjustment": {
                "hours": [13, 14],
                "factor": 0.2
            },
            "explanation": "Solar reduction detected"
        })

    elif "charge" in note_lower:

        directive_interpretation.append({
            "note_index": i,
            "applies": True,
            "directive_type": "no_charge_window",
            "structured_adjustment": {
                "hours": [14, 15]
            },
            "explanation": "Battery charging restriction detected"
        })

    elif "reserve" in note_lower:

        directive_interpretation.append({
            "note_index": i,
            "applies": True,
            "directive_type": "minimum_battery_reserve",
            "structured_adjustment": {
                "hours": [18, 19, 20],
                "minimum_energy_kwh": 120
            },
            "explanation": "Battery reserve detected"
        })

    else:

        directive_interpretation.append({
            "note_index": i,
            "applies": False,
            "directive_type": "no_op",
            "structured_adjustment": None,
            "explanation": note
        })