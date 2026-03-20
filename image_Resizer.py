import argparse
from PIL import Image
import os

def resize_image(input_path, width, height):
    """
    Resize the image to cover the specified width and height,
    maintaining aspect ratio by cropping if necessary.
    """
    img = Image.open(input_path)
    img_ratio = img.width / img.height
    target_ratio = width / height

    if img_ratio > target_ratio:
        # Image is wider, crop width
        new_width = int(img.height * target_ratio)
        offset = (img.width - new_width) // 2
        img = img.crop((offset, 0, offset + new_width, img.height))
    elif img_ratio < target_ratio:
        # Image is taller, crop height
        new_height = int(img.width / target_ratio)
        offset = (img.height - new_height) // 2
        img = img.crop((0, offset, img.width, offset + new_height))

    # Resize to exact target size
    img = img.resize((width, height), Image.LANCZOS)
    return img

def create_2x_version(resized_img, output_path_2x):
    """
    Create a 2x version of the resized image.
    """
    new_width = resized_img.width * 2
    new_height = resized_img.height * 2
    img_2x = resized_img.resize((new_width, new_height), Image.LANCZOS)
    img_2x.save(output_path_2x)

def main():
    parser = argparse.ArgumentParser(description='Resize an image to fit specified dimensions and create a 2x version.')
    parser.add_argument('--input', required=True, help='Path to the input image')
    parser.add_argument('--width', type=int, required=True, help='Target width in pixels')
    parser.add_argument('--height', type=int, required=True, help='Target height in pixels')
    parser.add_argument('--output', required=True, help='Path to save the resized image')
    parser.add_argument('--output_2x', help='Path to save the 2x version (optional, defaults to output with @2x suffix)')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return

    # Determine output paths
    if os.path.isdir(args.output):
        input_filename = os.path.basename(args.input)
        base, ext = os.path.splitext(input_filename)
        output_path = os.path.join(args.output, f"{base}_resized{ext}")
    else:
        output_path = args.output

    # Resize the image
    resized_img = resize_image(args.input, args.width, args.height)
    resized_img.save(output_path)
    print(f"Resized image saved to {output_path}")

    # Create 2x version
    if args.output_2x:
        if os.path.isdir(args.output_2x):
            output_2x = os.path.join(args.output_2x, f"{base}_resized@2x{ext}")
        else:
            output_2x = args.output_2x
    else:
        base_out, ext_out = os.path.splitext(output_path)
        output_2x = f"{base_out}@2x{ext_out}"

    create_2x_version(resized_img, output_2x)
    print(f"2x version saved to {output_2x}")

if __name__ == "__main__":
    main()
