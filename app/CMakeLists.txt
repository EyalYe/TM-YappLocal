# app_local — the "Local" LAN-source app component.
# REQUIRES: taskmaster_core (the stable app API) + esp_http_client/json for the
# fetch. Core is local in the build, so it's a plain CMake REQUIRES.
# WHOLE_ARCHIVE keeps the self-registration constructors from --gc-sections.
idf_component_register(
    SRCS "app_local.c" "tasks.c"
    REQUIRES taskmaster_core esp_http_client json
    WHOLE_ARCHIVE
)
