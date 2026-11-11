
def detecter_ip_non_autorisee(adresses, ips_autorisees):
    return [
        adresse for adresse in adresses
        if adresse not in ips_autorisees
    ]


def test_ip_autorisee():
    adresses = ["127.0.0.1"]
    ips_autorisees = ["127.0.0.1"]

    assert detecter_ip_non_autorisee(
        adresses, ips_autorisees
    ) == []


def test_ip_non_autorisee():
    adresses = ["192.168.1.100"]
    ips_autorisees = ["127.0.0.1"]

    assert detecter_ip_non_autorisee(
        adresses, ips_autorisees
    ) == ["192.168.1.100"]


def test_liste_vide():
    assert detecter_ip_non_autorisee([], ["127.0.0.1"]) == []
