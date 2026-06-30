# app_local — a self-registering TaskMaster app component.
#
# REQUIRES taskmaster_core: the app depends on the core's stable app API. Core is
# always present in the firmware build (it's the TaskMaster project's own
# component), so this is a plain REQUIRES — no git fetch of core needed here.
#
# WHOLE_ARCHIVE: nothing in core references this component by name (it
# self-registers via a constructor, TASKMASTER_REGISTER_APP), so without
# WHOLE_ARCHIVE the linker's --gc-sections would drop the constructor.
idf_component_register(
    SRCS "app_local.c"
    REQUIRES taskmaster_core
    WHOLE_ARCHIVE
)
