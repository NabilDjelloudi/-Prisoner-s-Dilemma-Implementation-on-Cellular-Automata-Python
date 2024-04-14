# Importation des bibliothèques nécessaires
import random
import matplotlib.pyplot as plt
import matplotlib.colors

# Définition des classes pour les types d'agents
class Cooperator:
    def __init__(self):
        self.id = 'C'  # Identifiant du coopérateur

class Defector:
    def __init__(self):
        self.id = 'D'  # Identifiant du défecteur

# Définition de la classe Grid pour créer et manipuler la grille
class Grid:
    def __init__(self, rowsize, colsize):
        self.rowsize = rowsize  # Nombre de lignes dans la grille
        self.colsize = colsize  # Nombre de colonnes dans la grille

    # Méthode pour créer une grille vide
    def make_grid(self):
        return [[0 for _ in range(self.colsize)] for _ in range(self.rowsize)]

    # Méthode pour remplir la grille avec des coopérateurs et des défecteurs
    def populate_grid(self, num_cooperators, num_defectors):
        grid = self.make_grid()
        all_positions = [(i, j) for i in range(self.rowsize) for j in range(self.colsize)]
        random.shuffle(all_positions)

        # Positionne les défecteurs aux premières positions
        defector_positions = set(all_positions[:num_defectors])
        for pos in defector_positions:
            grid[pos[0]][pos[1]] = Defector()

        # Positionne les coopérateurs sur les positions restantes
        remaining_positions = set(all_positions[num_defectors:])
        for pos in remaining_positions:
            grid[pos[0]][pos[1]] = Cooperator() if pos in remaining_positions else Defector()

        return grid

# Fonction pour obtenir les voisins de Moore d'une cellule donnée
def get_moore_neighbours(grid, row, col):
    neighbours = []
    for x, y in ((row - 1, col), (row + 1, col), (row, col - 1),
                 (row, col + 1), (row - 1, col - 1), (row - 1, col + 1),
                 (row + 1, col - 1), (row + 1, col + 1)):
        if 0 <= x < len(grid) and 0 <= y < len(grid[x]):
            neighbours.append(grid[x][y])
    return neighbours

# Fonction pour déterminer le type le plus fréquent parmi les voisins
def most_frequent_type(neighbours):
    type_counts = {'C': 0, 'D': 0}
    for neighbour in neighbours:
        type_counts[neighbour.id] += 1

    max_count = max(type_counts.values())
    max_types = [t for t, count in type_counts.items() if count == max_count]

    return random.choice(max_types) if len(max_types) > 1 else max_types[0]

# Définition des couleurs pour les interactions
color_C_C = 'darkblue'   # Cooperator reste Cooperator
color_D_D = 'red'  # Defector reste Defector
color_C_D = 'yellow'    # Cooperator devient Defector
color_D_C = 'green' # Defector devient Cooperator

# Création d'une colormap personnalisée
cmap = matplotlib.colors.ListedColormap([color_C_C, color_D_D, color_C_D, color_D_C])
bounds = [1, 2, 3, 4, 5]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

# Paramètres de la simulation
row, col, N = 99, 99, 80
num_cooperators = 3000  # Nombre de coopérateurs
num_defectors = 5000     # Nombre de défecteurs

# Création de la grille pour l'affichage de la chaleur
heatmap_data = Grid(row, col).make_grid()

# Initialisation des grilles avec les agents coopérateurs et défecteurs
lattice = Grid(row, col).populate_grid(num_cooperators, num_defectors)
dbl_buf = Grid(row, col).populate_grid(num_cooperators, num_defectors)

# Boucle principale de la simulation
for gen in range(N):
    # Mise à jour des types des cellules en fonction des voisins
    for r in range(row):
        for c in range(col):
            neighbours = get_moore_neighbours(lattice, r, c)
            dbl_buf[r][c].id = most_frequent_type(neighbours)

    # Mise à jour des données de la chaleur pour l'affichage
    for r in range(row):
        for c in range(col):
            state_map = {('C', 'C'): 1, ('D', 'D'): 2, ('C', 'D'): 3, ('D', 'C'): 4}
            heatmap_data[r][c] = state_map[(lattice[r][c].id, dbl_buf[r][c].id)]

    # Affichage de la grille avec les données de la chaleur
    plt.imshow(heatmap_data, interpolation='nearest', cmap=cmap, norm=norm)
    plt.pause(0.01)  # Pause pour l'affichage dynamique

    # Échange des grilles pour la prochaine itération
    lattice, dbl_buf = dbl_buf, lattice

# Affichage final de la simulation
plt.show()