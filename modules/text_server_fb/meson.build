_module_tsf_srcs = files(run_command(GLOB, '*.cpp', check: true).stdout().split('\n'))

lib_module_tsf = library('module_text_server_fb',
    _module_tsf_srcs,
    dependencies: [godotcore_dep,
                   thorvg_dep,
                   DEP_FREETYPE,
                   DEP_MSDF]
)

DEP_MODULE_TEXT_SERVER_FB = declare_dependency(link_with: lib_module_tsf)

MODULE_DEPENDENCIES += DEP_MODULE_TEXT_SERVER_FB
MODULES_ENABLED += 'text_server_fb'
