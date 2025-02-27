#!/usr/bin/python3

"""Functions used to generate source files during build time

All such functions are invoked in a subprocess on Windows to prevent build flakiness.

"""
import os.path
from typing import Optional, Iterable

from platform_methods import subprocess_main


def generate_inline_code(input_lines: Iterable[str], insert_newline: bool = True):
    """Take header data and generate inline code

    :param: input_lines: values for shared inline code
    :return: str - generated inline value
    """
    output = []
    for line in input_lines:
        if line:
            output.append(",".join(str(ord(c)) for c in line))
        if insert_newline:
            output.append("%s" % ord("\n"))
    output.append("0")
    return ",".join(output)


class RDHeaderStruct:
    def __init__(self):
        self.vertex_lines = []
        self.fragment_lines = []
        self.compute_lines = []

        self.vertex_included_files = []
        self.fragment_included_files = []
        self.compute_included_files = []

        self.reading = ""
        self.line_offset = 0
        self.vertex_offset = 0
        self.fragment_offset = 0
        self.compute_offset = 0


def include_file_in_rd_header(filename, header_data, depth):
    # This code implicitly assumes it is run in the source root,
    # and that you can just open files like "thirdparty/foo/bar".
    import os
    if os.path.exists(filename):
        fs = open(filename, "r")
    else:
        fs = open(os.path.join(os.getenv("MESON_SOURCE_ROOT"), filename), "r")
    line = fs.readline()

    while line:
        index = line.find("//")
        if index != -1:
            line = line[:index]

        if line.find("#[vertex]") != -1:
            header_data.reading = "vertex"
            line = fs.readline()
            header_data.line_offset += 1
            header_data.vertex_offset = header_data.line_offset
            continue

        if line.find("#[fragment]") != -1:
            header_data.reading = "fragment"
            line = fs.readline()
            header_data.line_offset += 1
            header_data.fragment_offset = header_data.line_offset
            continue

        if line.find("#[compute]") != -1:
            header_data.reading = "compute"
            line = fs.readline()
            header_data.line_offset += 1
            header_data.compute_offset = header_data.line_offset
            continue

        while line.find("#include ") != -1:
            includeline = line.replace("#include ", "").strip()[1:-1]

            if includeline.startswith("thirdparty/"):
                included_file = os.path.relpath(includeline)

            else:
                included_file = os.path.relpath(os.path.dirname(filename) + "/" + includeline)

            if not included_file in header_data.vertex_included_files and header_data.reading == "vertex":
                header_data.vertex_included_files += [included_file]
                if include_file_in_rd_header(included_file, header_data, depth + 1) is None:
                    print("Error in file '" + filename + "': #include " + includeline + "could not be found!")
            elif not included_file in header_data.fragment_included_files and header_data.reading == "fragment":
                header_data.fragment_included_files += [included_file]
                if include_file_in_rd_header(included_file, header_data, depth + 1) is None:
                    print("Error in file '" + filename + "': #include " + includeline + "could not be found!")
            elif not included_file in header_data.compute_included_files and header_data.reading == "compute":
                header_data.compute_included_files += [included_file]
                if include_file_in_rd_header(included_file, header_data, depth + 1) is None:
                    print("Error in file '" + filename + "': #include " + includeline + "could not be found!")

            line = fs.readline()

        line = line.replace("\r", "").replace("\n", "")

        if header_data.reading == "vertex":
            header_data.vertex_lines += [line]
        if header_data.reading == "fragment":
            header_data.fragment_lines += [line]
        if header_data.reading == "compute":
            header_data.compute_lines += [line]

        line = fs.readline()
        header_data.line_offset += 1

    fs.close()

    return header_data


def build_rd_header(filename, out_file, header_data = None):
    header_data = header_data or RDHeaderStruct()
    include_file_in_rd_header(filename, header_data, 0)

    fd = open(out_file, "w")

    fd.write("/* WARNING, THIS FILE WAS GENERATED, DO NOT EDIT */\n")

    out_file_base = out_file
    out_file_base = out_file_base[out_file_base.rfind("/") + 1 :]
    out_file_base = out_file_base[out_file_base.rfind("\\") + 1 :]
    out_file_ifdef = out_file_base.replace(".", "_").upper()
    out_file_class = out_file_base.replace(".glsl.gen.h", "").title().replace("_", "").replace(".", "") + "ShaderRD"

    if header_data.compute_lines:
        body_parts = [
            "static const char _compute_code[] = {\n%s\n\t\t};" % generate_inline_code(header_data.compute_lines),
            f'setup(nullptr, nullptr, _compute_code, "{out_file_class}");',
        ]
    else:
        body_parts = [
            "static const char _vertex_code[] = {\n%s\n\t\t};" % generate_inline_code(header_data.vertex_lines),
            "static const char _fragment_code[] = {\n%s\n\t\t};" % generate_inline_code(header_data.fragment_lines),
            f'setup(_vertex_code, _fragment_code, nullptr, "{out_file_class}");',
        ]

    body_content = "\n\t\t".join(body_parts)

    # Intended curly brackets are doubled so f-string doesn't eat them up.
    shader_template = f"""/* WARNING, THIS FILE WAS GENERATED, DO NOT EDIT */
#ifndef {out_file_ifdef}_RD
#define {out_file_ifdef}_RD

#include "servers/rendering/renderer_rd/shader_rd.h"

class {out_file_class} : public ShaderRD {{

public:

	{out_file_class}() {{

		{body_content}
	}}
}};

#endif
"""

    with open(out_file, "w") as fd:
        fd.write(shader_template)


def build_rd_headers(target, source, env):
    assert len(target) == len(source)
    for i in range(len(source)):
        build_rd_header(source[i], target[i])


class RAWHeaderStruct:
    def __init__(self):
        self.code = ""


def include_file_in_raw_header(filename: str, header_data: RAWHeaderStruct, depth: int) -> None:
    fs = open(filename, "r")
    line = fs.readline()

    while line:
        while line.find("#include ") != -1:
            includeline = line.replace("#include ", "").strip()[1:-1]

            included_file = os.path.relpath(os.path.dirname(filename) + "/" + includeline)
            include_file_in_raw_header(included_file, header_data, depth + 1)

            line = fs.readline()

        header_data.code += line
        line = fs.readline()

    fs.close()


def build_raw_header(filename, out_file, header_data=None):
    header_data = header_data or RAWHeaderStruct()
    include_file_in_raw_header(filename, header_data, 0)

    fd = open(out_file, "w")

    fd.write("/* WARNING, THIS FILE WAS GENERATED, DO NOT EDIT */\n")

    out_file_base = out_file.replace(".glsl.gen.h", "_shader_glsl")
    out_file_base = out_file_base[out_file_base.rfind("/") + 1 :]
    out_file_base = out_file_base[out_file_base.rfind("\\") + 1 :]
    out_file_ifdef = out_file_base.replace(".", "_").upper()

    shader_template = f"""/* WARNING, THIS FILE WAS GENERATED, DO NOT EDIT */
#ifndef {out_file_ifdef}_RAW_H
#define {out_file_ifdef}_RAW_H

static const char {out_file_base}[] = {{
    {generate_inline_code(header_data.code, insert_newline=False)}
}};
#endif
"""

    with open(out_file, "w") as f:
        f.write(shader_template)


def build_raw_headers(target, source, env):
    assert len(target) == len(source)
    for i in range(len(source)):
        build_raw_header(str(source[i]), str(target[i]))


if __name__ == "__main__":
    subprocess_main(globals())
