# Principe de fonctionnement de orchestrator
## Un script pour les contrôler tous
1) Situé soit sur un serveur Internet, soit interne à Telecom, soit en local sur un même AP Wi-Fi, un script  tourne sur une machine autre qu'un raspberry.  
2) L'objectif de ce dernier est d'envoyer des commandes et de recevoir des informations depuis chaque RPI.  
3) Il garde en mémoire les destinations des RPI ainsi que les objectifs finaux de ces derniers.  
4) Les RPI signalent quand elles ont atteint un checkpoint (fin ou marqueur intermédiaire).  
5) Il pourrait être intéressant d'informer l'orchestrateur de la distance par rapport au marqueur checkpoint: cela permettrait d'éviter les collisions en calculant quel robot va se trouver sur la trajectoire ?

6) Le premier des robots pourrait aussi faire un mapping des marqueurs à partir du centre afin de plus facilement éviter les collisions par la suite (fait perdre un peu de temps au début mais peu en faire gagner par la suite notamment en utilisant la propriété 4)

7) Une mesure du diamètre peut être faite par le premier robot pour calibrer tout les calculs de 

8) La gestion des collisions peut se faire aussi se faire (en plus) par robot:  
    Chaque robot est entouré de marqueurs (différent pour chaque face et chaque robot) permettant de dire si un autre robot se trouve sur son trajet. si les deux sont de face c'est cuit mais si c'est sur le côté, celui qui voit peut s'arrêter

## Proposition d'implémentation
### Flask partout
Orchestrator (collaborate-orchestrator) est un serveur HTTP(ou S) exécutant flask (ou équivalent).
Sur  chaque RPI (collaborate-rpi) un serveur flask est exécuter (différent de celui qui était potentiellement pour le contrôle manuel/l'ui).
Orchestrator et RPI sont chacuns tour à tour client et serveur HTTP en fonction de qui envoie les données.
Les données sont envoyées entre chaque composantes sous forme de string JSON. (API potentiellement réalisable avec https://editor-next.swagger.io/)

**Avantages**:
- Simplicité de mise en place
- Peu soumis au problème de pertes de réseau car un nouveau socket TCP est créé à chaque requêtre HTTP
- Permet la communication entre les RPI (Même si pas forcément envisagée pour l'instant)
- Authentification des RPI simplifiée (utilisation de header JWT par exemple dans chaque requête pour éviter les plus malins):
    Deux solutions:
    - Donner un token "définitif" par RPI (Pas trop besoin de HTTPS dans ce cas et permet de facilement authentifié le serveur (le token serveur est enregistré en dur dans les RPI)): risque de fuite d'identifiant (il faut trouver un moyen de partager les tokens facilement)
    - Dynamiquement à chaque démarrage de script un couple identifiant mot de passe est envoyé au serveur et il renvoie un token: il faut du HTTPS sûr (CA personnalisée obligatoire) pour protéger l'envoie id mdp et il faut que le serveur s'identifie auprès de tous : Pas de risque de fuite d'identifiant 
- Interface standard entre tout les RPIs, l'implémentation peut différer tant que le service des modes est le même

**Inconvénients**:
- Peu de réactivité 70/80ms (je pense)

### Des websockets ou Socket TCP purs
Orchestrator est un serveur servant un port TCP (9200 par exemple). Chaque RPI sont clients de ce serveur
Les ordres sont transmis sous forme de string (peuvent aussi être des JSON mais donc plus long => intérêt moins grand)

L'authentification peut être réalisée en envoyant chaque ordre avec un hash à la suite et vérifier si le hash correspond au RPI (Chaque RPI intègre un clé propre). le problème est qu'il n'est pas possible d'échanger dynamiquement les clés (de façon simple)
**Avantages**:
- Réactivité très grande (<10ms par ordre)
- Possibilité d'envoyer des ordres en broadcast très facilement
- Pas de serveur flask partout (Plus simple dans l'architecture et moins de ressources utilisées au final)

**Inconvénients**:
- Pas de communication inter RPI facile
- Soumis au problème de pertes de réseau (Il faut penser à intégrer un mécanisme de reconnexion au TCP et s'assurer qu'il est fiable)
- Authentification un peu archaïque et illogique du point de vu de l'avantage de la réactivité très grande (Ne pas en faire ?)

**A vous de choisir ou de proposer !**

