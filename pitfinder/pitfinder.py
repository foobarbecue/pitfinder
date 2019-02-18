from clize import run
from os import path, chdir
import subprocess

cc_exec_path = 'C:/Users/aaron/CloudCompareProjects/CloudCompare_debug/CloudCompare.exe'


def pitfinder(filepath='S:/active/pitfinder/meshes', filename='canyon_diablo_quads.ply', tmp_dir="C:/tmp"):
    chdir(filepath)
    subprocess.run([cc_exec_path,
                    '-O', path.join(filepath, filename),    # Load input
                    '-C_EXPORT_FMT', 'PLY',                 # Set output to PLY
                    '-PCV',                                 # Do ambient occlusion (Portion de Ciel Visible / ShadeVis)
                        '-N_RAYS', '256',
                        '-IS_CLOSED',
                        '-RESOLUTION', '1024',
                    '-EXTRACT_VERTICES',
                    '-FILTER_SF', '0.0', '0.25',
                    '-SAVE_CLOUDS'
                    ])


if __name__ == "__main__":
    run(pitfinder)
