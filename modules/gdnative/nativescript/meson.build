module_gdnative_srcs += files(run_command(GLOB, '*.cpp', check: true).stdout().split('\n'))

if PLATFORM == 'linuxbsd' or PLATFORM == 'ios'
    module_gdnative_link_args += ['-rdynamic']
endif
