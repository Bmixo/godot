# The libraries and defines added in this file are the *requirements* that are
# needed to build on the selected platform. Do not add debug/release/optional
# compilation flags here.

################################################################################
# Commands to always run
################################################################################
_target_uwp_logo = custom_target(
    'uwp_logo',
    output: ['logo_svg.gen.h'],
    input: ['logo.svg'],
    command: [SCRIPT_PLATFORM_LOGO, '@INPUT@', '@OUTPUT@', 'uwp'],
    build_by_default: true
)
SOURCES += [_target_uwp_logo]


################################################################################
# Host Machine Specifics
################################################################################
if PLATFORM == 'uwp'
    error('uwp not implemented yet')
endif
