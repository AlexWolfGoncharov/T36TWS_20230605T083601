import json
import geopandas as gpd
import rasterio
import numpy as np
from rasterio.transform import from_origin
from rasterio.features import rasterize
from pyproj import CRS
import matplotlib.pyplot as plt

def create_geotiff_from_geojson(geojson_path, output_tiff_path):
    # Load GeoJSON data
    with open(geojson_path) as f:
        geojson_data = json.load(f)

    # Create a GeoDataFrame from GeoJSON
    gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])

    # Ensure the 'default' key exists in properties
    if 'default' not in gdf.columns:
        raise KeyError("The key 'default' is not found in the GeoJSON properties.")

    # Set initial CRS if not present (assuming WGS84 for GeoJSON)
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)  # WGS84

    # Reproject to UTM (meters)
    gdf = gdf.to_crs(epsg=32633)  # UTM zone 33N, WGS84

    # Get unique classes from the GeoDataFrame
    classes = gdf['default'].unique()

    # Print information about the layers
    print("Classes and their respective layers:")
    for cls in classes:
        print(f"Class: {cls}")

    # Determine the bounding box of all geometries in the GeoJSON
    bounds = gdf.total_bounds  # returns (minx, miny, maxx, maxy)
    print(f"Bounding box: {bounds}")

    # Define the resolution
    resolution = 20  # 20 meters per pixel

    # Calculate the dimensions of the output image
    width = int((bounds[2] - bounds[0]) / resolution)
    height = int((bounds[3] - bounds[1]) / resolution)
    
    # Ensure width and height are greater than 0
    if width <= 0 or height <= 0:
        raise ValueError("Calculated width and height must be greater than 0. Check the bounds and resolution.")

    # Calculate the transform for the output image
    transform = from_origin(bounds[0], bounds[3], resolution, resolution)

    # Define the CRS using pyproj
    crs = CRS.from_epsg(32633)  # UTM zone 33N, WGS84

    # Create an empty array for each class
    layers = {cls: np.zeros((height, width), dtype=np.uint8) for cls in classes}

    # Rasterize each class into its respective layer
    for cls in classes:
        shapes = [(geom, 1) for geom in gdf[gdf['default'] == cls].geometry]
        layers[cls] = rasterize(shapes, out_shape=(height, width), transform=transform, fill=0, dtype=np.uint8)

    # Create GeoTIFF with multiple layers
    with rasterio.open(
        output_tiff_path, 'w', 
        driver='GTiff', 
        height=height, 
        width=width, 
        count=len(classes), 
        dtype=np.uint8, 
        crs=crs.to_wkt(), 
        transform=transform
    ) as dst:
        for idx, (cls, layer) in enumerate(layers.items(), start=1):
            dst.write(layer, idx)

    # Display the created layers
    fig, axes = plt.subplots(1, len(classes), figsize=(15, 5))
    if len(classes) == 1:
        axes = [axes]
    for ax, (cls, layer) in zip(axes, layers.items()):
        ax.imshow(layer, cmap='gray')
        ax.set_title(f"Class: {cls}")
    plt.show()

# Paths
geojson_path = '../data/labels.geojson'
output_tiff_path = '../data/output_layers.tif'

create_geotiff_from_geojson(geojson_path, output_tiff_path)

