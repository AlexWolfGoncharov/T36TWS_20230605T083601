import json
import geopandas as gpd
import rasterio
import numpy as np
from rasterio.transform import from_origin
from rasterio.features import rasterize
from pyproj import CRS
import matplotlib.pyplot as plt


def create_geotiff_from_geojson(geojson_path, reference_tiff_path, output_tiff_path):
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

    # Open the reference GeoTIFF file to get its transform and dimensions
    with rasterio.open(reference_tiff_path) as ref_tiff:
        transform = ref_tiff.transform
        width = ref_tiff.width
        height = ref_tiff.height
        crs = ref_tiff.crs

    # Reproject the GeoDataFrame to match the reference GeoTIFF's CRS
    gdf = gdf.to_crs(crs)

    # Get unique classes from the GeoDataFrame
    classes = gdf['default'].unique()

    # Print information about the layers
    print("Classes and their respective layers:")
    for cls in classes:
        print(f"Class: {cls}")

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
output_tiff_path = '../data/labeled_layers.tif'
reference_tiff_path = '../data/crop_T36TWS_20230605T083601_TCI_20m.tif'  # Reference GeoTIFF file path


create_geotiff_from_geojson(geojson_path, reference_tiff_path, output_tiff_path)


