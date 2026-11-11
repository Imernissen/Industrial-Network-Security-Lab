
def detecter_trafic_excessif(temps, fenetre=0.010, seuil=3):
    temps = sorted(temps)

    gauche = 0
    maximum = 0

    for droite in range(len(temps)):
        while temps[droite] - temps[gauche] > fenetre:
            gauche += 1

        nombre = droite - gauche + 1
        maximum = max(maximum, nombre)

    return maximum > seuil


def test_trafic_normal():
    temps = [0.0, 0.020, 0.040]
    assert detecter_trafic_excessif(temps) is False


def test_trafic_excessif():
    temps = [0.001, 0.002, 0.003, 0.004, 0.005]
    assert detecter_trafic_excessif(temps) is True


def test_seuil_exact():
    temps = [0.001, 0.002, 0.003]
    assert detecter_trafic_excessif(temps) is False


def test_liste_vide():
    assert detecter_trafic_excessif([]) is False
