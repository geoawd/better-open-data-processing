'''
simple scriot to convert files with deflate compression and statistics
'''
import os
from osgeo import gdal

input_dir = r'lidar/'
output_dir = r'newlidar/'

for f in os.listdir(input_dir):
    if f.endswith('.tif'):
        input_file = os.path.join(input_dir, f)
        output_file = os.path.join(output_dir, f)
        
        translate_options = gdal.TranslateOptions(
            format='COG',
            creationOptions=["COMPRESS=ZSTD", "PREDICTOR=2", "NUM_THREADS=ALL_CPUS", "STATISTICS=Yes"],
            outputSRS='EPSG:29902'
        )
        
        gdal.Translate(output_file, input_file, options=translate_options)
