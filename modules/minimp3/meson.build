_module_minimp3_srcs = files(run_command(GLOB, '*.cpp', check: true).stdout().split('\n'))
lib_module_minimp3 = library('module_minimp3',
                             _module_minimp3_srcs,
                             dependencies: [godotcore_dep, DEP_MINIMP3])

DEP_MODULE_MINIMP3 = declare_dependency(link_with: lib_module_minimp3)

MODULE_DEPENDENCIES += DEP_MODULE_MINIMP3
MODULES_ENABLED += 'minimp3'
