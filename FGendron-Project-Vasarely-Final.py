"""
Autheur: Fred Gendron
Date: Mai 2020
Code: Permet de dessiner une illusion optique dans le style de
Vasarely basée sur le dessin d'hexagones déformés ou non
Entrees: Coordonnées (x,y) des coins exterieurs du pavé, longueur (l) de l'arrete des héxagones,
trois couleurs pour les faces de l'hexagone, les coordonnés (x,y,z) du centre du sphère de la deformation,
et le rayon de la sphère de la déformation.
Sortie: Un pavage d'hexagones dont certains sont déformés par une sphère
"""

# Import fonctions prédéfinies:
from math import pi, sin, cos, sqrt, acos, asin, atan2
import turtle


# Definition des fonctions:
def deformation(p, centre, rayon):
    """ Calcul des coordonnées d'un point suite à la déformation engendrée par la sphère émergeante
        Entrées :
          p : coordonnées (x, y, z) du point du dalage à tracer (z = 0) AVANT déformation
          centre : coordonnées (X0, Y0, Z0) du centre de la sphère
          rayon : rayon de la sphère
        Sorties : coordonnées (xprim, yprim, zprim) du point du dallage à tracer APRÈS déformation
    """
    x, y, z = p
    xprim, yprim, zprim = x, y, z
    xc, yc, zc = centre
    if rayon ** 2 > zc ** 2:
        zc = zc if zc <= 0 else -zc
        r = sqrt(
            (x - xc) ** 2 + (y - yc) ** 2)  # distance horizontale depuis le point à dessiner jusqu'à l'axe de la sphère
        rayon_emerge = sqrt(rayon ** 2 - zc ** 2)  # rayon de la partie émergée de la sphère
        rprim = rayon * sin(acos(-zc / rayon) * r / rayon_emerge)
        if 0 < r <= rayon_emerge:  # calcul de la déformation dans les autres cas
            xprim = xc + (x - xc) * rprim / r  # les nouvelles coordonnées sont proportionnelles aux anciennes
            yprim = yc + (y - yc) * rprim / r
        if r <= rayon_emerge:
            beta = asin(rprim / rayon)
            zprim = zc + rayon * cos(beta)
            if centre[2] > 0:
                zprim = -zprim
    return (xprim, yprim, zprim)

def hexagone(point, longueur, col, centre, rayon):
    """Dessine un héxagone qui peut être déformé ou non
        Entrées :
        point : coordonnées (x,y) du centre de l'héxagone non déformé
        longueur : longueur de l'arrete de l'hexagone
        col : tuple(col1,col2,col3) contenant les couleurs des trois faces de l'hexagone
        centre : coordonnées (x,y) du centre de la sphère de déformation
        rayon : longueur du rayon de la sphère de déformation
        Sorties : héxagone
    """
    # origine de l'hexagone:
    centerx = point[0]
    centery = point[1]
    # couleurs de l'hexagone:
    col1 = col[0]
    col2 = col[1]
    col3 = col[2]
    # taille de l'hexagone:
    l = longueur
    # points de l'hexagone avant déformation:
    pt0 = (centerx, centery)
    pt1 = (centerx + l, centery)
    pt2 = (centerx + l * cos(pi / 3), centery + l * sin(pi / 3))
    pt3 = (centerx - l * cos(pi / 3), centery + l * sin(pi / 3))
    pt4 = (centerx - l, centery)
    pt5 = (centerx - l * cos(pi / 3), centery - l * sin(pi / 3))
    pt6 = (centerx + l * cos(pi / 3), centery - l * sin(pi / 3))
    ptnodef = [pt0, pt1, pt2, pt3, pt4, pt5, pt6]
    # points de l'hexagone après déformation:
    ptdef = []
    for elem in ptnodef:
        ptdef.append((deformation((elem[0], elem[1], 0), centre, rayon)[0],
                      deformation((elem[0], elem[1], 0), centre, rayon)[1]))
    # print(ptnodef)
    # print(ptdef)
    # plot de l'hexagone
    turtle.up()
    turtle.goto(ptdef[0])
    # face 1
    turtle.down()
    turtle.color(col1)
    turtle.begin_fill()
    turtle.goto(ptdef[1])
    turtle.goto(ptdef[2])
    turtle.goto(ptdef[3])
    turtle.goto(ptdef[0])
    turtle.end_fill()
    # face 2
    turtle.color(col2)
    turtle.begin_fill()
    turtle.goto(ptdef[1])
    turtle.goto(ptdef[6])
    turtle.goto(ptdef[5])
    turtle.goto(ptdef[0])
    turtle.end_fill()
    # face 3
    turtle.color(col3)
    turtle.begin_fill()
    turtle.goto(ptdef[3])
    turtle.goto(ptdef[4])
    turtle.goto(ptdef[5])
    turtle.goto(ptdef[0])
    turtle.end_fill()
    turtle.up()


def pavage(inf_gauche, sup_droit, longueur, col, centre, rayon):
    """
    Dessine un pavage d'hexagones en faisiant appel aux fonctions hexagone
    et deformation
    Entrées :
    inf_gauche : coordonnées (x,y) du coin inférieur gauche du pavé
    sup_droit : coordonnées (x,y) du coin supérieur droit du pavé
    longueur : longueur de l'arrete de l'hexagone
    col : tuple(col1,col2,col3) contenant les couleurs des trois faces de l'hexagone
    centre : coordonnées (x,y) du centre de la sphère de déformation
    rayon : longueur du rayon de la sphère de déformation
    Sorties : pavé d'héxagones
    """
    # Dessin du pavage d'héxagones
    n, m = 0, 0
    width = sup_droit[0] - inf_gauche[0]
    height = sup_droit[0] - inf_gauche[0]
    step_x = longueur * 3.0
    step_y = longueur * sin(pi / 3)
    nb_i = width / step_x
    nb_j = height / step_y

    for j in range(int(nb_j)):
        m += 1
        for i in range(int(nb_i) - (m % 2)):
            n += 1
            x_p = step_x * (i + 1 / 2) + (m % 2) * step_x / 2 - (width) / 2 + (width - (int(nb_i) * step_x)) / 2
            y_p = step_y * j - (height / 2) + (height - int(nb_j) * step_y) / 2
            hexagone((x_p, y_p, 0), longueur, col, centre, rayon)
        n = 0

# Code Principal
infgauche = int(input("Coin inférieur gauche (val,val) : ", ))
supdroit = int(input("Coin supérieur doit (val,val) : ", ))
arrete = int(input("Longueur d'une arrete : ", ))
col1 = str(input("Couleur 1 : ", ))
col2 = str(input("Couleur 2 : ", ))
col3 = str(input("Couleur 3 : ", ))
cerclex = int(input("Abscisse du centre du cercle : ", ))
cercley = int(input("Ordonnée du centre du cercle : ", ))
cerclez = int(input("Hauteur du centre du cercle : ", ))
radius = int(input("Rayon du cercle : ", ))

INF_GAUCHE = (infgauche, infgauche)
SUP_DROIT = (supdroit, supdroit)
COLORS = (col1, col2, col3)
CERCLE = (cerclex, cercley, cerclez)

# CALL of pavage
pavage(INF_GAUCHE, SUP_DROIT, arrete, COLORS, CERCLE, radius)
# Export eps of plot
turtle.getcanvas().postscript(file="pavage-tmp.eps")
turtle.done()
