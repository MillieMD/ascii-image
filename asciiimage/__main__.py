# IMPORTS
import sys
import os
import argparse
import colorsys

CHARS_BY_LUMINANCE = [" ", "░", "▒", "▓", "█"]

def error(message : str):
    print(message, file=sys.stderr)
    exit(1)

def warn(message : str):
    print(message, file=sys.stderr)

def main():

    parser = argparse.ArgumentParser(
        prog="ascii-image",
        description="Convert an image file to ascii art",
    )

    parser.add_argument("img", help="file to display")

    args = parser.parse_args()

    try:
        with open(args.img, "rb") as file:

            # Check that file is a bitmap image
            signature = file.read(2).decode("utf-8")
            if signature != "BM":
                error(f"{args.img} must be a Bitmap image")

            total_bytes = int.from_bytes(file.read(4), "little")

            # Width
            file.seek(0x0012)
            pixel_width = int.from_bytes(file.read(4), "little")

            terminal_width = os.get_terminal_size()[0]
            if pixel_width > terminal_width:
                warn(f"image width is larger than number of terminal columns. Image may not display properly.\n Terminal width is: {terminal_width} cols, image width is {pixel_width}px")

            # Pixel data is padded with 0s so that each scan line is a multiple of 4
            bytes_per_line = pixel_width*3 

            if pixel_width * 3%4 !=0:
                bytes_per_line = pixel_width*3 + (4-(pixel_width*3)%4)

            # Get compression type
            file.seek(0x001E)
            encoding = int.from_bytes(file.read(4), "little")

            # Compression 0 = no encoding, 1 or 2 is RLE decoding
            if encoding != 0:
                error("Run length decoding is not supported")

            # Pixel data starts at byte 55, assuming no colour table i.e. BitsPerPixel > 8. This is usually the case.
            for line_index in range(total_bytes-bytes_per_line, 0x0036-1, -bytes_per_line):
                file.seek(line_index)
                line = file.read(bytes_per_line)

                for byte_index in range(0, pixel_width*3, 3):
                    red = line[byte_index]/255
                    green = line[byte_index + 1]/255
                    blue = line[byte_index + 2]/255

                    # Convert to HLS to get the luminance of each pixel
                    luminance = colorsys.rgb_to_hls(red, green, blue)[1]
                    # Maps to CHARS_BY_LUMINANCE
                    luminance_index = int(round(luminance*(len(CHARS_BY_LUMINANCE)-1), 0))

                    print(CHARS_BY_LUMINANCE[luminance_index], end="")
                    
                print("")

                
    except FileNotFoundError:
        error(f"{args.img} does not exist")

if __name__ == '__main__':
    main()