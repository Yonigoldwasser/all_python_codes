import os
import pandas as pd
import geopandas as gpd
# import openynxl
# import xlsxWriter
path = r"C:\Users\User\Documents\ProAg2022_test\ProAg_2022_test_IN_15_6-1_9_2023-05-02_ci_preds\ProAg_2022_test_IN_15_6-1_9_2023-05-02_ci_preds"
files = os.listdir(path)
#all_df = pd.Dataframe()
tile_list = []
acc_list = []
cdlHsL_list = []
kappa_list = []
cdlHsV_list = []
for file in files:
    if file.endswith(".geojson"):
        print(file)
        df = gpd.read_file(os.path.join(path, file))
        acc_list.append(df['accuracy'][0])
        tile_list.append(df['tile'][0])
        cdlHsL_list.append(df['cdlHsL'][0])
        kappa_list.append(df['kappa'][0])
        cdlHsV_list.append(df['cdlHsV'][0])
# print(tile_list)
# path2 = r"C:\Users\User\Documents\CC_tests-20230308\CC_tests\CC_byArea_and_crop_VS_regular\training_NorthArkansas_area_2023-04-05\training_NorthArkansas_area_2023-04-05_ci_preds"
# files2 = os.listdir(path2)
# for file in files2:
#     if file.endswith(".geojson"):
#         print(file)
#         df = gpd.read_file(os.path.join(path2, file))
#         acc_list.append(df['accuracy'][0])
#         tile_list.append(df['tile'][0])
#         cdlHsL_list.append(df['cdlHsL'][0])
#         kappa_list.append(df['kappa'][0])
#         cdlHsV_list.append(df['cdlHsV'][0])
all_df = pd.DataFrame(data=tile_list)
all_df.insert(1, 'acc_area', acc_list)
all_df.insert(2, 'cdlHsL_area', cdlHsL_list)
all_df.insert(3, 'cdlHsV_area', cdlHsV_list)
all_df.insert(4, 'kappa_area', kappa_list)
all_df.to_excel(r"C:\Users\User\Documents\ProAg2022_test\ProAg_2022_test_IN_15_6-1_9_2023-05-02_ci_preds.xlsx")
print(all_df)