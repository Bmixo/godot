if get_option('tools')
    _module_tsa_icu_data_name = DEP_ICU.get_variable(internal: 'icu_data_name')
    _module_tsa_icu_file = files('../../../thirdparty/icu4c' / _module_tsa_icu_data_name)

    _script_icu_data_gen = find_program('../scripts/icu_data.py')
    _icu_data_gen_target = custom_target(
        'icu_data_gen',
        output: ['icudata.gen.h'],
        input: [_module_tsa_icu_file],
        command: [_script_icu_data_gen, '@INPUT@', '@OUTPUT@'],
        env: SCRIPTS_ENV,
        build_by_default: true
    )
    module_tsa_srcs += [_icu_data_gen_target]
else
    module_tsa_srcs += files('icudata_stub.cpp')
endif
