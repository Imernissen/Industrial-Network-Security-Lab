
def detecter_fonctions_non_autorisees(fonctions, fonctions_autorisees):
    return [
        fonction for fonction in fonctions
        if fonction not in fonctions_autorisees
    ]


def test_fonctions_autorisees():
    fonctions = ["1", "5"]
    autorisees = ["1", "5"]

    assert detecter_fonctions_non_autorisees(
        fonctions, autorisees
    ) == []


def test_fonction_non_autorisee():
    fonctions = ["1", "5"]
    autorisees = ["1"]

    assert detecter_fonctions_non_autorisees(
        fonctions, autorisees
    ) == ["5"]


def test_aucune_fonction():
    assert detecter_fonctions_non_autorisees([], ["1", "5"]) == []
