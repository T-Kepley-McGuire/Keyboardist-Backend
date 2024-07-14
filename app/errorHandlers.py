from flask import jsonify

def handleBadRequest(error):
    response = jsonify({
        'error': 'Bad Request',
        'message': error.description if error.description else 'The request could not be understood by the server due to malformed syntax.'
    })
    response.status_code = 400
    return response

def handleNotFoundError(error):
    response = jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found on this server.'
    })
    response.status_code = 404
    return response

def handleInternalServerError(error):
    response = jsonify({
        'error': 'Internal Server Error',
        'message': 'The server encountered an internal error and was unable to complete your request.'
    })
    response.status_code = 500
    return response



def registerErrorHandlers(app):
    app.register_error_handler(400, handleBadRequest)
    app.register_error_handler(404, handleNotFoundError)
    app.register_error_handler(500, handleInternalServerError)
