# Document Storage for AWS
# March, 2024
#
# Document Storage for AWS is a freemium accelerator from Seattle Software Works, Inc.
# https://seattleworks.com 
#
# Please see README.md
#




from chalice import Blueprint, Response

from chalicelib.common import CreateDBConnection

utility_routes = Blueprint(__name__)




@utility_routes.route('/customers/v2/documentsheartbeat', methods=['GET'], content_types=['application/json'], cors=False)
# Notes
# May be used for a simple connectivity test and as a Lambda warmer.

def documentsheartbeat():

    request = utility_routes.current_request
    request_body = utility_routes.current_request.json_body

    try:
        requestContentType = request.headers['Content-Type']
        requestContentType = requestContentType.lower()
    except ValueError as e:
        requestContentType = None
    if requestContentType is None \
        or requestContentType != 'application/json':
            return Response(
                status_code=415,
                headers={'Content-Type': 'application/json'},
                body={
                    }
                )

    (dbConnection, errorMessage) = CreateDBConnection()
    if dbConnection is None \
        or errorMessage != 'OK':
        utility_routes.log.error("Could not create Database Connection.  " + errorMessage)
        return Response(
            status_code=500,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': errorMessage
                }
            )

    try:
        dbCursor = dbConnection.cursor(prepared=True)
        dbCursor.execute('select now()')
        dbResults = dbCursor.fetchall()
    except:
        None

    if dbCursor:
        dbCursor.close()

    if dbConnection:
        dbConnection.commit()
        dbConnection.close()
        dbConnection = None

    if dbResults is None \
        or dbResults == '':
        utility_routes.log.error("Unable to query database.")
        return Response(
            status_code=500,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'Unable to query database.'
                }
            )
    else:
        return Response(
            status_code=200,
            headers={'Content-Type': 'application/json'},
            body = {
                }
            )

       


@utility_routes.route('/customers/v2/documentsinspectrequest', methods=['GET'], content_types=['application/json'], cors=False)
# Notes
# May be used to inspect request

def documentsinspectrequest():
    return Response(
        status_code = 200,
        headers={'Content-Type': 'application/json'},
        body = utility_routes.current_request.to_dict()
        )




# END
