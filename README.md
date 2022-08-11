# BattleMonster

**DISCLAIMER :**
Le Bot est en cours de développement, il ne peut donc être déployé sur d'autres serveurs.
Vous pouvez nous contacter si vous voulez participer au développement et/ou le tester !

BattleMonster est un bot RPG permettant de combattre des Monstres qui apparaissent de façon aléatoire sur le canal d'un serveur Discord.
Une fois le monstre abattu, les joueurs peuvent acquérir des butins pour améliorer leurs compétences.

## Fonctionnalités:
### Pour les joueurs: 
- 
-

## A propos:


Merci à vous de jouer et de partager le bot !

### 😄

## TodoList:
- [X] Création et gestion des Slayers
- [X] Ajouter la possibilité d'avoir plusieurs butins par combats
- [X] Gestion des dégâts effectués via Class Damage Done (Gestion du Timestamp)
- [X] Mise en place de la Spé Standard pour gestion des Stacks de spécial
- [X] Stats Monstres plus dynamiques (HP Mult & Difficulty Mult)
- [X] Ajouter de la Létalité aux Monstres
- [X] Gestion des dégâts subis par les joueurs
- [X] Récupération Date de Création du joueur (Dans la class Slayers)
- [X] Ajouter la létalité aux dégâts infligés par les monstres
- [X] Finalisation fiche monstre 
- [X] Gestion du Butin quand le Monstre est mort
- [X] Améliorer la gestion du Butin (Différentes slots à loot...)
- [X] Une seule attaque toutes les X minutes
- [X] Message et gestion si joueur parry
- [X] Message et gestion si joueur fail
- [X] Prépa Spé 4 : Acharnement (mult_spe dans Slayers)
- [X] Fusionner données spawn-hunts dans Combat_Variables & Rate
- [X] Optimisation des rates avec table intermédiaire (gamemode_spawn_rate, rarities_loot_rates)
- [X] Timeout View Items
- [X] Pouvoir attaquer avec le spécial
- [X] Stockage des items dans une table IDSlayers -> IDItems
- [X] PostgreSQL en self.table (Fonction pour récup chaque table)
- [X] Prendre en compte le loot slot dans le calcul du butin
- [X] Loop pour Regen & Revive (Sauf première boucle) 5% toutes les Xmin
- [X] Multiplicateur pour les combats à plusieurs Monstres
- [X] Enlever le rBaseBonuses de MSlayer
- [X] Remettre le ratio armor
- [X] Embed de fin de combat
- [X] Remettre toutes les views, séparément, dans le dossier Views
- [X] Timeout Behemoths (Fuite) - TBC
- [X] Gérer quand on est full stack mais qu'on attaque quand même
- [X] Details des items
- [X] Distribution du butin
- [X] Acceptation ou revente du butin

- [] Spe 3 (Surarmement)
Pour la deuxième attaque ->
If special == 3 (surarmement) & les 2 slots sont non vides:
    Damage, Stacks_Earned += … (après le parry_fail)

- [] Prépa Spé 4 : Reset (X%) to increase mult_spe & reset stacks

- [] Affichage Stats Slayers (3 page : Stats / Items / Achievements)
- [] InventorySlayer

- [] Remove le pull rGamemode de Admin Commands
- [] Parametize les requêts dans MainSlayers
- [] Rajout de bonus supplémentaires pour les spé
- [] Complétion de la BDD des Monstres
- [] Complétion de la BDD des Butins
- [] Ajout d' "Achievements" : Nombre de Monstres tués, ...
- [] Ajout d' "Achievements" pour le monstre : Display le nombre de dégâts occasionnés aux Slayers ....
- [] Canal pour afficher les dégâts infligés par les joueurs
- [] Spawn aléatoire des Monstres
- [] Système d'autodelete des loots selon rareté (Dans la class Slayer)