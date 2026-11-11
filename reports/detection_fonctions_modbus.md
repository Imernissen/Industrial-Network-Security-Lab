
# Détection des fonctions Modbus non autorisées

## Objectif

Ce script analyse une capture réseau Modbus TCP afin d'identifier les fonctions Modbus qui ne respectent pas la politique de sécurité définie pour le laboratoire.

## Environnement

- OpenPLC Runtime
- Modbus TCP
- Wireshark / TShark
- Python 3
- PyModbus

## Principe de détection

Le script utilise TShark pour extraire les codes de fonction Modbus présents dans les requêtes envoyées vers le port TCP 502.

Une liste blanche définit les fonctions autorisées dans ce laboratoire :

- FC1 : Read Coils
- FC5 : Write Single Coil

Toute fonction absente de cette liste déclenche une alerte.

## Résultats des tests

### Test 1 : trafic conforme

Fonctions autorisées : FC1 et FC5.

Résultat observé :
- FC1 : 3 requêtes
- FC5 : 2 requêtes
- Aucune fonction inhabituelle détectée.

### Test 2 : simulation d'une fonction non autorisée

La liste blanche a été temporairement modifiée pour autoriser uniquement FC1.

Résultat observé :
- FC1 : 3 requêtes autorisées
- FC5 : 2 requêtes non autorisées
- Une alerte a été générée pour FC5.

La configuration initiale a ensuite été restaurée.

## Intérêt en cybersécurité industrielle

La surveillance des fonctions Modbus permet de repérer des opérations qui ne correspondent pas aux règles définies pour un équipement industriel.

Par exemple, une fonction d'écriture non prévue dans la politique de sécurité peut justifier une investigation.

## Limites

- L'analyse est réalisée hors ligne à partir d'un fichier PCAP.
- La liste des fonctions autorisées est définie manuellement.
- Le script détecte les écarts à cette liste, mais ne détermine pas à lui seul si une opération est malveillante.
- Aucune action de blocage du trafic n'est effectuée.
- Les tests ont été réalisés dans un environnement local isolé.

## Conclusion

Ce détecteur constitue une première approche de surveillance des communications Modbus TCP. Il permet d'identifier les fonctions qui ne respectent pas une liste blanche et de générer des alertes pour faciliter l'analyse du trafic industriel.
