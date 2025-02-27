#!/usr/bin/python3

import argparse
import os


def fix_path(name: str, dest: str):
    return os.path.join(os.getenv("MESON_BUILD_ROOT"), dest, os.path.basename(name))


def _make_icu_data(input_data_file: str, output_gen_file: str):
    import os

    f = output_gen_file
    g = open(f, "w", encoding="utf-8")

    g.write("/* THIS FILE IS GENERATED DO NOT EDIT */\n")
    g.write("/* (C) 2016 and later: Unicode, Inc. and others. */\n")
    g.write("/* License & terms of use: https://www.unicode.org/copyright.html */\n")
    g.write("#ifndef _ICU_DATA_H\n")
    g.write("#define _ICU_DATA_H\n")
    g.write('#include "unicode/utypes.h"\n')
    g.write('#include "unicode/udata.h"\n')
    g.write('#include "unicode/uversion.h"\n')

    f = open(input_data_file, "rb")
    buf = f.read()
    import os.path

    g.write('extern "C" U_EXPORT const size_t U_ICUDATA_SIZE = ' + str(len(buf)) + ";\n")
    g.write('extern "C" U_EXPORT const unsigned char U_ICUDATA_ENTRY_POINT[] = {\n')
    for i in range(len(buf)):
        g.write("\t" + str(buf[i]) + ",\n")

    g.write("};\n")
    g.write("#endif")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the icu data header.")
    parser.add_argument("input_data_file", type=str)
    parser.add_argument("output_gen_file", type=str)

    args = parser.parse_args()
    _make_icu_data(args.input_data_file, args.output_gen_file)
