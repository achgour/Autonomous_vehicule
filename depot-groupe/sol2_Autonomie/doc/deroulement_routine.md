# Déroulement routine résolution
## Composantes
Pour recevoir des informations chaque robot expose une API REST 

### Serveur 
Un des robots (élu ou désigné) exécute une partie serveur. Ce sera le partenaire de communication unique des autres robots.


1) Situé soit sur un serveur Internet, soit interne à Telecom, soit en local sur un même AP Wi-Fi, un script  tourne sur une machine autre qu'un raspberry.  
2) L'objectif de ce dernier est d'envoyer des commandes et de recevoir des informations depuis chaque RPI.  
3) Il garde en mémoire les destinations des RPI ainsi que les objectifs finaux de ces derniers.  
4) Les RPI signalent quand elles ont atteint un checkpoint (fin ou marqueur intermédiaire).  
5) Il pourrait être intéressant d'informer l'orchestrateur de la distance par rapport au marqueur checkpoint: cela permettrait d'éviter les collisions en calculant quel robot va se trouver sur la trajectoire ?

6) Le premier des robots pourrait aussi faire un mapping des marqueurs à partir du centre afin de plus facilement éviter les collisions par la suite (fait perdre un peu de temps au début mais peu en faire gagner par la suite notamment en utilisant la propriété 4)

7) Une mesure du diamètre peut être faite par le premier robot pour calibrer tout les calculs de 

8) La gestion des collisions peut se faire aussi se faire (en plus) par robot:  
    Chaque robot est entouré de marqueurs (différent pour chaque face et chaque robot) permettant de dire si un autre robot se trouve sur son trajet. si les deux sont de face c'est cuit mais si c'est sur le côté, celui qui voit peut s'arrêter