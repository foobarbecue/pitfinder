from clize import run
from os import path, chdir
import subprocess
from glob import glob
import numpy as np
import json
import math
from ellipsoid_fit import ellipsoid_fit, data_regularize

cc_exec_path = 'C:\\Users\\aaron\\CloudCompareProjects\\CloudCompare_debug\\CloudCompare.exe'

def rotationMatrixToEulerAngles(R):
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


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
    ellipsoid_data = []
    for n, pit_cloud in enumerate(pit_clouds):
        pit_cloud_mat = np.loadtxt(pit_cloud)
        # et = EllipsoidTool() # Why is this a class?
        # center, radii, rotation = et.getMinVolEllipse(pit_cloud_mat[:, :3], tolerance=0.1)
        data_regd = data_regularize(pit_cloud_mat[:, :3], divs=16)
        center, radii, evecs, v = ellipsoid_fit(data_regd)
        rotation = rotationMatrixToEulerAngles(evecs)
        print("{}, {}, {}".format(center, radii, rotation))
        ellipsoid_data.append({'center': center.tolist(),
                           'radii': radii.tolist(),
                           'rotation': rotation.tolist()})
    with open('EllipsoidData.js', 'w') as ellipse_file:
        ellipse_file.write(f'window.ellipses = {ellipsoid_data}')
        # ctr, radii, evecs, v = ellipsoid_fit(pit_cloud_mat)

pitfinder()

# if __name__ == "__main__":
#     run(pitfinder)
