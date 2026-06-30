# app_local — a self-registering TaskMaster app component (Local LAN source).
# REQUIRES taskmaster_core (the stable app API; core is local in the build).
# WHOLE_ARCHIVE keeps the self-registration constructor from --gc-sections.
idf_component_register(
    SRCS "app_local.c" "tasks.c"
    REQUIRES taskmaster_core
    WHOLE_ARCHIVE
)
