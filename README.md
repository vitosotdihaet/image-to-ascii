# Image To ASCII
Outputs an image to a file named `out-<current-time>.txt` or to terminal drawn with ASCII symbols using python and pillow

To run the program just run the following lines in your terminal:

```
python3 main.py <path-to-image>
```

After doing so you can copy ASCII repesentation of your image from the terminal

## Options
Flags:

`-s`/`--save` -- save ASCII art to a file

`-c`/`--compression [FLOAT]` -- set the compression of your ASCII art compared to target image

`-i`/`--inverse` -- inverse brightness

`-w`/`--width [FLOAT]` -- change width of every pixel (because height of glyphs != its width)

TODO: Make a better preview
