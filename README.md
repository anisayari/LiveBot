# Bugfix

Il semblerait que la variable du robot était réassigné avec son propre résultat, la méthode switch_robot a été utilisée pour faire passer le dernier message dans le robot qui va être utilisé en suivant.

Pour le débug le son a été émulé, donc le passage d'un robot à l'autre à été fait via l'event KEYDOWN qui attend un appui clavier.

# Repo

Ajout de requirement.txt pour la simplification de l'installation des dépendances.