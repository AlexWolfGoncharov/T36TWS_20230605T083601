
# Sentinel-2 Project

This project provides an example of manually labeled data using the [Groundwork](https://groundwork.element84.com/) service for the area around the Kakhovka HPP as of 2023-06-05, before its destruction. The data includes 3 layers: Water, Fields, and Other. These data will be used for further training of a model to determine water and fields and to assess the impact of the disaster on fields and crops.


Script in this project processes Sentinel-2 imagery and associated ground truth data to create a multi-layer GeoTIFF file. Each layer in the GeoTIFF represents a different class of objects from the ground truth data.

## Project Structure

```
sentinel2_project/
├── data/
│   ├── cropped_image.tif
│   ├── <other_channel_files>.tif
│   ├── labels.geojson
│   ├── labeled_layers.tif  # Generated by the script
├── scripts/
│   ├── convert_labels_to_geotiff.py
├── README.md
```

## How to Use

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/sentinel2_project.git
   cd sentinel2_project
   ```

2. **Place your Sentinel-2 image files and `labels.geojson` in the `data/` directory.**

3. **Run the script to generate the multi-layer GeoTIFF:**
   ```sh
   cd scripts
   python convert_labels_to_geotiff.py
   ```

4. **Check the `data/` directory for the `labeled_layers.tif` file.**

## Requirements

- Python 3.x
- Libraries: `geopandas`, `rasterio`, `numpy`, `matplotlib`, `pyproj`

Install the required libraries using:
```sh
pip install geopandas rasterio numpy matplotlib pyproj
```

## Sample of Data
`labeled_layers.tif`  -- Generated by the script from `labels.geojson`

|Layer|Data class|
| -------- | ------- |
|1| Other|
|2| Field|
|3| Water|



## Project Description

This project processes ground truth data from `labels.geojson` and creates a multi-layer GeoTIFF file. Each layer in the GeoTIFF corresponds to a different class of objects present in the ground truth data.

### Steps in the script:

1. **Load GeoJSON Data:**
   Load the ground truth data from `labels.geojson`.

2. **Create GeoDataFrame:**
   Convert the GeoJSON data to a GeoDataFrame for easy manipulation.

3. **Reproject Data:**
   Reproject the data to UTM zone 33N (EPSG:32633).

4. **Determine Bounding Box:**
   Calculate the bounding box of all geometries to determine the dimensions of the output image.

5. **Rasterize Geometries:**
   Rasterize each class of objects into separate layers.

6. **Create GeoTIFF:**
   Create a multi-layer GeoTIFF file with each layer representing a different class of objects.

7. **Visualize Layers:**
   Display the generated layers for verification.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
