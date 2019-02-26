from pitfinder import pitfinder

def cdt():
    pitfinder(
        filepath='..\\meshes\\cdt',
        filename='canyon_diablo_quads.ply',
        tmp_dir="C:/tmp",
        output_file="..\\meshes\\cdt\\EllipsoidData.js",
        is_closed=True,
        filter_sf_range=(0.0, 0.25)
    )

def bruno():
    pitfinder(
        filepath='..\\meshes\\bruno',
        filename='bruno.ply',
        tmp_dir="C:/tmp",
        output_file="..\\meshes\\bruno\\EllipsoidData.js",
        is_closed=False,
        filter_sf_range=(0.0, 0.47)
    )