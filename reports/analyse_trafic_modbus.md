# Analyse du trafic industriel Modbus TCP

## 1. Objectif

L'objectif de cette analyse est d'approfondir l'analyse des communications Modbus TCP entre un client et un automate simulé OpenPLC.

L'analyse est réalisée à partir du fichier de capture :

`traffic-analysis/modbus_capture.pcap`

Les outils utilisés sont Wireshark et TShark.

## 2. Environnement

- Système : Ubuntu 24.04 sous WSL2
- Automate : OpenPLC Runtime v4.3.2
- Protocole industriel : Modbus TCP
- Port serveur : TCP 502
- Interface de capture : lo (Loopback)
- Adresse IP client : 127.0.0.1
- Adresse IP serveur : 127.0.0.1

## 3. Analyse des échanges Modbus

Commande utilisée :

```bash
tshark -r traffic-analysis/modbus_capture.pcap -Y modbus -T fields -E separator='|' -e frame.number -e frame.time_relative -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e modbus.func_code -e modbus.reference_num
```

Résultat : 10 paquets Modbus correspondant à 5 échanges requête/réponse.

### 3.1 Lecture d'une bobine — FC1

Paquet 4 : requête du client.

- Fonction : Read Coils (FC1)
- Adresse de départ : 0
- Nombre de bobines : 1
- Identifiant de transaction : 1

Paquet 6 : réponse du serveur.

- Fonction : Read Coils (FC1)
- Valeur retournée : TRUE
- Identifiant de transaction : 1

Conclusion : le client a demandé l'état de la bobine 0 et le serveur a retourné la valeur TRUE.

### 3.2 Écriture d'une bobine — FC5

Paquets 8 et 9 :

- Fonction : Write Single Coil (FC5)
- Adresse : 0
- Valeur écrite : 0000
- Identifiant de transaction : 2

Interprétation : le client demande la désactivation de la bobine 0.

Paquets 12 et 13 :

- Fonction : Write Single Coil (FC5)
- Adresse : 0
- Valeur écrite : FF00

Interprétation : le client demande l'activation de la bobine 0.

Rappel :
- 0x0000 = FALSE (OFF)
- 0xFF00 = TRUE (ON)

Les réponses du serveur reprennent les valeurs et adresses demandées.

## 4. Analyse de la communication TCP

Commande utilisée :

```bash
tshark -r traffic-analysis/modbus_capture.pcap -Y "tcp.port == 502" -T fields -E separator='|' -e frame.number -e frame.time_relative -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e tcp.flags -e tcp.len
```

### 4.1 Établissement de la connexion

Trois paquets ont été observés :

1. Paquet 1 : SYN — demande de connexion du client.
2. Paquet 2 : SYN-ACK — réponse du serveur.
3. Paquet 3 : ACK — confirmation du client.

La connexion TCP est établie.

### 4.2 Transmission des données

Les paquets 4 à 15 contiennent les échanges Modbus.

Les indicateurs PSH et ACK sont présents sur les segments transportant les données.

Exemples :
- Paquet 4 : 12 octets TCP.
- Paquet 6 : 10 octets TCP.
- Paquet 8 : 12 octets TCP.
- Paquet 9 : 12 octets TCP.

### 4.3 Fermeture de la connexion

- Paquet 16 : FIN-ACK envoyé par le client.
- Paquet 17 : FIN-ACK envoyé par le serveur.
- Paquet 18 : ACK final du client.

La fermeture TCP est observée dans la capture.

## 5. Mesure de la durée

Commande utilisée :

```bash
tshark -r traffic-analysis/modbus_capture.pcap -Y "tcp.port == 502" -T fields -e frame.number -e frame.time_relative
```

Premier paquet : 0 seconde.

Dernier paquet : 0,009630137 seconde.

Durée observée :

0,009630137 seconde, soit environ 9,63 millisecondes.

Cette mesure correspond à la séquence TCP capturée, depuis le premier SYN jusqu'au dernier ACK.

## 6. Observations de sécurité

Cette analyse met en évidence plusieurs points :

- Le port TCP 502 est utilisé pour les communications Modbus TCP.
- Le protocole permet la lecture et la modification des bobines du PLC.
- Les fonctions FC1 et FC5 sont visibles dans la capture.
- Les valeurs transmises sont lisibles avec TShark.
- Modbus TCP classique ne fournit pas nativement de chiffrement ni d'authentification.

### Recommandations

Dans un environnement industriel réel, il est recommandé de :

- Segmenter les réseaux IT et OT.
- Limiter les communications vers les automates.
- Filtrer les accès au port TCP 502.
- Autoriser uniquement les équipements nécessaires.
- Surveiller les commandes d'écriture Modbus.
- Centraliser et analyser les journaux réseau.

## 7. Limites de l'analyse

Les communications observées proviennent uniquement de l'environnement local :

127.0.0.1 → 127.0.0.1

Cette capture ne représente donc pas un réseau industriel réel avec plusieurs équipements.

La durée mesurée ne constitue pas non plus une mesure générale des performances de l'automate.

## 8. Conclusion

Ce travail a permis d'approfondir l'analyse du trafic industriel Modbus TCP.

Les échanges de lecture et d'écriture ont été identifiés, les requêtes et réponses ont été étudiées et les différentes phases de la communication TCP ont été observées.

Ces résultats constituent une première base technique pour comprendre et surveiller les communications industrielles dans le cadre du projet Industrial Network Security Lab.
