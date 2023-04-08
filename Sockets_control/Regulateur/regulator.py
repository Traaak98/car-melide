import numpy as np

def ech(x):
    return 0.5*(np.sign(x)+1)
def ech_radial(x,y,r):
    return 0.5*(np.sign(r**2-(x**2+y**2))+1)

def repulsive(x,y,cx):
    def repuls0(x,y): 
        norm = np.sqrt(x**2+y**2)   
        return x/norm,y/norm
    
    z1 =  x-cx
    z2 =  y
    w1,w2=repuls0(z1,z2)
    v1 =  w1
    v2 =  w2
    return v1,v2
def centre_repulsive(x,y,d,r):
    v1l,v2l=repulsive(x,y,-d/2)
    v1r,v2r=repulsive(x,y,d/2)
    v1u,v2u=0,1
    v1d,v2d=0,-1
    R=ech(x-d/2)*ech_radial(x-d/2,y,r)  # Right circle
    L=ech(-x-d/2)*ech_radial(-x-d/2,y,r) # Left
    U=ech(y)*ech(r-y)*(1-ech(x-d/2))*(1-ech(-x-d/2))   # Up line
    D=ech(-y)*ech(r+y)*(1-ech(x-d/2))*(1-ech(-x-d/2))  # Down
    v1=R*v1r+L*v1l+U*v1u+D*v1d
    v2=R*v2r+L*v2l+U*v2u+D*v2d
    return v1,v2

def attractive(x,y,cx):
    def attract0(x,y): 
        norm = np.sqrt(x**2+y**2)   
        return -x/norm,-y/norm
    
    z1 =  x-cx
    z2 =  y
    w1,w2=attract0(z1,z2)
    v1 =  w1
    v2 =  w2
    return v1,v2
def centre_attractive(x,y,d,r):
    v1l,v2l=attractive(x,y,-d/2)
    v1r,v2r=attractive(x,y,d/2)
    v1u,v2u=0,-1
    v1d,v2d=0,1
    R=ech(x-d/2)*(1-ech_radial(x-d/2,y,r))  # Right circle
    L=ech(-d/2-x)*(1-ech_radial(-x-d/2,y,r)) # Left
    U=ech(y)*ech(y-r)*(1-ech(x-d/2))*(1-ech(-x-d/2))   # Up line
    D=ech(-y)*ech(-y-r)*(1-ech(x-d/2))*(1-ech(-x-d/2))  # Down
    v1=R*v1r+L*v1l+U*v1u+D*v1d
    v2=R*v2r+L*v2l+U*v2u+D*v2d
    return v1,v2   

def circle(x,y,cx,R):
    def circle0(x,y):        
        return -(x**3+y**2*x-x+y),-(y**3+x**2*y-x-y)
    
    D=np.array([[R,0],[0,R]])
    D_=np.linalg.inv(D)
    z1 =  D_[0,0]*(x-cx) + D_[0,1]*(y)
    z2 =  D_[1,0]*(x-cx) + D_[1,1]*(y)
    w1,w2=circle0(z1,z2)
    v1 =  D[0,0]*w1 + D[0,1]*w2
    v2 =  D[1,0]*w1 + D[1,1]*w2
    return v1,v2
def centre_circuit(x,y,d,r):
    v1l,v2l=circle(x,y,-d/2,r)
    v1r,v2r=circle(x,y,d/2,r)
    v1u,v2u=-1,np.arctan(-y+r)
    v1d,v2d=1,np.arctan(-y-r)
    R=ech(x-d/2)  # Right circle
    L=ech(-x-d/2) # Left
    U=ech(y)*(1-R)*(1-L)   # Up line
    D=ech(-y)*(1-R)*(1-L)  # Down
    v1=R*v1r+L*v1l+U*v1u+D*v1d
    v2=R*v2r+L*v2l+U*v2u+D*v2d
    return v1,v2




def circuit(x,y,a,b,R,largeur):
    theta=np.arctan2(a[1]-b[1],b[0]-a[0])

    D = np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]])
    D_=np.linalg.inv(D)
    z1 =  D_[0,0]*(x-(a[0]+b[0])/2) + D_[0,1]*(y-(a[1]+b[1])/2)
    z2 =  D_[1,0]*(x-(a[0]+b[0])/2) + D_[1,1]*(y-(a[1]+b[1])/2)

    d = np.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)
    c1, c2 = centre_circuit(z1,z2,d,R)
    a1,a2=centre_attractive(z1,z2,d,R+largeur/2)
    r1,r2=centre_repulsive(z1,z2,d,R-largeur/2)
    v1 = c1 + 100*a1 + 100*r1
    v2 = c2 + 100*a2 + 100*r2

    w1 =  D[0,0]*v1 + D[0,1]*v2
    w2 =  D[1,0]*v1 + D[1,1]*v2

    return w1,w2

def circuit_plot(x,y,a,b,R,largeur):
    theta=np.arctan2(a[1]-b[1],b[0]-a[0])

    D = np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]])
    D_=np.linalg.inv(D)
    z1 =  D_[0,0]*(x-(a[0]+b[0])/2) + D_[0,1]*(y-(a[1]+b[1])/2)
    z2 =  D_[1,0]*(x-(a[0]+b[0])/2) + D_[1,1]*(y-(a[1]+b[1])/2)

    d = np.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)
    c1, c2 = centre_circuit(z1,z2,d,R)
    a1,a2=centre_attractive(z1,z2,d,R+largeur/2)
    r1,r2=centre_repulsive(z1,z2,d,R-largeur/2)
    v1 = 100*a1 + 100*r1
    v2 = 100*a2 + 100*r2

    w1 =  D[0,0]*v1 + D[0,1]*v2
    w2 =  D[1,0]*v1 + D[1,1]*v2

    return w1,w2



def plot_vector_field(ax, f, xlim,ylim, step, *args):
    Mx, My = np.arange(xlim[0], xlim[1], step), np.arange(ylim[0],ylim[1], step)
    X1, X2 = np.meshgrid(Mx, My)

    VX, VY = f(X1, X2, *args)
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