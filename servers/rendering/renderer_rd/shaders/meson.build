subdir('effects')
subdir('environment')
subdir('forward_clustered')
subdir('forward_mobile')

# NOTE: do not use files() here
rd_shaders = run_command(GLOB, '*.glsl', check: true).stdout().split('\n')

foreach glsl_file : rd_shaders
    rd_target = custom_target(
        'rd_target_' + glsl_file,
        output: '@PLAINNAME@.gen.h',
        input: files(glsl_file),
        env: SCRIPTS_ENV,
        command: [SCRIPT_COMPAT, 'build_rd_headers', SCRIPT_GLSL_BUILDERS, '-i', '@INPUT@', '-o', '@OUTPUT@'],
        build_by_default: true
    )

    SOURCES += [rd_target]
endforeach
