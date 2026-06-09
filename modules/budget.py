def calculate_budget(dest_cost_usd, duration, num_people):
    """All values in USD. dest_cost_usd = daily cost per person."""
    accommodation = dest_cost_usd * duration
    food          = 30  * duration * num_people   # $30/day/person
    transport     = 50  * num_people              # $50/person
    activities    = 20  * duration * num_people   # $20/day/person
    miscellaneous = 10  * duration                # $10/day

    total = accommodation + food + transport + activities + miscellaneous

    breakdown = {
        "🏨 Accommodation": accommodation,
        "🍽️ Food & Drinks": food,
        "🚌 Transport":     transport,
        "🎯 Activities":    activities,
        "🛍️ Miscellaneous": miscellaneous,
    }
    return breakdown, total