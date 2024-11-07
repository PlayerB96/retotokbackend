def build_response(message, data, status):
    response_data = {
        "message": message,
        "data": data,
        "status": status,
    }
    return response_data
