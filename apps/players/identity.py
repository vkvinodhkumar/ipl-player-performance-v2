PLAYER_ALIASES = {
    "Arshad Khan (2)": "Arshad Khan",
}


def canonical_player_name(name):
    return PLAYER_ALIASES.get(name, name)


def source_player_names(name):
    return [
        source_name
        for source_name, canonical_name in PLAYER_ALIASES.items()
        if canonical_name == name
    ] + [name]
