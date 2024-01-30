

def detectUnusualGeom(fileloc, negbuff=20):
    ''' Inputs are GEOJSON location string, negative buffer in meters (default 20).  \n
    Outputs same GEOJSON with 0-1 unusual shape perimeter index ('USPI' column), \n
    and whether negative buffer omitted row feature or not ('buffomit' column). \n
    Final file will ouput in same directory as the original file, with an additional "_GeomChecks" in the filename'''
    import geopandas as gpd
    import os
    import math

    try_n = 0
    negbuff = abs(negbuff)
    try:  # Reading geofile, chdir
        fileloc = os.path.join(fileloc)
        os.chdir('{}'.format(os.path.dirname(fileloc)))
        vec = gpd.read_file(fileloc)
        try_n = try_n + 1
    except:
        print('File reading fail')
    try:  # Computation of the USPI
        vec_modified = vec.to_crs("EPSG:3857")
        vec_modified['area_m'] = vec_modified.area
        vec_modified['circ_radius'] = (vec_modified['area_m'] / math.pi) ** (1 / 2)
        vec_modified['circ_Per'] = 2 * math.pi * vec_modified['circ_radius']
        vec_modified['perimeter_m'] = vec_modified.length
        vec_modified['USPI'] = vec_modified['circ_Per'] / vec_modified['perimeter_m']
        try_n = try_n + 1
    except:
        print('Computation of unusual shape perimeter index failed!')
    try:  # Negative buffer section:
        vec_modified['negBuffGeom'] = vec_modified['geometry'].buffer(-negbuff)
        vec_modified['BuffOmit'] = vec_modified['negBuffGeom'].is_empty
        try_n = try_n + 1
    except:
        print('Computation of negative buffer flag failed!')
    try:  # Dropping irrelevant columns
        vec_modified.drop(columns=['circ_radius',
                                   'circ_Per', 'perimeter_m', 'area_m',
                                   'negBuffGeom'], inplace=True)
        try_n = try_n + 1
    except:
        print('Final column drop failed!')
    try:  # Back to EPSG:4326 & export to final GEOJSON
        vec_modified = vec_modified.to_crs("EPSG:4326")
        try_n = try_n + 1
        if (try_n == 5):
            vec_modified.to_file("{}_GeomChecks.gpkg".format(fileloc.split('\\')[-1].split('.')[0]),
                                 driver='GPKG')
            print('Final GPKG export success!')
    except:
        print('Reprojection back to EPSG:4326 / final file export failed!')
detectUnusualGeom(r"C:\Users\User\Documents\2022_2023_Proag_data\df_clus_both_2022_2023_data_second_DB.gpkg", negbuff = 20)