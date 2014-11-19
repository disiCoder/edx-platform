
def format_error(id, message):
    return {"errors" : {"id" : id, "message" : message}}

ERROR_INVALID_MODULE_ID = format_error(-1, "Could not find module for module_id")
ERROR_INVALID_COURSE_ID = format_error(-2, "Could not find course for course_id")