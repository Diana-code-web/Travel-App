def generate_itinerary(destination, duration, activities):
    # Sample activities for each time of day
    morning_options = [
        "Visit local markets and grab breakfast",
        "Early morning nature walk",
        "Visit a nearby landmark or viewpoint",
        "Guided tour of the area",
        "Photography walk around the destination",
    ]

    afternoon_options = [
        "Explore local cuisine at a restaurant",
        "Visit a museum or cultural center",
        "Join a group activity or excursion",
        "Relax and explore at your own pace",
        "Shopping for local souvenirs",
    ]

    evening_options = [
        "Sunset viewing at a scenic spot",
        "Dinner at a recommended local restaurant",
        "Evening cultural show or performance",
        "Bonfire or campfire experience",
        "Stroll through the town center",
    ]

    # Build day-by-day plan
    itinerary = {}

    for day in range(1, duration + 1):
        # Pick activity based on user interests for that day
        main_activity = activities[(day - 1) % len(activities)]
        morning = morning_options[(day - 1) % len(morning_options)]
        afternoon = afternoon_options[(day - 1) % len(afternoon_options)]
        evening = evening_options[(day - 1) % len(evening_options)]

        itinerary[f"Day {day}"] = {
            "Main Activity": f"{main_activity} at {destination}",
            "Morning": morning,
            "Afternoon": afternoon,
            "Evening": evening,
        }

    return itinerary