module_gdnative_srcs = files(run_command(GLOB, '*.cpp', check: true).stdout().split('\n'))

# XXX Could use compat, but module will be removed, so no need to spend time on it.
SCRIPT_GDNATIVE_API_GEN = find_program('scripts/gdnative_api_struct_gen.py')

# generated api structs
_gdnative_api_structs_source_target = custom_target(
    'gndative_api_structs_source',
    input: ['gdnative_api.json'],
    output: [ 'gdnative_api_struct.gen.cpp'],
    command: [SCRIPT_GDNATIVE_API_GEN, '@INPUT@', 'gen_source', '@OUTPUT@'],
    build_by_default: true
)
module_gdnative_srcs += [_gdnative_api_structs_source_target]

# generate the header file here...
subdir('include')

module_gdnative_link_args = []
module_gdnative_cpp_args = []

subdir('android')
subdir('gdnative')
subdir('nativescript')
#subdir('net')
subdir('pluginscript')
subdir('videodecoder')
#subdir('xr')
#subdir('text')

_module_gdnative_incdirs = include_directories('include')

lib_module_gdnative = library('module_gdnative',
    module_gdnative_srcs,
    link_args: module_gdnative_link_args,
    cpp_args: module_gdnative_cpp_args,
    include_directories: _module_gdnative_incdirs,
    dependencies: [DEP_GODOT_ALL]
)

DEP_MODULE_GDNATIVE = declare_dependency(link_with: lib_module_gdnative,
                                         sources: _gdnative_api_structs_header_target,
                                         include_directories: _module_gdnative_incdirs)

MODULE_DEPENDENCIES += DEP_MODULE_GDNATIVE
MODULES_ENABLED += 'gdnative'
