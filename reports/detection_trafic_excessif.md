
# Détection du trafic Modbus excessif

## Objectif

Ce mécanisme analyse une capture réseau Modbus TCP afin d'identifier les sources qui génèrent un nombre anormalement élevé de requêtes sur le port TCP 502.

## Environnement

- OpenPLC Runtime
- Modbus TCP
- Wireshark / TShark
- Python 3

## Principe de détection

Le script extrait les horodatages et les adresses IP sources des requêtes Modbus.

Il utilise une fenêtre glissante de 10 millisecondes pour calculer le nombre maximal de requêtes émises par une même adresse IP pendant cet intervalle.

Une alerte est générée lorsque le nombre de requêtes dépasse le seuil configuré.

Paramètres utilisés pour les tests :
- Fenêtre temporelle : 10 ms
- Seuil : plus de 3 requêtes

## Résultats des tests

### Test 1 : détection du trafic excessif

Résultat observé :
- Adresse IP source : 127.0.0.1
- Nombre total de requêtes analysées : 5
- Maximum dans une fenêtre de 10 ms : 5
- Résultat : alerte générée.

### Test 2 : absence d'alerte

Le seuil a temporairement été fixé à 5 requêtes.

Résultat observé :
- Nombre de requêtes : 5
- Seuil : 5
- Résultat : aucune alerte.

La configuration initiale a ensuite été restaurée avec un seuil de 3 requêtes.

## Intérêt en cybersécurité industrielle

Une fréquence inhabituelle de requêtes Modbus peut révéler une activité anormale, une mauvaise configuration ou un comportement potentiellement malveillant.

La surveillance de cette fréquence peut contribuer à identifier des situations de surcharge ou des communications inhabituelles dans un réseau industriel.

## Limites

- L'analyse est réalisée hors ligne à partir d'un fichier PCAP.
- Le seuil et la fenêtre temporelle sont définis manuellement.
- Les paramètres utilisés sont expérimentaux et ne constituent pas des seuils universels.
- Le détecteur ne bloque pas les communications.
- Une fréquence élevée ne prouve pas à elle seule une attaque.
- Les tests ont été effectués dans un environnement local isolé.

## Conclusion

Ce mécanisme apporte une première capacité de détection des pics de requêtes Modbus TCP. Il complète les contrôles sur les adresses IP et les fonctions Modbus autorisées.
