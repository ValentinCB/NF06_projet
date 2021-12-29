# -*- coding: utf-8 -*-
import ctypes as ct
from random import uniform
from itertools import combinations
import matplotlib.pyplot as plt


def read_points_mesh(nom_fichier):  # permet d'extraire une liste de points d'un  fichier .mesh
    list_pts = list()
    with open(nom_fichier) as f:
        fichier = f.readlines()
        for i in range(int(fichier[3])):  # boucle sur le nombre de points
            coord = []
            batch = ''
            for char in fichier[4 + i]:  # compte à partir de la ligne 5
                if char != ' ':
                    batch += char
                else:
                    coord.append(float(batch))
                    batch = ''
            list_pts.append(tuple(coord))
    return list_pts


def add_points(liste, nb_points, rnd=False, mini=0, maxi=5):  # ajoute des points à la liste de points
    if rnd:  # si rnd = True, on crée des coordonnées floatantes entre les deux bornes
        for i in range(nb_points):
            point = list()
            point.append(float(uniform(mini, maxi)))
            point.append(float(uniform(mini, maxi)))
            liste.append(tuple(point))
    else:
        for i in range(nb_points):
            point = list()
            point.append(float(input('point {}, x : '.format(i))))
            point.append(float(input('point {}, y : '.format(i))))
            liste.append(tuple(point))
    return 0  # comme la pluspart des fonction ici, le changement se fait par adresse


def write_file(nom_fichier, liste_pts, liste_tris):  # crée un fichier .mesh à partir des points et des triangles
    with open(nom_fichier, 'w') as f:
        f.writelines(['MeshVersionFormatted 1', '\n'])
        f.writelines(['Dimension 2', '\n'])
        f.writelines(['Vertices', '\n'])
        f.writelines([str(len(liste_pts)), '\n'])
        for point in liste_pts:
            x_coord, y_coord = round(point[0], 6), round(point[1], 6)
            f.writelines([str(x_coord), (6 - str(x_coord)[::-1].find('.')) * '0', ' '])  # str(x)[::-1].find('.') compte de nb de décimales de x
            f.writelines([str(y_coord), (6 - str(y_coord)[::-1].find('.')) * '0', ' 1', '\n'])
        f.writelines(['\nTriangles', '\n'])
        f.writelines([str(len(liste_tris)), '\n'])
        for triangle in liste_tris:
            f.writelines([str(triangle[0] + 1), ' '])  # +1 pour conserver l'indexation à partir de 1 dans le .mesh
            f.writelines([str(triangle[1] + 1), ' '])
            f.writelines([str(triangle[2] + 1), ' 1', '\n'])
        f.writelines(['End'])
    return 0


def flatten(liste):  # transforme [[a, b], [c, d], [e, f] en [a, b, c, d, e, f]
    flat = list()
    for elements in liste:
        for element in elements:
            flat.append(element)
    return flat


# retourne les paires de points avec lequels il faut trianguler le nouveau point ajouté à partir
# des triangles dont le cercle circonstit contient le nouveau point, appelé ici red_triangles
def which_pairs_to_connect(red_triangles):
    pairs = list()
    for triangle in red_triangles:
        batch = list(combinations(triangle, 2))
        for pair in batch:
            # (1, 2) et (2, 1) correspondent à la même arrête, on les tri donc pour obtenir l'unicité
            pairs.append(tuple(sorted(pair)))  # pairs contient les 2 uplets de tous les red_triangles
    seen = set()
    dupes = [x for x in pairs if x in seen or seen.add(x)]  # paires vue au moins deux fois dans pairs
    red_points = set(flatten(red_triangles))  # liste des points présent dans les red_triangles sans doublons
    all_pairs = list(combinations(red_points, 2))  # toutes les 2 uplets possible avec red_points (red_points != pairs)
    all_pairs[:] = [tuple(sorted(pair)) for pair in all_pairs]  # tri les paires de all_pairs
    unconnected = [x for x in all_pairs if x not in pairs]  # trouve les autres arrêtes qui ne sont pas côte à côtes
    # exclude correspond alors à toutes les paires avec lequels il ne faut pas trianguler le nouveau point
    exclude = dupes + unconnected
    return [x for x in all_pairs if x not in exclude]  # on renvoit l'opposé de exclude


def delauney_algo():  # algoritme principal qui lit les points, crée les triangles et écrit le fichier
    liste_points = list()
    liste_triangles = list()
    print('[0] - ne pas lire de fichier')
    print('[1] - lire un fichier')
    choice = -1
    while choice != 0 and choice != 1:  # lit ou non un fichier
        choice = int(input('-> '))
        if choice == 0:
            print('aucun fichier lu')
        elif choice == 1:
            print('entrer le nom du fichier')
            file_name = input('-> ')
            liste_points = read_points_mesh(file_name)
            print('fichier lu correctement')
        else:
            print('erreur : choix invalide, entrer de nouveau')
    print('[0] - ne pas ajouter de points')
    print('[1] - ajouter des points')
    print('[2] - ajouter des points aléatoirement')
    choice = -1
    while (choice != 0 and choice != 1 and choice != 2) or liste_points == 0:  # ajouts ou non de points
        choice = int(input('-> '))
        if choice == 0:
            print('aucun points ajoutés')
            if len(liste_points) == 0:
                print('erreur : liste de points vide')
        elif choice == 1:
            nb_pts = int(input('nombre de points -> '))
            add_points(liste_points, nb_pts, rnd=False)
        elif choice == 2:
            nb_pts = int(input('nombre de points -> '))
            borne_min = int(input('borne min -> '))
            borne_max = int(input('borne max -> '))
            add_points(liste_points, nb_pts, rnd=True, mini=borne_min, maxi=borne_max)
        else:
            print('erreur : choix invalide, entrer de nouveau')
    delauney_points = super_triangle(liste_points)  # crée les 3 points du super triangle (s-triangle)
    liste_triangles.append([delauney_points.index(x) for x in delauney_points])  # ajoute la triangulation du s-triangle
    for point in liste_points:  # ajoute les points un à un à la triangulation
        red_triangles = verif_all_circles(delauney_points, point, liste_triangles)  # voir la fonction
        delauney_points.append(point)
        for red_triangle in red_triangles:
            liste_triangles.remove(red_triangle)  # on supprime les red_triangles de la triangulation
        connect = which_pairs_to_connect(red_triangles)  # voir la fonction
        for pair in connect:  # triangule le point avec les paires de connect
            triangle = [delauney_points.index(point), pair[0], pair[1]]
            liste_triangles.append(triangle)
    delete_super_triangle(delauney_points, liste_triangles)
    write_file('result.mesh', delauney_points, liste_triangles)  # écrit le fichier .mesh
    return delauney_points, liste_triangles


def connect_triangle(x, y, triangle):  # ajoute un triange au plot
    a, b, c = triangle[0], triangle[1], triangle[2]  # ici on compte à partir de 0
    x1, x2, x3 = x[a], x[b], x[c]
    y1, y2, y3 = y[a], y[b], y[c]
    plt.plot([x1, x2], [y1, y2], 'ko-', markersize=3)  # crée les trois arrêtes du triangle
    plt.plot([x1, x3], [y1, y3], 'ko-', markersize=3)
    plt.plot([x2, x3], [y2, y3], 'ko-', markersize=3)
    return 0


def plot_triangulation(liste_pts, liste_triangles):  # affiche la triangulation
    x = [pt[0] for pt in liste_pts]
    y = [pt[1] for pt in liste_pts]
    for triangle in liste_triangles:
        connect_triangle(x, y, triangle)
    plt.plot(x, y, 'ro', markersize=3)  # repasse les points en rouge
    plt.axis('square')
    plt.show()
    return 0


# renvoie la liste des triangles dont le cercle circonscrit contient pt
def verif_all_circles(list_pts, pt, list_triangle):
    list_red_triangle = []
    for triangle in list_triangle:
        pt_ctype = (ct.c_float * 2)(*pt)
        triangle_ctype = ((ct.c_float * 2) * 3)(*(list_pts[triangle[0]], list_pts[triangle[1]], list_pts[triangle[2]]))
        if lib.is_in_cercle(triangle_ctype, pt_ctype) == 1:
            list_red_triangle.append(triangle)
    return list_red_triangle


def super_triangle(list_pts):
    list_pt_ctype = ((ct.c_float * 2) * len(list_pts))(*list_pts)
    pt_triangle_ctype = ((ct.c_float * 2) * 3)(*[(0, 0), (0, 0), (0, 0)])
    lib.Super_Triangle(len(list_pts), pt_triangle_ctype, list_pt_ctype)
    pt_triangle = list()
    for i in range(3):
        pt_triangle.append((pt_triangle_ctype[i][0], pt_triangle_ctype[i][1]))
    return pt_triangle


def delete_super_triangle(list_points, list_trianlges):  # supprime les 3 pts du s-triangle et les triangles associés
    for triangle in list_trianlges:
        triangle[:] = [point - 3 for point in triangle]  # décrémente de 3 tous les points des triangles
    list_trianlges[:] = [t for t in list_trianlges if -3 not in t and -2 not in t and -1 not in t]
    list_points[:] = list_points[3:]  # supprime les 3 premiers points de la liste de points
    return 0


# lien vers le fichier .dll, à changer
lib = ct.CDLL("C:\\user\\...\\liblibcprojet.dll")

# Main
points, triangles = delauney_algo()
plot_triangulation(points, triangles)
