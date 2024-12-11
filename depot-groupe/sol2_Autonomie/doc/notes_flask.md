# Fichier regroupant les différentes précision sur l'organisation de Flask
## Modes de fonctionnement des RPI
- **stopped**: robot arrêter du fait d'un obstacle (ou ordre) en dehors d'un marqueur. Lorsqu'il repart, il cherche à retrouver son marqueur d'origine. Le robot connaît et indique son prochain objectif
- **reached**: marqueur/objectif atteint par le robot. En attente d'un nouvel ordre (autorisation de déplacement ou nouvel objectif). Le  robot connaît et indique son dernier objectif atteint
- **searching**: le robot est en mode de recherche de son objectif. (Tourne sur lui-même par exemple). Le robot connaît et indique son prochain objectif
- **going**: le robot est en route vers son objectif (roule/corrige sa direction). Le robot connaît et indique son prochain objectif
- **ready**: le robot n'a pas d'objectif et n'en a pas atteint (début). Le robot indique le marqueur -1
