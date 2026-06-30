# app_local — the "Local" LAN-source app component.
# REQUIRES: taskmaster_core + esp_http_client + espressif__cjson (fetch/parse).
# tasks.h is header-only (static fns) so the two source apps don't collide.
idf_component_register(
    SRCS "app_local.c"
    REQUIRES taskmaster_core esp_http_client espressif__cjson
    WHOLE_ARCHIVE
)
