# helper functions

def get_city_choices(city_codes):
    return [(c.code, f"{c.name}") for c in city_codes]
