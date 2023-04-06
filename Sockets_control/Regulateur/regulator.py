import numpy as np

def regulateur_simple(X, consigne, memoire):
    """ calcule les commandes en fonction des consignes de cap et de vitesse

    Args:
        consigne (numpy.ndarray): [cap_desire, vitesse_desire], en radians et rd/s
        capteurs (list): [cap, vitesse], en radians et rd/s
        memoire (list): [*args], memoire à retenir pour les PID
    
    Returns:
        numpy.ndarray: [u1, u2], en radians(guidon) et rd/s
        memoire_new (list): [*args], memoire mise à jour
    """

    x, y, theta, w = X.flatten()
    theta_desire, w_desire = consigne

    u1max = 1.5
    theta_prec, Se_theta = memoire
    e = theta_desire - theta
    Se_theta += e
    de = theta - theta_prec

    u1 = 0.5*e + 0.5*Se_theta + 0.5*de
    u1 = np.clip(u1, -u1max, u1max)

    u2max = 10
    u2 = w + 0.1*(w_desire - w)
    u2 = np.clip(u2, -u2max, u2max)
    
    memoire_new = [theta, Se_theta]
    if len(memoire_new)==len(memoire):
        return np.array([u1, u2]), memoire_new
    else :
        raise ValueError("Vous n'avez pas mis à jour toutes les variables de mémoire")



def vector_field_circle(x,y, centre, Morph):
    """Champs de vecteur pour suivre un cercle ou une ellipse

    Args:
        x (float): position en x du robot
        y (float): position en y du robot
        centre (tuple<float,float>): centre du cercle ou de l'ellipse
        morph (numpy.ndarray): matrice de morphing (2x2)

    Returns:
        tuple<float,float>: vecteur à suivre
        tuple<float,float>: dérivée du vecteur à suivre
    """

    cx, cy = centre
    invMorph = np.linalg.inv(Morph)
    x1 = invMorph[0, 0] * (x - cx) + invMorph[0, 1] * (y - cy)
    y1 = invMorph[1, 0] * (x - cx) + invMorph[1, 1] * (y - cy)


    dx, dy = -x1**3 - y1**2*x1 + x1 - y1, -y1**3 - x1**2*y1 + x1 + y1
    vecx = Morph[0, 0] * dx + Morph[0, 1] * dy
    vecy = Morph[1, 0] * dx + Morph[1, 1] * dy

    return [vecx, vecy]

def plot_vector_field(ax, f, centre, Morph, xmin, xmax, ymin, ymax, step):
    Mx, My = np.arange(xmin, xmax, step), np.arange(ymin, ymax, step)
    X1, X2 = np.meshgrid(Mx, My)

    VX, VY = f(X1, X2, centre, Morph)
    R = np.sqrt(VX ** 2 + VY ** 2)

    ax.quiver(Mx, My, VX / R, VY / R)


def regule_vector(X, vec):
    """Régule le robot pour suivre un vecteur

    Args:
        X (list): [x, y, theta, w] vecteur d'état du robot
        vec (list): [vx, vy] vecteur à suivre
        dvec (list): [dvx, dvy] dérivée du vecteur à suivre
    Returns:
        numpy.ndarray: [u1, u2], consignes en radians(guidon) et rd/s
    """

    def sawtooth(x):
        return 2*np.arctan(np.tan(x/2))

    x, y, theta, w = X
    v = theta-np.arctan2(vec[1],vec[0])
    
    u1 = 1*sawtooth(v)
    u2 = np.linalg.norm(vec)

    return np.array([u1, u2])  

def regule_circuit(X, point, dt):
    """Régule le robot pour suivre un cap

    Args:
        X (list): [x, y, theta, z] vecteur d'état du robot, adapté pour que la matrice de délais différentiels soit inversible
        point (list<list>): [[xd, dxd, ddxd], [yd, dyd, ddyd]] liste de listes contenant les coordonnées du point à suivre, sa dérivée et sa dérivée seconde
        dt (float): pas de temps estimé

    Returns:
        numpy.ndarray: [u1, u2], consignes guidon (rd) et vitesse
        z (float): valeur de z mise à jour (besoin d'un intégrateur)
    """

    x, y, theta, z = X
    xd, dxd, ddxd = point[0]
    yd, dyd, ddyd = point[1]

    
    dz = np.cos(theta)*(xd-x+2*(dxd-z*np.cos(theta))+ddxd)+np.sin(theta)*(yd-y+2*(dyd-z*np.sin(theta))+ddyd)
    z = z + dt*dz
    u1 = z
    u2 = -np.sin(theta)/z*(xd-x+2*(dxd-z*np.cos(theta))+ddxd)+np.cos(theta)/z*(yd-y+2*(dyd-z*np.sin(theta))+ddyd)

    return np.array([u1, u2], z)