'''
This script analyzes single-band GeoTIFF files in a specified directory.
It retrieves the filename, size, compression type, data type,
no data value, minimum value, and maximum value using GDAL.
It also provides options to save the results in Markdown or plain text format.
'''
import os
import glob
from osgeo import gdal

def get_file_size(file_path):
    """
    Returns file size in MB
    """
    return os.path.getsize(file_path) / (1024 * 1024)

def analyze_geotiff_files(file_list):
    """
    Analyses a list of single-band GeoTIFF files and returns their
    filename, size, compression, data type, no data value, min value, and max value using GDAL.
    
    Args:
        file_list (list): List of paths to GeoTIFF files
        
    Returns:
        list: List of dictionaries containing analysis results for each file
    """
    # Register all GDAL drivers
    gdal.AllRegister()
    
    results = []
    
    for file_path in file_list:
        try:
            # Open the dataset
            ds = gdal.Open(file_path)
            if ds is None:
                print(f"Error: Could not open {os.path.basename(file_path)}")
                continue
            
            # Check if it's a single band file
            if ds.RasterCount != 1:
                print(f"Warning: {os.path.basename(file_path)} has {ds.RasterCount} bands, not a single band file.")
                continue
            
            # Get the band
            band = ds.GetRasterBand(1)
            
            # Get file size in MB
            file_size = get_file_size(file_path)
            
            # Get compression type
            metadata = ds.GetMetadata()
            compression = ds.GetMetadata('IMAGE_STRUCTURE').get('COMPRESSION', 'None')
            
            # Get data type
            data_type = gdal.GetDataTypeName(band.DataType)
            
            # Get the no data value
            nodata = band.GetNoDataValue()
            
            # Get statistics (min, max, mean, stddev)
            stats = band.GetStatistics(1, 1)
            min_val = stats[0]
            max_val = stats[1]
            
            # Store the results
            results.append({
                'filename': os.path.basename(file_path),
                'file_size': file_size,
                'compression': compression,
                'data_type': data_type,
                'nodata_value': nodata,
                'min_value': min_val,
                'max_value': max_val
            })
            
            print(f"Processed: {os.path.basename(file_path)}")
            
            # Close the dataset
            ds = None
            
        except Exception as e:
            print(f"Error processing {os.path.basename(file_path)}: {str(e)}")
    
    return results

def print_results(results):
    """
    Prints the analysis results in a formatted way.
    
    Args:
        results (list): List of dictionaries containing analysis results
    """
    print("\nGeoTIFF Analysis Results:")
    print("-" * 120)
    print(f"{'Filename':<30} {'Size (MB)':<10} {'Compression':<12} {'Data Type':<10} {'No Data':<10} {'Min Value':<15} {'Max Value':<15}")
    print("-" * 120)
    
    for result in results:
        nodata_str = str(result['nodata_value']) if result['nodata_value'] is not None else "None"
        print(f"{result['filename']:<30} {result['file_size']:<10.2f} {result['compression']:<12} {result['data_type']:<10} "
              f"{nodata_str:<10} {result['min_value']:<15.6f} {result['max_value']:<15.6f}")

def save_markdown_results(results, output_file='analysis_results.md'):
    """
    Saves the analysis results in a Markdown formatted table.
    
    Args:
        results (list): List of dictionaries containing analysis results
        output_file (str): Path to output markdown file
    """
    with open(output_file, 'w') as f:
        f.write("# GeoTIFF Analysis Results\n\n")
        f.write("| Filename | Size (MB) | Compression | Data Type | No Data | Min Value | Max Value |\n")
        f.write("|----------|-----------|-------------|-----------|----------|-----------|------------|\n")
        
        for result in results:
            nodata_str = str(result['nodata_value']) if result['nodata_value'] is not None else "None"
            f.write(f"| {result['filename']} | {result['file_size']:.2f} | {result['compression']} | "
                   f"{result['data_type']} | {nodata_str} | {result['min_value']:.6f} | {result['max_value']:.6f} |\n")

def save_text_results(results, output_file='analysis_results.txt'):
    """
    Saves the analysis results in a plain text format.
    
    Args:
        results (list): List of dictionaries containing analysis results
        output_file (str): Path to output text file
    """
    with open(output_file, 'w') as f:
        f.write("GeoTIFF Analysis Results\n")
        f.write("-" * 120 + "\n")
        f.write(f"{'Filename':<30} {'Size (MB)':<10} {'Compression':<12} {'Data Type':<10} "
                f"{'No Data':<10} {'Min Value':<15} {'Max Value':<15}\n")
        f.write("-" * 120 + "\n")
        
        for result in results:
            nodata_str = str(result['nodata_value']) if result['nodata_value'] is not None else "None"
            f.write(f"{result['filename']:<30} {result['file_size']:<10.2f} {result['compression']:<12} "
                   f"{result['data_type']:<10} {nodata_str:<10} {result['min_value']:<15.6f} "
                   f"{result['max_value']:<15.6f}\n")

if __name__ == "__main__":
    geotiff_dir = "/Volumes/MyShare/lidar"
    #geotiff_dir = "/Volumes/MyShare/lidar_deflate"
    #geotiff_dir = "/Users/alexdonald/Downloads/newlidar"
    file_list = glob.glob(os.path.join(geotiff_dir, "*.tif"))
    
    if not file_list:
        print(f"No GeoTIFF files found in {geotiff_dir}")
    else:
        results = analyze_geotiff_files(file_list)
        # Sort results by filename
        results.sort(key=lambda x: x['filename'])
        print_results(results)  # Print results to console
        save_markdown_results(results)  # Save as markdown
        save_text_results(results)  # Save as text file