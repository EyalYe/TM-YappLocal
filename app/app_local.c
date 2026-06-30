/*
 * app_local.c — the "Local" device app for TaskMaster-C3.
 *
 * Firmware half of the yapplocal source product: a self-registering app pulled
 * into a build via the manifest. Depends only on the stable core app API
 * (core ⟂ userspace).
 *
 * Step 9: renders a task list (priority + nesting) from STATIC canned tasks via
 * the core ui_list. Step 10 replaces the canned data with a real fetch over the
 * LAN contract (async_job → GET /tasks → parse into the task model).
 */
#include "app.h"
#include "input.h"
#include "ui_frame.h"
#include "tasks.h"

#include <string.h>

/* Task Manager hints: rotate scrolls, Select completes, click opens the menu. */
static const control_hints_t LOCAL_HINTS = { .rotate = "<>", .click = "MNU", .select = "DON" };

static task_view_t s_view;

/* Seed canned tasks (mirror the yapplocal stub) until the fetch lands (step 10). */
static void seed_task(int i, const char *id, const char *parent, const char *title,
                      const char *due, uint8_t prio)
{
    task_t *t = &s_view.items[i];
    memset(t, 0, sizeof(*t));
    strlcpy(t->id, id, sizeof(t->id));
    strlcpy(t->parent_id, parent, sizeof(t->parent_id));
    strlcpy(t->title, title, sizeof(t->title));
    strlcpy(t->due, due, sizeof(t->due));
    t->priority = prio;
}

static void local_init(void)
{
    task_view_init(&s_view, UI_ROWS);
    seed_task(0, "1", "",  "Water the plants",       "today",    4);
    seed_task(1, "4", "",  "Reply to the long email", "fri",      3);
    seed_task(2, "2", "",  "Read a chapter",          "tomorrow", 2);
    seed_task(3, "3", "2", "Find the bookmark",       "",         2);
    task_view_set_count(&s_view, 4);
}

static void local_on_event(uint8_t ev)
{
    switch (ev) {
    case EV_ENCODER_CW:  task_view_move(&s_view, +1); break;
    case EV_ENCODER_CCW: task_view_move(&s_view, -1); break;
    /* Select = complete, click = detail menu — wired in step 10. */
    default: break;
    }
}

static void local_render(void)
{
    lv_obj_clean(ui_frame_content());
    ui_frame_set_hints(&LOCAL_HINTS);   /* size content (leave room for the bar) FIRST */
    task_view_render(&s_view);
}

static void local_exit(void) { }

static const device_app_t local_app = {
    .name     = "Local",
    .init     = local_init,
    .on_event = local_on_event,
    .render   = local_render,
    .exit     = local_exit,
};

TASKMASTER_REGISTER_APP(local_app);
