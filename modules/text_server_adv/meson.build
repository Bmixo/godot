module_tsa_srcs = files(run_command(GLOB, '*.cpp', check: true).stdout().split('\n'))

subdir('icu_data')

tsa_args = []
if get_option('tools')
    tsa_args += '-DICU_STATIC_DATA'
endif

lib_module_tsa = library('module_text_server_adv', module_tsa_srcs,
    dependencies: [godotcore_dep,
                   thorvg_dep,
                   DEP_HARFBUZZ,
                   DEP_ICU,
                   DEP_FREETYPE,
                   DEP_GRAPHITE,
                   DEP_MSDF],
    cpp_args: tsa_args
)

DEP_MODULE_TEXT_SERVER_ADV = declare_dependency(link_with: lib_module_tsa)

MODULE_DEPENDENCIES += DEP_MODULE_TEXT_SERVER_ADV
MODULES_ENABLED += 'text_server_adv'
