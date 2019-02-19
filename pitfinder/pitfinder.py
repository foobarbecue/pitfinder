from clize import run
from os import path, chdir
import subprocess
from glob import glob


cc_exec_path = 'C:\\Users\\aaron\\CloudCompareProjects\\CloudCompare_debug\\CloudCompare.exe'

def pitfinder(filepath='S:\\active\\pitfinder\\meshes',
              filename='canyon_diablo_quads.ply', tmp_dir="C:/tmp"):
    print('stuffs')
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
                    '-FILTER_SF', '0.0', '0.25',
                    '-EXTRACT_CC', '5', '500'
                    ])

if __name__ == "__main__":
    run(pitfinder)
