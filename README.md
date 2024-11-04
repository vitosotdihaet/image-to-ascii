# Image To ASCII
Outputs an image to a file named `out-<current-time>.txt` or to terminal drawn with ASCII symbols using python and pillow

To run the program just run the following lines in your terminal:

```
python3 main.py <path-to-image>
```

After doing so you can copy ASCII repesentation of your image from the terminal

## Options
```
usage: main.py [-h] [-c COMPRESSION] [-i] [-p {red,green,blue,grayscale,diff}] [-e {unweighted,horizontal,vertical,gaussian}] [-w WIDTH] [-s] path

positional arguments:
  path                  Path to an image file

options:
  -h, --help            show this help message and exit
  -c COMPRESSION, --compression COMPRESSION
                        Coefficient of a compression: if compression is 0.5, the resolution goes from 1920x1080 to 960x540
  -i, --inverse         Inverse the brightness
  -p {red,green,blue,grayscale,diff}, --pixel_to_value_function {red,green,blue,grayscale,diff}
                        A function to interpret colors as floats
  -e {unweighted,horizontal,vertical,gaussian}, --edge_detection_matrix {unweighted,horizontal,vertical,gaussian}
                        A matrix for edge detections
  -w WIDTH, --width WIDTH
                        Ratio of width multiplication (reason is char's height is bigger than its width)
  -s, --save            Save the output to a file <image_name>.txt
```
