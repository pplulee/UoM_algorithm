import string
import random
import sys
import os


def generate_dictionary(words, number, out_file, sorting=None):
    print(":: Generating dictionary")
    if os.path.exists(out_file):
        print(f" WARN: Overwriting existing '{out_file}'")

    if sorting == "sorted":
        print(" -> Sorting dictionary")
        with open(out_file, "w") as f:
            f.write("\n".join(sorted(words[:number])) + "\n")
    elif sorting == "reverse":
        print(" -> Reverse sorting dictionary")
        with open(out_file, "w") as f:
            f.write("\n".join(sorted(words[:number], reverse=True)) + "\n")
    elif sorting == "random":
        print(" -> Randomising dictionary")
        random.shuffle(words)
        with open(out_file, "w") as f:
            f.write("\n".join(words[:number]) + "\n")
    else:
        print(" -> No sorting performed")
        with open(out_file, "w") as f:
            f.write("\n".join(words[:number]) + "\n")
    print(f" -> Generated dictionary written to '{out_file}'")


def random_word(length=40):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_queries(words, hits, misses, out_file):
    print(f":: Generating {hits + misses} queries")
    if os.path.exists(out_file):
        print(f" WARN: Overwriting existing '{out_file}'")

    print(f" -> Computing {hits} query hits")
    choices = [*words]
    random.shuffle(choices)
    with open(out_file, "w") as f:
        if hits > len(choices):
            print(f"WARN: Requested {hits} from {len(choices)} words. Some words will be repeated.")

        while hits > 0:
            take = len(choices) if hits >= len(choices) else hits
            f.write("\n".join(choices[:take]) + "\n")
            hits -= take

    print(f" -> Computing {misses} query misses")
    with open(out_file, "a") as f:
        for i in range(misses):
            word = random_word()
            while word in words:
                word = random_word()
                pass
            f.write(word + "\n")

    print(f" -> Generated queries written to '{out_file}'")


def parse_dict(dict_in):
    print(":: Exploding dictionary")
    words = []
    with open(dict_in, "r") as d:
        for line in d:
            for i in filter(bool, line.split()):
                words.append(i)
    print(f" -> {len(words)} words in dictionary")
    return words


def print_usage():
    print(f"Usage: {sys.argv[0]} <dict_in> <dict_out> <query_out> <dict_len> <query_len> <dict_sorting> <query_hit_percent>")
    print("")
    print("  dict_in            Path to original file to generate dictionary from")
    print("  dict_out           Path to output dictionary (i.e. 'dict')")
    print("  query_out          Path to output query file (i.e. 'infile')")
    print("  dict_len           Number of items in dict_out. Use '-' for all items.")
    print("  query_len          Number of items in query_out")
    print("  dict_sorting       One of random, sorted, reverse, none")
    print("  query_hit_percent  Percentage of queries that should be hits")
    print("")
    print("WARNING: dict_out and query_out will both be overwritten if they exist!")


def parse_args():
    if len(sys.argv) != 8:
        print_usage()
        quit()

    dict_in, dict_out, query_out, dict_len, query_len, dict_sorting, query_hit_percent = sys.argv[1:]
    if not os.path.exists(dict_in):
        print("Input dictionary does not exist!")
        quit()
    if dict_len != "-" and not dict_len.isdigit():
        print("Invalid dict_len")
        quit()
    if not query_len.isdigit():
        print("Invalid query_len")
        quit()
    query_len = int(query_len)
    if not query_hit_percent.rstrip("%").isdigit():
        print("Invalid query_len")
        quit()
    query_hit_percent = int(query_hit_percent.rstrip("%"))
    if query_hit_percent < 0 or query_hit_percent > 100:
        print("query hit percent must be between 0 and 100")
        quit()

    return dict_in, dict_out, query_out, dict_len, query_len, dict_sorting, query_hit_percent


def main():
    dict_in, dict_out, query_out, dict_len, query_len, dict_sorting, query_hit_percent = parse_args()

    if dict_sorting not in ("sorted", "reverse", "random", "none"):
        print("WARN: Invalid dict_sorting. Defaulting to no sorting")

    words = parse_dict(dict_in)

    if dict_len == "-":
        dict_len = len(words)
    else:
        dict_len = int(dict_len)
        if dict_len > len(words):
            print("We cannot create new words, dictionary length must be less than actual")
            quit()

    generate_dictionary(words, dict_len, dict_out, dict_sorting)

    query_hit = round(query_len * (query_hit_percent / 100))
    generate_queries(words, query_hit, query_len - query_hit, query_out)

    print(":: All files generated!")


if __name__ == "__main__":
    main()
