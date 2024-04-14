# Importation des bibliothèques nécessaires
import random  # Pour générer des nombres aléatoires
import matplotlib.pyplot as plt  # Pour afficher des graphiques
import matplotlib.colors  # Pour gérer les couleurs dans les graphiques
from matplotlib.animation import ArtistAnimation  # Pour créer une animation

# Définition des dimensions de la grille
row = 99
col = 99

# Définition des classes pour les types d'agents
class Cooperator:
    def __init__(self):
        self.score = 0  # Score de l'agent
        self.id = 'C'  # Identifiant de l'agent

class Defector:
    def __init__(self):
        self.score = 0  # Score de l'agent
        self.id = 'D'  # Identifiant de l'agent

# Définition de la classe Grid pour créer et manipuler la grille
class Grid:
    def __init__(self, rowsize, colsize):
        self.rowsize = rowsize
        self.colsize = colsize

    # Crée une grille vide
    def make_grid(self):
        return [[0 for _ in range(self.colsize)] for _ in range(self.rowsize)]

    # Remplit la grille avec un nombre donné d'agents coopérateurs et de défecteurs
    def populate_grid(self, num_cooperators, num_defectors):
        grid = self.make_grid()
        all_positions = [(i, j) for i in range(self.rowsize) for j in range(self.colsize)]
        random.shuffle(all_positions)
        # Placement des agents coopérateurs et défectueurs dans la grille
        if num_defectors == 1:
            center = (self.rowsize // 2, self.colsize // 2)
            for i in range(self.rowsize):
                for j in range(self.colsize):
                    grid[i][j] = Defector() if (i, j) == center else Cooperator()            
        else:
            defector_positions = set(all_positions[:num_defectors])
            for i in range(self.rowsize):
                for j in range(self.colsize):
                    if (i, j) in defector_positions:
                        grid[i][j] = Defector()
                    else:
                        grid[i][j] = Cooperator()
        return grid

# Renvoie les voisins de Moore d'une cellule donnée
def get_moore_neighbours(grid, row, col):
    neighbours = []
    # Coordonnées des voisins de Moore
    for x, y in (
            (row - 1, col), (row + 1, col), (row, col - 1),
            (row, col + 1), (row - 1, col - 1), (row - 1, col + 1),
            (row + 1, col - 1), (row + 1, col + 1)):
        if 0 <= x < len(grid) and 0 <= y < len(grid[x]):
            neighbours.append(grid[x][y])
    return neighbours

# Calcule le score d'une cellule en fonction de ses voisins
def calculate_score(grid, row, col):
    b = 1.85  # Paramètre pour le calcul du score
    neighbours = get_moore_neighbours(grid, row, col)
    player = grid[row][col]
    score = 0
    # Calcul du score en fonction des interactions avec les voisins
    if player.id == 'C':
        score += 1  # Interaction avec soi-même
    for neighbour in neighbours:
        if player.id == 'C' and neighbour.id == 'C':
            score += 1
        elif player.id == 'D' and neighbour.id == 'C':
            score += b
    return score

# Détermine le type du meilleur voisin d'une cellule donnée
def best_neighbor_type(grid, row, col): 
    neighbour_score = 0
    type_neighbour = ""
    neighbours = get_moore_neighbours(grid, row, col)
    player_score = grid[row][col].score
    # Recherche du voisin avec le score le plus élevé
    for neighbour in neighbours:
        if neighbour.score > neighbour_score:
            neighbour_score = neighbour.score
            type_neighbour = neighbour.id
    if player_score < neighbour_score:
        return type_neighbour
    else:
        return grid[row][col].id

# Paramètres de la simulation
N = 30  # Nombre d'itérations
num_cooperators = 9800  # Nombre d'agents coopérateurs initiaux
num_defectors = 1  # Nombre d'agents défectueux initiaux

# Crée et remplit la grille initiale avec les agents coopérateurs et défectueux
lattice = Grid(row, col).populate_grid(num_cooperators, num_defectors)
dbl_buf = Grid(row, col).populate_grid(num_cooperators, num_defectors)

# Définition des couleurs pour l'affichage
color_C_C = 'darkblue'  # Coopérateur à Coopérateur
color_D_D = 'red'  # Défecteur à Défecteur
color_C_D = 'yellow'  # Coopérateur à Défecteur
color_D_C = 'green'  # Défecteur à Coopérateur

# Création d'une colormap pour la représentation graphique des cellules
cmap = matplotlib.colors.ListedColormap([color_C_C, color_D_D, color_C_D, color_D_C])
bounds = [1, 2, 3, 4, 5]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

# Création de la figure et des axes pour l'animation graphique
fig, ax = plt.subplots()
images = []

# Création de la grille pour l'affichage de la chaleur (heatmap)
heatmap_data = Grid(row, col).make_grid()

# Boucle principale de la simulation pour chaque itération
for _ in range(N):    
    # Calcul des scores pour chaque cellule de la grille
    for r in range(row):
        for c in range(col):
            lattice[r][c].score = calculate_score(lattice, r, c)

    # Sélection du meilleur voisin pour chaque cellule et mise à jour de la grille
    for r in range(row):
        for c in range(col):
            dbl_buf[r][c].id = best_neighbor_type(lattice, r, c)

    # Mise à jour des données de la chaleur pour l'affichage graphique
    for r in range(row):
        for c in range(col):
            if lattice[r][c].id == 'C' and dbl_buf[r][c].id == 'C':
                heatmap_data[r][c] = 1
            elif lattice[r][c].id == 'D' and dbl_buf[r][c].id == 'D':
                heatmap_data[r][c] = 2
            elif lattice[r][c].id == 'C' and dbl_buf[r][c].id == 'D':
                heatmap_data[r][c] = 3
            elif lattice[r][c].id == 'D' and dbl_buf[r][c].id == 'C':
                heatmap_data[r][c] = 4

    # Ajoutez la grille de chaleur actuelle à la liste des images pour l'animation
    img = ax.imshow(heatmap_data, interpolation='nearest', cmap=cmap, norm=norm)
    images.append([img])
    
    # Mettre à jour les grilles pour la prochaine itération
    lattice, dbl_buf = dbl_buf, lattice

# Créez l'animation à partir de la liste des images
ani = ArtistAnimation(fig, images, interval=100, blit=True, repeat_delay=True)

# Sauvegarde de l'animation en GIF
ani.save("inv.gif", writer='pillow', fps=4)

# Calcul et affichage du nombre final de coopérateurs et de défecteurs restants
count_C = sum(cell.id == 'C' for row in lattice for cell in row)
count_D = sum(cell.id == 'D' for row in lattice for cell in row)

print(f"Nombre de Coopérateurs (C) restants: {count_C}")
print(f"Nombre de Défecteurs (D) restants: {count_D}")

# Affichage du graphique
plt.show()
plt.close(fig)