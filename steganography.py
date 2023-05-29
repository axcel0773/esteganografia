import argparse
import stegano_functions as stg

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-m', '--message', help="Message that will be inserted inside the image")
    parser.add_argument('-p', '--image_path', help="Image path that will receive the text")
    parser.add_argument('-o', '--image_path_out', help="Image output path")
    parser.add_argument('-e', '--extract', help="Encrypt text", action='store_true')
    parser.add_argument('-i', '--insert', help="decrypt text", action='store_true')

    args = parser.parse_args()

    path_out = args.image_path_out
    if args.insert:
        message = args.message
        path_in = args.image_path

        stg.encode_image(path_in, message, path_out)
    elif args.extract:
        stg.decode_image(path_out)


if __name__ == '__main__':
    main()
