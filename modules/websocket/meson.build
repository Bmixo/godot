_module_websocket_srcs = files(run_command(GLOB, '*.cpp', check: true).stdout().split('\n'))
_module_websocket_deps = [godotcore_dep, DEP_ZLIB]

DEP_MODULE_WEBSOCKET = []

if PLATFORM == 'javascript'
    DEP_MODULE_WEBSOCKET += cpp.find_library('library_godot_websocket.js', dirs: [meson.current_source_dir()])
else
    _module_websocket_deps += DEP_WSLAY
endif

lib_module_websocket = library('module_websocket',
                               _module_websocket_srcs,
                               'editor/editor_debugger_server_websocket.cpp',
                               dependencies: _module_websocket_deps)

DEP_MODULE_WEBSOCKET += declare_dependency(link_with: lib_module_websocket)

MODULE_DEPENDENCIES += DEP_MODULE_WEBSOCKET
MODULES_ENABLED += 'websocket'
