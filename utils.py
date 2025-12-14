from flask import request, jsonify, make_response
from dicttoxml import dicttoxml

def format_response(data, status_code=200):
    """
    Returns data in JSON or XML format based on URL parameter.
    
    Args:
        data: Dictionary with response data
        status_code: HTTP status code
    
    Returns:
        Flask response in JSON or XML format
    """
    output_format = request.args.get('format', 'json').lower()
    
    if output_format == 'xml':
        xml_data = dicttoxml(data, custom_root='response', attr_type=False)
        response = make_response(xml_data)
        response.headers['Content-Type'] = 'application/xml'
        return response, status_code
    else:
        return jsonify(data), status_code