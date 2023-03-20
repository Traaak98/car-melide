import numpy as np

def regulateur(consigne, capteurs):
    """ calcule les commandes en fonction des consignes de cap et de vitesse

    Args:
        consigne (numpy.ndarray): [cap_desire, vitesse_desire], en radians et m/s
        capteurs (_type_): [cap, vitesse], en radians et m/s
    """
    cap, vitesse = capteurs
    cap_desire, vitesse_desire = consigne

    Kp_cap, Kp_vit = 0.1, 0.1
    u1 = (cap_desire - cap) * Kp_cap # + dcap_desire
    u2 = (vitesse_desire - vitesse) * Kp_vit # + dvitesse_desire

    return np.array([u1, u2])


def regulateur_pos(consigne, capteurs, T_carac=0.5):
    """ calcule les commandes en fonction des consignes de position (x, y), vitesse (dx, dy) et accélération (ddx, ddy)

    Args:
        consigne (numpy.ndarray): [x_desire, y_desire, dx_desire, dy_desire, ddx_desire, ddy_desire] en m, m/s et m/s²
        capteurs (numpy.ndarray): [x, y, v, cap] en m, m, m/s et rad
        T_carac (float, optional): temps caractéristique de la réponse souhaitée. Defaults to 0.5.
    """    

    xd, yd, dxd, dyd, ddxd, ddyd = consigne
    x, y, v, cap = capteurs

    
    v1 = (xd - x) +2*T_carac*(dxd - v*np.cos(cap)) + T_carac**2*ddxd
    v2 = (yd - y) +2*T_carac*(dyd - v*np.sin(cap)) + T_carac**2*ddyd

    A = np.array([[-v*np.sin(cap), np.cos(cap)], [v*np.cos(cap), np.sin(cap)]])
    u = np.linalg.inv(A) @ np.array([[v1], [v2]])

    return u.flatten()






    
