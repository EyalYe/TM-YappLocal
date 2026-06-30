/*
 * app_local.c — the "Local" device app for TaskMaster-C3.
 *
 * This is the firmware half of the yapplocal source product: a self-registering
 * app component that the device pulls into a build via the manifest (a git: line
 * in the firmware's main/idf_component.yml). It depends ONLY on the stable core
 * app API (taskmaster_core) — never the other way round (core ⟂ userspace).
 *
 * Placeholder for now: it registers and renders a stub screen. The Task Manager
 * logic (source_client over the device contract → this app's server) + its
 * declared config (server URL, via TASKMASTER_REGISTER_APP_CONFIG) land at
 * Phase 3 steps 6.5/11. It already proves the manifest pulls a remote app repo
 * into the build and self-registers in the Launcher.
 */
#include "app.h"
#include "ui_frame.h"

#define LOCAL_ROW_TITLE 0
#define LOCAL_ROW_NOTE1 1
#define LOCAL_ROW_NOTE2 2

static void local_init(void)            { }
static void local_on_event(uint8_t ev) { (void)ev; }

static void local_render(void)
{
    lv_obj_clean(ui_frame_content());
    ui_frame_set_hints(NULL);                 /* full width for now */
    ui_text_row(LOCAL_ROW_TITLE, "Local source");
    ui_text_row(LOCAL_ROW_NOTE1, "task manager");
    ui_text_row(LOCAL_ROW_NOTE2, "coming soon");
}

static void local_exit(void)            { }

static const device_app_t local_app = {
    .name     = "Local",
    .init     = local_init,
    .on_event = local_on_event,
    .render   = local_render,
    .exit     = local_exit,
};

TASKMASTER_REGISTER_APP(local_app);
