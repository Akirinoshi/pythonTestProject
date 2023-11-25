import os
import traceback
import logging
from http import HTTPStatus

from logging.handlers import RotatingFileHandler
from config import Config


def init_logging(app):
    # define custom error handler
    set_custom_handlers(app)

    if app.config['DEBUG'] == 1:
        # log the error to a file
        handler = RotatingFileHandler('logs.log', maxBytes=10000, backupCount=1)
    else:
        # log the error to the stdout
        handler = logging.StreamHandler()

    handler.setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG, handlers=[handler])
    print('Logging run...')


def set_custom_handlers(app):
    # define custom error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        exception(e)
        return 'Something went wrong', 500

    @app.errorhandler(403)
    def handle_forbidden(e):
        return {'success': False, 'error': 'Forbidden'}, HTTPStatus.FORBIDDEN

    @app.errorhandler(404)
    def handle_not_found(e):
        return "Not found", 404

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return "Method not allowed", 405

    @app.errorhandler(400)
    def handle_method_not_allowed(e):
        return "Bad request", 400


def info(message: str):
    prefix = 'INFO: '
    logging.info(prefix + message)


def debug(message: str):
    prefix = 'DEBUG: '
    logging.debug(prefix + message)
    print('>>>>> DEBUG: ', message)


def warning(message: str):
    logging.warning(message)


def error(message: str):
    logging.error(message)


def exception(e: Exception):
    logging.exception(e)
    message = presentation_error(e)


def presentation_error(e: Exception) -> str:
    tb = traceback.extract_tb(e.__traceback__)
    if len(tb) > 0:
        file_name, line_number, function_name, code_line = tb[-1]
        traceback_str = "".join(traceback.format_list(tb))
    else:
        file_name, line_number, function_name, code_line, traceback_str = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
    error_message = (
        f"<b>Error msg:</b> {str(e)}\n"
        f"<b>Type:</b> {type(e).__name__}\n"
        f"<b>Args:</b> {', '.join(map(str, e.args)) if e.args else 'N/A'}\n"
        f"<b>Line number:</b> {line_number}\n"
        f"<b>Function name:</b> {function_name}\n"
        f"<b>Code line:</b> {code_line}\n"
        f"<b>Traceback:</b>\n{traceback_str}\n"
        f"<b>File name:</b> {file_name}\n"
        f"<b>ENV:</b> {Config.ENV}\n"
    )
    return f"\u2757\ufe0f \u2757\ufe0f \u2757\ufe0f \n{error_message}"
