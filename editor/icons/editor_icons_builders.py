#!/usr/bin/python3

"""Functions used to generate source files during build time

All such functions are invoked in a subprocess on Windows to prevent build flakiness.

"""

import os, sys
from io import StringIO
from glob import glob

def replace_if_different(output_path_str, new_content_path_str):
    import pathlib

    output_path = pathlib.Path(output_path_str)
    new_content_path = pathlib.Path(new_content_path_str)
    if not output_path.exists():
        new_content_path.replace(output_path)
        return
    if output_path.read_bytes() == new_content_path.read_bytes():
        new_content_path.unlink()
    else:
        new_content_path.replace(output_path)


# See also `scene/resources/default_theme/default_theme_icons_builders.py`.
def make_editor_icons(dst, sourcedir):

    tmpfilename = dst + '~'
    svg_icons = glob(os.path.join(sourcedir, '*.svg'))
    svg_icons.sort()

    icons_string = StringIO()

    for f in svg_icons:
        fname = str(f)

        icons_string.write('\t"')

        with open(fname, "rb") as svgf:
            b = svgf.read(1)
            while len(b) == 1:
                icons_string.write("\\" + str(hex(ord(b)))[1:])
                b = svgf.read(1)

        icons_string.write('"')
        if fname != svg_icons[-1]:
            icons_string.write(",")
        icons_string.write("\n")

    s = open(tmpfilename, "w")
    s.write("/* THIS FILE IS GENERATED DO NOT EDIT */\n")
    s.write("#ifndef _EDITOR_ICONS_H\n")
    s.write("#define _EDITOR_ICONS_H\n")
    s.write("static const int editor_icons_count = {};\n".format(len(svg_icons)))
    s.write("static const char *editor_icons_sources[] = {\n")
    s.write(icons_string.getvalue())
    s.write("};\n\n")
    s.write("static const char *editor_icons_names[] = {\n")

    # this is used to store the indices of thumbnail icons
    thumb_medium_indices = []
    thumb_big_indices = []
    index = 0
    for f in svg_icons:
        fname = str(f)

        # Trim the `.svg` extension from the string.
        icon_name = os.path.basename(fname)[:-4]
        # some special cases
        if icon_name.endswith("MediumThumb"):  # don't know a better way to handle this
            thumb_medium_indices.append(str(index))
        if icon_name.endswith("BigThumb"):  # don't know a better way to handle this
            thumb_big_indices.append(str(index))
        if icon_name.endswith("GodotFile"):  # don't know a better way to handle this
            thumb_big_indices.append(str(index))

        s.write('\t"{0}"'.format(icon_name))

        if fname != svg_icons[-1]:
            s.write(",")
        s.write("\n")

        index += 1

    s.write("};\n")

    if thumb_medium_indices:
        s.write("\n\n")
        s.write("static const int editor_md_thumbs_count = {};\n".format(len(thumb_medium_indices)))
        s.write("static const int editor_md_thumbs_indices[] = {")
        s.write(", ".join(thumb_medium_indices))
        s.write("};\n")
    if thumb_big_indices:
        s.write("\n\n")
        s.write("static const int editor_bg_thumbs_count = {};\n".format(len(thumb_big_indices)))
        s.write("static const int editor_bg_thumbs_indices[] = {")
        s.write(", ".join(thumb_big_indices))
        s.write("};\n")

    s.write("#endif\n")

    s.close()
    icons_string.close()
    replace_if_different(dst, tmpfilename)



if __name__ == "__main__":
    make_editor_icons(sys.argv[1], sys.argv[2])

