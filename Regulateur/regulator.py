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



def phi_dphi(X, centre, Morph):
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
    def dphidp(x,y):
        dxx = -3*x**2 - y**2 + 1
        dxy = -2*x*y -1
        dyx = -2*x*y + 1
        dyy = -3*y**2 - x**2 + 1

        return np.array([[dxx,dxy],[dyx,dyy]])

    x, y, theta, _ = X.flatten()
    dpdt = np.array([[np.cos(theta)], [np.sin(theta)]])

    cx, cy = centre
    invMorph = np.linalg.inv(Morph)
    x1 = invMorph[0, 0] * (x - cx) + invMorph[0, 1] * (y - cy)
    y1 = invMorph[1, 0] * (x - cx) + invMorph[1, 1] * (y - cy)


    dx, dy = -x1**3 - y1**2*x1 + x1 - y1, -y1**3 - x1**2*y1 + x1 + y1
    phix = Morph[0, 0] * dx + Morph[0, 1] * dy
    phiy = Morph[1, 0] * dx + Morph[1, 1] * dy

    gradphi = dphidp(x1,y1)
    dphidt = Morph @ gradphi @ invMorph @ dpdt
    dphix, dphiy = dphidt.flatten()

    return [phix, phiy], [dphix, dphiy]


def regulateur_vector(X, centre, Morph, w_cons):
    vec, dvec = phi_dphi(X, centre, Morph)

    x, y, theta, w = X.flatten()
    v = theta-np.arctan2(vec[1],vec[0])
    dv = (-dvec[0]*vec[1]+dvec[1]*vec[0])/np.linalg.norm(vec)**2
    
    u1max = 1.5
    u1 = -1*np.mod(v+np.pi,2*np.pi)-np.pi + dv
    u1 = np.clip(u1, -u1max, u1max)

    u2max = 10
    u2 = w + 0.1*(w_cons - w)
    u2 = np.clip(u2, -u2max, u2max)

    return np.array([u1, u2])  


