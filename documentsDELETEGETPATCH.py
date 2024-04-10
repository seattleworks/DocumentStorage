# Document Storage for AWS
#
# Document Storage for AWS is a freemium accelerator from Seattle Software Works, Inc.
# https://seattleworks.com 
#
# Please see README.md
#



from chalice import Blueprint, Response

from chalicelib.common import CheckValidUserType, CheckValidUUId, CreateDBConnection, GetCurrentUTCDateTime, GetGlobalVariables

import sys
import boto3
import io
import os
import re

from boto3.s3.transfer import ClientError
from botocore.exceptions import ClientError

documentsDELETEGETPATCH_routes = Blueprint(__name__)

(S3BUCKETNAME, S3REGIONNAME, S3SERVERSIDEENCRYPTION) = GetGlobalVariables()




@documentsDELETEGETPATCH_routes.route('/customers/v1/documents/{documentUUId}', methods=['DELETE','GET','PATCH'], content_types=['application/json'], cors=False)
# Notes
# 

# Dev Notes
# Authentication.
# Get.  Should it ask for download path and append that with documentName?

def documentsDELETEGETPATCH(documentUUId):
    request = documentsDELETEGETPATCH_routes.current_request
    request_body = documentsDELETEGETPATCH_routes.current_request.json_body

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

    if documentUUId is not None:
        documentUUId = documentUUId.strip()
        documentUUId = documentUUId.lower()
    if documentUUId is None \
        or documentUUId == '' \
        or not CheckValidUUId(documentUUId):
        return Response(
            status_code=400,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'Bad Parameter.  Missing or invalid documentUUId.',
                'documentUUId': documentUUId
                }
            )  




    elif request.method == 'DELETE':

        (dbConnection, errorMessage) = CreateDBConnection()
        if dbConnection is None \
            or errorMessage != 'OK':
                documentsDELETEGETPATCH_routes.log.error('Could not create Database Connection.  ' + errorMessage)
                return Response(
                    status_code=500,
                    headers={'Content-Type': 'application/json'},
                    body = {
                        'message': 'Could not create Database Connection.  ' + errorMessage
                        }
                    )

        try:
            sqlStatement = 'select ' \
                + 'documentInternalName ' \
                + ', legalHold ' \
                + 'from tdocument where documentUUId = ? '
            sqlArguments = (documentUUId,)
            dbCursor = dbConnection.cursor(prepared=True)
            dbCursor.execute(sqlStatement, sqlArguments)
            dbResults = dbCursor.fetchall()
            dbConnection.commit()
            documentInternalName = None
            if dbCursor.rowcount is not None \
                and dbCursor.rowcount == 1:
                    for row in dbResults:
                        documentInternalName = row[0].decode('utf-8')
                        legalHold = row[1].decode('utf-8')
            if documentInternalName is None \
                or documentInternalName == '':
                    # 404 Not Found
                    return Response(
                        status_code=404,
                        headers={'Content-Type': 'application/json'},
                        body = {
                            }
                        )
            elif legalHold is not None \
                and legalHold == 'Y':
                    # 403 Forbidden
                    return Response(
                        status_code=403,
                        headers={'Content-Type': 'application/json'},
                        body = {
                            'message': 'Delete not permitted since Document has a Legal Hold.',
                            'documentUUId': documentUUId
                            }
                        )
        except Exception as e:
            dbConnection.commit()
            documentsDELETEGETPATCH_routes.log.error('SELECT on tdocument failed due to {}'.format(e))
            return Response(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'SELECT on tdocument failed due to {}'.format(e),
                    'documentUUId': documentUUId
                    }
                )

        try:
            s3Client = boto3.client('s3',region_name=S3REGIONNAME)
            s3Client.delete_object(
                Bucket = S3BUCKETNAME
                , Key = documentInternalName
            )
            s3Client = None
            sqlArguments = (documentUUId,)
            sqlStatement = 'delete from tdocument_auditlog where documentUUId = ? '
            dbCursor = dbConnection.cursor(prepared=True)
            dbCursor.execute(sqlStatement, sqlArguments)
            dbConnection.commit()
            sqlStatement = 'delete from tdocument where documentUUId = ? '
            dbCursor = dbConnection.cursor(prepared=True)
            dbCursor.execute(sqlStatement, sqlArguments)
            dbConnection.commit()
        except Exception as e:
            dbConnection.rollback()
            documentsDELETEGETPATCH_routes.log.error('Delete failed due to {}'.format(e))
            return Response(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Delete failed due to {}'.format(e),
                    'documentUUId': documentUUId
                    }
                )

        # Successful DELETE
        # 204 No Content
        return Response(
            status_code=204,
            headers={'Content-Type': 'application/json'},
            body = {
                }
            )




    elif request.method == 'GET':

        currentUTCDateTime = GetCurrentUTCDateTime()
        if currentUTCDateTime is None:
            return Response(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Could not generate a current UTC DateTime'
                    }
                )

        try:
            userId = request_body['userId']
            userId = userId.strip()
        except:
            userId = None
        if userId == '':
            userId = None
        elif userId is not None \
            and len(userId) > 255:
                return Response(
                    status_code=400,
                    headers={'Content-Type': 'application/json'},
                    body = {
                        'message': 'Bad Parameter.  userId is too large for database column.',
                        'userId': userId
                        }
                    )

        try:
            userType = request_body['userType']
            userType = userType.strip()
            userType = userType.upper()
        except:
            userType = None
        if userType == '':
            userType = None
        elif not CheckValidUserType(userType):
                return Response(
                    status_code=400,
                    headers={'Content-Type': 'application/json'},
                    body = {
                        'message': 'Bad Parameter.  userType must be CUSTOMER, EMPLOYEE, MIGRATION, or SYSTEM.',
                        'userType': userType
                        }
                    )

        if userId is not None \
            and userType is None:
                return Response(
                    status_code=400,
                    headers={'Content-Type': 'application/json'},
                    body = {
                        'message': 'Missing Parameter.  Must provide userType if providing a userId.',
                        'userId': userId,
                        'userType': userType
                        }
                    )        

        (dbConnection, errorMessage) = CreateDBConnection()
        if dbConnection is None \
            or errorMessage != 'OK':
                documentsDELETEGETPATCH_routes.log.error('Could not create Database Connection.  ' + errorMessage)
                return Response(
                    status_code=500,
                    headers={'Content-Type': 'application/json'},
                    body = {
                        'message': 'Could not create Database Connection.  ' + errorMessage
                        }
                    )

        try:
            sqlStatement = 'select ' \
                + 'documentInternalName ' \
                + ', documentName ' \
                + 'from tdocument where documentUUId = ? '
            sqlArguments = (documentUUId,)
            dbCursor = dbConnection.cursor(prepared=True)
            dbCursor.execute(sqlStatement, sqlArguments)
            dbResults = dbCursor.fetchall()
            dbConnection.commit()
            documentInternalName = None
            if dbCursor.rowcount is not None \
                and dbCursor.rowcount == 1:
                    for row in dbResults:
                        documentInternalName = row[0].decode('utf-8')
                        documentName = row[1].decode('utf-8')
            if documentInternalName is None \
                or documentInternalName == '' \
                or documentName is None \
                or documentName == '':
                    # 404 Not Found
                    return Response(
                        status_code=404,
                        headers={'Content-Type': 'application/json'},
                        body = {
                            }
                        )

            sqlStatement = 'insert into tdocument_auditlog ' \
                + '( documentUUId ' \
                + ', createdUTCDateTime ' \
                + ', accessType ' \
                + ', userId ' \
                + ', userType ' \
                + ') ' \
                + 'values ' \
                + '( %s ' \
                + ', %s ' \
                + ', %s ' \
                + ', ifnull(null, %s) ' \
                + ', ifnull(null, %s) ' \
                + ')'
            sqlArguments = \
                documentUUId \
                , currentUTCDateTime \
                , 'GET' \
                , userId \
                , userType
            dbCursor = dbConnection.cursor(prepared=True)
            dbCursor.execute(sqlStatement,sqlArguments)
            dbConnection.commit()

            sqlStatement = 'update tdocument ' \
                + 'set accessedCount = accessedCount + 1 ' \
                + ', lastAccessedUTCDateTime = ? ' \
                + 'where documentUUId = ? '
            sqlArguments = (currentUTCDateTime, documentUUId)
            dbCursor = dbConnection.cursor(prepared=True)
            dbCursor.execute(sqlStatement, sqlArguments)
            dbConnection.commit()

            s3Client = boto3.client('s3',region_name=S3REGIONNAME)
            with open(documentName, 'wb') as data:
                s3Client.download_fileobj(
                    S3BUCKETNAME
                    , documentInternalName
                    , data
                    )

        except Exception as e:
            dbConnection.commit()
            documentsDELETEGETPATCH_routes.log.error('Get failed due to {}'.format(e))
            return Response(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Get failed due to {}'.format(e),
                    'documentUUId': documentUUId
                    }
                )

        # Successful GET
        # 200 OK
        return Response(
            status_code=200,
            headers={'Content-Type': 'application/json'},
            body = {
                }
            )




    elif request.method == 'PATCH':

        currentUTCDateTime = GetCurrentUTCDateTime()
        if currentUTCDateTime is None:
            return Response(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Could not generate a current UTC DateTime'
                    }
                )

        try:
            legalHold = request_body['legalHold']
            legalHold = legalHold.strip()
            legalHold = legalHold.upper()
        except:
            legalHold = None
        if legalHold is None \
            or (legalHold != 'N' \
            and legalHold != 'Y'):
                return Response(
                    status_code=400,
                    headers={'Content-Type': 'application/json'},
                    body = {
                        'message': 'Bad Parameter.  legalHold must be N or Y.',
                        'legalHold': legalHold
                        }
                    )

        try:
            userId = request_body['userId']
            userId = userId.strip()
        except:
            userId = None
        if userId == '':
            userId = None
        elif userId is not None \
            and len(userId) > 255:
                return Response(
                    status_code=400,
                    headers={'Content-Type': 'application/json'},
                    body = {
                        'message': 'Bad Parameter.  userId is too large for database column.',
                        'userId': userId
                        }
                    )

        try:
            userType = request_body['userType']
            userType = userType.strip()
            userType = userType.upper()
        except:
            userType = None
        if userType == '':
            userType = None
        elif not CheckValidUserType(userType):
                return Response(
                    status_code=400,
                    headers={'Content-Type': 'application/json'},
                    body = {
                        'message': 'Bad Parameter.  userType must be CUSTOMER, EMPLOYEE, MIGRATION, or SYSTEM.',
                        'userType': userType
                        }
                    )

        if userId is not None \
            and userType is None:
                return Response(
                    status_code=400,
                    headers={'Content-Type': 'application/json'},
                    body = {
                        'message': 'Missing Parameter.  Must provide userType if providing a userId.',
                        'userId': userId,
                        'userType': userType
                        }
                    )        

        (dbConnection, errorMessage) = CreateDBConnection()
        if dbConnection is None \
            or errorMessage != 'OK':
                documentsDELETEGETPATCH_routes.log.error('Could not create Database Connection.  ' + errorMessage)
                return Response(
                    status_code=500,
                    headers={'Content-Type': 'application/json'},
                    body = {
                        'message': 'Could not create Database Connection.  ' + errorMessage
                        }
                    )

        try:
            sqlStatement = 'select ' \
                + 'documentInternalName ' \
                + 'from tdocument where documentUUId = ? '
            sqlArguments = (documentUUId,)
            dbCursor = dbConnection.cursor(prepared=True)
            dbCursor.execute(sqlStatement, sqlArguments)
            dbResults = dbCursor.fetchall()
            dbConnection.commit()
            documentInternalName = None
            if dbCursor.rowcount is not None \
                and dbCursor.rowcount == 1:
                    for row in dbResults:
                        documentInternalName = row[0].decode('utf-8')
            if documentInternalName is None \
                or documentInternalName == '':
                    # 404 Not Found
                    return Response(
                        status_code=404,
                        headers={'Content-Type': 'application/json'},
                        body = {
                            }
                        )

            sqlStatement = 'update tdocument ' \
                + 'set legalHold = ? ' \
                + ', updatedUTCDateTime = ? ' \
                + 'where documentUUId = ? '
            sqlArguments = (legalHold, currentUTCDateTime, documentUUId)
            dbCursor = dbConnection.cursor(prepared=True)
            dbCursor.execute(sqlStatement, sqlArguments)
            dbConnection.commit()

            if legalHold is not None \
                and legalHold == 'Y':
                    s3LegalHoldStatus = 'ON'
            else:
                s3LegalHoldStatus = 'OFF'
            s3Client = boto3.client('s3',region_name=S3REGIONNAME)
            s3Client.put_object_legal_hold(
                Bucket = S3BUCKETNAME
                , Key = documentInternalName
                , LegalHold =
                {
                    'Status': s3LegalHoldStatus,
                }
                )
            s3Client = None

            sqlStatement = 'insert into tdocument_auditlog ' \
                + '( documentUUId ' \
                + ', createdUTCDateTime ' \
                + ', accessType ' \
                + ', userId ' \
                + ', userType ' \
                + ') ' \
                + 'values ' \
                + '( %s ' \
                + ', %s ' \
                + ', %s ' \
                + ', ifnull(null, %s) ' \
                + ', ifnull(null, %s) ' \
                + ')'
            sqlArguments = \
                documentUUId \
                , currentUTCDateTime \
                , 'PATCH' \
                , userId \
                , userType
            dbCursor = dbConnection.cursor(prepared=True)
            dbCursor.execute(sqlStatement,sqlArguments)
            dbConnection.commit()

        except Exception as e:
            dbConnection.commit()
            documentsDELETEGETPATCH_routes.log.error('Update failed due to {}'.format(e))
            return Response(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Update failed due to {}'.format(e),
                    'documentUUId': documentUUId
                    }
                )

        # Successful PATCH
        # 204 No Content
        return Response(
            status_code=204,
            headers={'Content-Type': 'application/json'},
            body = {
                }
            )




    else:
        # 405 Method Not Allowed
        return Response(
            status_code=405,
            headers={'Content-Type': 'application/json'},
            body = {
                }
            )




# END
