_module_gltf_srcs = files(run_command(GLOB, '*.cpp', check: true).stdout().split('\n'))
_module_gltf_srcs += files(run_command(GLOB, 'editor/*.cpp', check: true).stdout().split('\n'))
_module_gltf_srcs += files(run_command(GLOB, 'structures/*.cpp', check: true).stdout().split('\n'))
_module_gltf_srcs += files(run_command(GLOB, 'extensions/*.cpp', check: true).stdout().split('\n'))
_module_gltf_srcs += files(run_command(GLOB, 'extensions/physics/*.cpp', check: true).stdout().split('\n'))

lib_module_gltf = library('module_gltf', _module_gltf_srcs, dependencies: [godotcore_dep, DEP_ZLIB])

DEP_MODULE_GLTF = declare_dependency(link_with: lib_module_gltf)

MODULE_DEPENDENCIES += DEP_MODULE_GLTF
MODULES_ENABLED += 'gltf'
