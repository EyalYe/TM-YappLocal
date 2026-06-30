# app_local — the "Local" LAN-source app component.
# REQUIRES: taskmaster_core (the stable app API) + esp_http_client for the fetch +
# espressif__cjson (the registry cJSON component) for parsing. Core is local in the
# build, so it's a plain CMake REQUIRES.
# WHOLE_ARCHIVE keeps the self-registration constructors from --gc-sections.
idf_component_register(
    SRCS "app_local.c" "tasks.c"
    REQUIRES taskmaster_core esp_http_client espressif__cjson
    WHOLE_ARCHIVE
)
