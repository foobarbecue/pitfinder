from pitfinder import pitfinder

def cdt():
    pitfinder(
        filepath='..\\meshes\\cdt',
        filename='canyon_diablo_quads.ply',
        tmp_dir="C:/tmp",
        output_file="..\\meshes\\cdt\\EllipsoidData.js",
        is_closed=True,
        filter_sf_range=('0.0', '0.25'),
        conn_comp_oct_lev='5',
        conn_comp_min_pts='500'
    )

def bruno():
    pitfinder(
        filepath='..\\meshes\\bruno',
        filename='bruno_holefilled.ply',
        tmp_dir="C:/tmp",
        output_file="..\\meshes\\bruno\\EllipsoidData.js",
        is_closed=False,
        filter_sf_range=('0.0', '0.34'),
        conn_comp_oct_lev='6',
        conn_comp_min_pts='1000'
    )

bruno()