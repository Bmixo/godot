subdir('fsr2')

effect_shaders = run_command(GLOB, '*.glsl', check: true).stdout().split('\n')

foreach glsl_file : effect_shaders
   shad_target = custom_target(
        'effect_target_' + glsl_file,
        output: '@PLAINNAME@.gen.h',
        input: files(glsl_file),
        env: SCRIPTS_ENV,
        command: [SCRIPT_COMPAT, 'build_rd_headers', SCRIPT_GLSL_BUILDERS, '-i', '@INPUT@', '-o', '@OUTPUT@'],
        build_by_default: true
    )

    SHADER_HEADERS += [shad_target]
    SOURCES += [shad_target]
endforeach
