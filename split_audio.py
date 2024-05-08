import os
import argparse
from slugify import slugify
import re


def extract_timestamp(input_string):
    # Define a regular expression pattern for mm:ss or hh:mm:ss format
    pattern = re.compile(r"(\d{1,}:\d{1,}(:\d{1,})?)")

    # Use findall to search for the pattern in the input string
    matches = pattern.findall(input_string)

    # Check if any matches were found
    if matches:
        # Return the first match found (the timestamp)
        return matches[0][0]
    else:
        # Return None if no timestamp is found
        return None


def extract_filename_from_timestamp(input_string: str):
    timestamp = extract_timestamp(input_string)
    slug = slugify(input_string.replace(timestamp, ""), separator="_")
    return (slug, timestamp)


def main():
    parser = argparse.ArgumentParser(description="A simple CLI program.")

    parser.add_argument("audio_file", help="Path to the audio file")
    parser.add_argument("timestamps_file", help="Path to the file with timestamps")
    parser.add_argument("-p", "--prefix", help="ignore timestamp name and add a prefix starting from 1", action="store_true")

    args = parser.parse_args()
    prefix = 1
    with open(args.timestamps_file, "r") as file:
        output_name, from_timestamp = extract_filename_from_timestamp(file.readline())
        lines = file.readlines()
        num_digits = len(str(len(lines)))
        print("ffmpeg -i", '"' + args.audio_file + '" \\')
        for line in lines:
            if args.prefix:
                output_name = os.path.splitext(args.audio_file)[0] + "_" + f"{prefix:0{num_digits}d}"
                prefix += 1
            next_output_name, to_timestamp = extract_filename_from_timestamp(line)
            print("  -ss", from_timestamp, "-to", to_timestamp, "-acodec copy", '"' + output_name + os.path.splitext(args.audio_file)[1] + '" \\')
            output_name, from_timestamp = next_output_name, to_timestamp
        if args.prefix:
            output_name = os.path.splitext(args.audio_file)[0] + "_" + f"{prefix:0{num_digits}d}"
            prefix += 1
        print("  -ss", from_timestamp, "-acodec copy", '"' + output_name + os.path.splitext(args.audio_file)[1] + '"')


if __name__ == "__main__":
    main()

    # Example usage:
    # print(extract_filename_from_timestamp("Chapter 1 - 00:00:00"))
    # print(extract_filename_from_timestamp("This is an example! string with á timestamp at the end: 03:45"))
