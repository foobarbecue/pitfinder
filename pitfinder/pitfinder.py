from clize import run
from os import path, chdir
import subprocess
from glob import glob
import numpy as np

cc_exec_path = 'C:\\Users\\aaron\\CloudCompareProjects\\CloudCompare_debug\\CloudCompare.exe'

def pitfinder(filepath='S:\\active\\pitfinder\\meshes',
              filename='canyon_diablo_quads.ply', tmp_dir="C:/tmp"):
    chdir(filepath)
    subprocess.run([cc_exec_path,
                    '-SILENT',
                    '-O', path.join(filepath, filename),    # Load input
                    '-C_EXPORT_FMT', 'PLY',                 # Set output to PLY
                    '-PCV',                                 # Do ambient occlusion (Portion de Ciel Visible / ShadeVis)
                        '-N_RAYS', '256',
                        '-IS_CLOSED',
                        '-RESOLUTION', '1024',
                    '-EXTRACT_VERTICES'
                    ])

    # This is only a second process because of https://github.com/CloudCompare/CloudCompare/issues/847
    point_cloud_filename = glob(path.join(filepath, filename[:-4] + '*vertices*.ply'))[-1]
    subprocess.run([cc_exec_path,
                    '-SILENT',
                    '-O', point_cloud_filename,
                    '-C_EXPORT_FMT', 'ASC',
                    '-FILTER_SF', '0.0', '0.25',
                    '-EXTRACT_CC', '5', '500'
                    ])
    pit_clouds = glob(path.join(filepath, filename[:-4] + '*vertices*.asc'))
    for cloud in pit_clouds:
        pit_cloud_mat = np.loadtxt(cloud)
        # et = EllipsoidTool() # Why is this a class?
        # center, radii, rotation = et.getMinVolEllipse(pit_cloud_mat[:, :3], tolerance=0.1)

        print("{}, {}, {}".format(center, radii, rotation))
        with open(cloud[:-4] + 'elps.txt', 'w') as ellipse_file:
            ellipse_file.write('Center: {} \nRadii: {} \nRotation matrix: {}'
                               .format(center, radii, rotation))

        # ctr, radii, evecs, v = ellipsoid_fit(pit_cloud_mat)

#from https://github.com/aleksandrbazhin/ellipsoid_fit_python/blob/master/ellipsoid_fit.py
def ellipsoid_fit(X):
    x = X[:, 0]
    y = X[:, 1]
    z = X[:, 2]
    D = np.array([x * x,
                 y * y,
                 z * z,
                 2 * x * y,
                 2 * x * z,
                 2 * y * z,
                 2 * x,
                 2 * y,
                 2 * z])
    DT = D.conj().T
    v = np.linalg.solve( D.dot(DT), D.dot( np.ones( np.size(x) ) ) )
    A = np.array([[v[0], v[3], v[4], v[6]],
                  [v[3], v[1], v[5], v[7]],
                  [v[4], v[5], v[2], v[8]],
                  [v[6], v[7], v[8], -1]])

    center = np.linalg.solve(- A[:3, :3], [[v[6]], [v[7]], [v[8]]])
    T = np.eye(4)
    T[3,:3] = center.T
    R = T.dot(A).dot(T.conj().T)
    evals, evecs = np.linalg.eig(R[:3, :3] / -R[3, 3])
    radii = np.sqrt(1. / evals) # problem: negative evals
    return center, radii, evecs, v

pitfinder()

# if __name__ == "__main__":
#     run(pitfinder)
