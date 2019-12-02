import numpy as np
import matplotlib.pyplot as pl
from matplotlib.patches import RegularPolygon
import h5py

# LOAD IN THE DATA
def loadfile(positionFile,dataFile,nDomains):
    h5f = h5py.File(positionFile,'r')
    x = h5f['x'][:]
    y = h5f['y'][:]
    n = len(x)
    h5f.close()
    h5f = h5py.File(dataFile,'r')
    A = h5f['a0'][:]
    for i in range(nDomains):
        A = np.vstack([A,h5f['a'+str(i)][:]])
    C = h5f['c0'][:]
    for i in np.arange(nDomains):
        C = np.vstack([C,h5f['c'+str(i)][:]])
    h5f.close()
    return C[1:,:],A[1:,:],x,y,n

def plotHexMap(f,Col,X,Y,n,rad=0.006):
    for i in range(n):
        hex = RegularPolygon((X[i], Y[i]),numVertices=6, radius=rad,
                             facecolor=Col[i],edgecolor='none')
        f.add_patch(hex)
        f.axis(np.array([-1,1,-1,1])*0.9)
        f.set_aspect(np.diff(f.get_xlim())/np.diff(f.get_ylim()))
        f.set_xticks([])
        f.set_yticks([])

C,A,X,Y,n = loadfile('/home/seb/gdrive_usfd/data/BarrelEmerge/25N2M_rect_1/positions.h5','/home/seb/gdrive_usfd/data/BarrelEmerge/25N2M_rect_1/c_04000.h5',25)

Cid = np.argmax(C,axis=0)
Cmax  = np.max(C,axis=0)
Csum  = np.sum(C,axis=0)
Csumsum = np.sum(Csum)

Aid = np.argmax(A,axis=0)
Amax  = np.max(A,axis=0)
Asum  = np.sum(A,axis=0)
Asumsum = np.sum(A)

# DEFINE COLOURS
n_grid = 5
xmax = 1.*(np.floor(Cid/n_grid))
ymax = 1.*(Cid%n_grid)
norm = 1./(n_grid-1.)
Col = np.zeros([n,3])
for i in range(n):
    Col[i] = np.array([xmax[i]*norm,0,ymax[i]*norm])

# PLOTTING
F = pl.figure(figsize=(12,12))
f = F.add_subplot(111)
plotHexMap(f,Col,X,Y,n)
f.tricontour(X, Y, Cmax/Csum,linewidths=3.0, colors="white", levels=[0.95])
pl.savefig('fig.pdf')

#pl.show()
