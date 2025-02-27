#!/usr/bin/python3

import os, sys, importlib.util
from importlib.machinery import SourceFileLoader


def fix_path(name: str, dest: str, base: str):
    return os.path.join(os.getenv(base), dest, os.path.basename(name))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("method")
    parser.add_argument("script")
    parser.add_argument("-s", "--source-fix-path", default="")
    parser.add_argument("-t", "--target-fix-path", default="")
    parser.add_argument("-i", "--inputs", nargs="+", default=[])
    parser.add_argument("-o", "--outputs", nargs="+", default=[])
    parser.add_argument("-e", "--scons-env", nargs="+", default=[])
    parser.add_argument("-f", "--fake-stamp", default="")

    args = [x for x in sys.argv[1:] if 'python.exe' not in x.lower()]
    args = parser.parse_args(args)

    script = args.script
    if "MESON_SOURCE_ROOT" in os.environ:
        sys.path.append(os.getenv("MESON_SOURCE_ROOT"))
        script = os.path.join(os.getenv("MESON_SOURCE_ROOT"), script)

    sources = []
    if args.source_fix_path:
        for s in args.inputs:
            sources.append(fix_path(s, args.source_fix_path, "MESON_SOURCE_ROOT"))
    else:
        sources = args.inputs

    targets = []
    if args.target_fix_path:
        for t in args.outputs:
            targets.append(fix_path(t, args.target_fix_path, "MESON_BUILD_ROOT"))
    else:
        targets = args.outputs

    env = None
    if args.scons_env:
        env = dict()
    for v in args.scons_env:
        key, val = v.split("=", 1)
        if val == "true":
            val = True
        elif val == "false":
            val = False
        env[key] = val

    mymodule = SourceFileLoader("script", script).load_module()
    getattr(mymodule, args.method)(targets, sources, env)

    # HACK to make it so that the file does not get forcibly
    # regenerated on every build. The proper fix is to move
    # the defs around to there are no cyclic dependencies
    # between third party code and Godot core.
    if args.fake_stamp:
        with open(args.fake_stamp, "w") as fake_stamp:
            fake_stamp.write("#error This file should not be included, your include paths are wrong.\n")
