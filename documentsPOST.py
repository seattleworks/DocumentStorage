# Document Storage for AWS
#
# Document Storage for AWS is a freemium accelerator from Seattle Software Works, Inc.
# https://seattleworks.com 
#
# Please see README.md
#



from chalice import Blueprint, Response

from chalicelib.common import CheckDateEarlier, CheckValidAmount, CheckValidDate, CheckValidUserType, CreateDBConnection, CreateUUId, GetCurrentUTCDateTime, GetGlobalVariables

import sys
import boto3
import datetime
import io
import os
import re

from boto3.s3.transfer import S3UploadFailedError
from botocore.exceptions import ClientError

documentsPOST_routes = Blueprint(__name__)

(S3BUCKETNAME, S3REGIONNAME, S3SERVERSIDEENCRYPTION) = GetGlobalVariables()




@documentsPOST_routes.route('/customers/v1/documents', methods=['POST'], content_types=['application/json'], cors=False)
# Notes
# - createdUTCDateTime and updatedUTCDateTime are set to same value for a new Document.
# - Documents are placed in subfolders in the S3 Bucket.
# - Metadata identifier of the documentUUId is added to each Document in S3.
# - Expiration Date is added to each Document in S3.
# - Tags are added to each Document in S3 for potential analysis and allocation of S3 costs.
# - If legalHold = Y, a Legal Hold will be placed on the Document in S3.
# - Any rollback due to a failure may involve two different database tables and the Document.

# Dev Notes
# Authentication.
# Able to handle more than one document on a POST
# should document updated date be set to origination date if it doesn't exist?
# test document creation with each permissible s3StorageClass value (4)
# discussion of server-side encryption here for files in S3 bucket
#      https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object 

def documentsPOST():
    request = documentsPOST_routes.current_request
    request_body = documentsPOST_routes.current_request.json_body

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

    documentUUId = CreateUUId()
    if documentUUId is None:
        documentsPOST_routes.log.error("Could not generate a new documentUUId.")
        return Response(
            status_code=500,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'Could not generate a new documentUUId.'
                }
            )

    currentUTCDateTime = GetCurrentUTCDateTime()
    if currentUTCDateTime is None:
        documentsPOST_routes.log.error("Could not generate the current UTC DateTime.")
        return Response(
            status_code=500,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'Could not generate the current UTC DateTime.'
                }
            )

    try:
        agreementId = request_body['agreementId']
        agreementId = agreementId.strip()
    except:
        agreementId = None
    if agreementId == '':
        agreementId = None
    elif agreementId is not None \
        and len(agreementId) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  agreementId is too large for database column.',
                    'agreementId': agreementId
                    }
                )

    try:
        businessArea = request_body['businessArea']
        businessArea = businessArea.strip()
    except:
        businessArea = None
    if businessArea == '':
        businessArea = None
    elif businessArea is not None \
        and len(businessArea) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  businessArea is too large for database column.',
                    'businessArea': businessArea
                    }
                )

    try:
        containsSensitiveData = request_body['containsSensitiveData']
        containsSensitiveData = containsSensitiveData.strip()
        containsSensitiveData = containsSensitiveData.upper()
    except:
        containsSensitiveData = None
    if containsSensitiveData is None \
        or (containsSensitiveData != 'N' \
        and containsSensitiveData != 'Y'):
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  containsSensitiveData must be N or Y.',
                    'containsSensitiveData': containsSensitiveData
                    }
                )

    try:
        customerCompanyName = request_body['customerCompanyName']
        customerCompanyName = customerCompanyName.strip()
    except:
        customerCompanyName = None
    if customerCompanyName == '':
        customerCompanyName = None
    elif customerCompanyName is not None \
        and len(customerCompanyName) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  customerCompanyName is too large for database column.',
                    'customerCompanyName': customerCompanyName
                    }
                )

    try:
        customerFirstName = request_body['customerFirstName']
        customerFirstName = customerFirstName.strip()
    except:
        customerFirstName = None
    if customerFirstName == '':
        customerFirstName = None
    elif customerFirstName is not None \
        and len(customerFirstName) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  customerFirstName is too large for database column.',
                    'customerFirstName': customerFirstName
                    }
                )

    try:
        customerId1 = request_body['customerId1']
        customerId1 = customerId1.strip()
    except:
        customerId1 = None
    if customerId1 == '':
        customerId1 = None
    elif customerId1 is not None \
        and len(customerId1) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  customerId1 is too large for database column.',
                    'customerId1': customerId1
                    }
                )

    try:
        customerId2 = request_body['customerId2']
        customerId2 = customerId2.strip()
    except:
        customerId2 = None
    if customerId2 == '':
        customerId2 = None
    elif customerId2 is not None \
        and len(customerId2) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  customerId2 is too large for database column.',
                    'customerId2': customerId2
                    }
                )

    try:
        customerId3 = request_body['customerId3']
        customerId3 = customerId3.strip()
    except:
        customerId3 = None
    if customerId3 == '':
        customerId3 = None
    elif customerId3 is not None \
        and len(customerId3) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  customerId3 is too large for database column.',
                    'customerId3': customerId3
                    }
                )

    try:
        customerLastName = request_body['customerLastName']
        customerLastName = customerLastName.strip()
    except:
        customerLastName = None
    if customerLastName == '':
        customerLastName = None
    elif customerLastName is not None \
        and len(customerLastName) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  customerLastName is too large for database column.',
                    'customerLastName': customerLastName
                    }
                )

    try:
        customerType = request_body['customerType']
        customerType = customerType.strip()
    except:
        customerType = None
    if customerType == '':
        customerType = None
    elif customerType is not None \
        and len(customerType) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  customerType is too large for database column.',
                    'customerType': customerType
                    }
                )

    try:
        descriptionText = request_body['descriptionText']
        descriptionText = descriptionText.strip()
    except:
        descriptionText = None
    if descriptionText == '':
        descriptionText = None
    elif descriptionText is not None \
        and len(descriptionText) > 2000:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  descriptionText is too large for database column.',
                    'descriptionText': descriptionText
                    }
                )

    try:
        documentExpirationDate = request_body['documentExpirationDate']
        documentExpirationDate = documentExpirationDate.strip()
    except:
        documentExpirationDate = None
    if documentExpirationDate is None \
        or documentExpirationDate == '' \
        or not CheckValidDate(documentExpirationDate):
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  documentExpirationDate is required, must be a valid date, and must be in the format YYYY-MM-DD.',
                    'documentExpirationDate': documentExpirationDate
                    }
                )

    try:
        documentName = request_body['documentName']
        documentName = documentName.strip()
    except:
        documentName = None
    if documentName is None \
        or documentName == '':
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Missing Parameter.  documentName and path are required.',
                    'documentName': documentName
                    }
                )
    else:
        validExtensionNames = \
            [ 'avi'
            , 'bmp'
            , 'csv' 
            , 'doc'
            , 'docx'
            , 'gif'
            , 'htm'
            , 'html'
            , 'jpeg'
            , 'jpg'
            , 'keynote'
            , 'numbers'
            , 'm4a'
            , 'mid'
            , 'midi'
            , 'mov'
            , 'mp3'
            , 'mp4'
            , 'mpeg'
            , 'mpg'
            , 'ods'
            , 'odt'
            , 'pages'
            , 'pdf'
            , 'png'
            , 'ppt'
            , 'pptx'
            , 'pub'
            , 'rtf'
            , 'text'
            , 'txt'
            , 'vsd'
            , 'vsdx'
            , 'wav'
            , 'wmv'
            , 'xls'
            , 'xlsx'
            , 'xps'
            ]
        extensionPeriod = documentName.rfind('.')
        if extensionPeriod is not None \
            and extensionPeriod > 0 \
            and len(documentName) - extensionPeriod >= 2:
                extensionName = documentName[(extensionPeriod + 1):]
                extensionName = extensionName.strip()
                extensionName = extensionName.lower()
        else:
            extensionName = None
        if extensionName is None \
            or extensionName == '' \
            or ( extensionName is not None \
            and (extensionName not in validExtensionNames) ):
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  documentName does not have an expected extension (e.g. .PDF).',
                    'documentName': documentName
                    }
                )
        else:
            pathEndSlash = documentName.rfind('/')
            if pathEndSlash is None \
                or pathEndSlash < 1:
                pathEndSlash = documentName.rfind('"\"')
            if pathEndSlash is None \
                or pathEndSlash < 1:
                    return Response(
                        status_code=400,
                        headers={'Content-Type': 'application/json'},
                        body = {
                            'message': 'Bad Parameter.  documentName does not have a path to the file.',
                            'documentName': documentName
                            }
                        )
            if not os.path.exists(documentName):
                    return Response(
                        status_code=400,
                        headers={'Content-Type': 'application/json'},
                        body = {
                            'message': 'Bad Parameter.  documentName is not a valid path to the file.',
                            'documentName': documentName
                            }
                        )
            else:
                documentNamePathRemoved = documentName[(pathEndSlash + 1):]
                documentNamePathRemoved = documentNamePathRemoved.strip()
                if documentNamePathRemoved is None \
                    or len(documentNamePathRemoved) < 3:
                        return Response(
                            status_code=400,
                            headers={'Content-Type': 'application/json'},
                            body = {
                                'message': 'Bad Parameter.  documentName (after path is removed) is not a valid name (e.g. minimum of x.y).',
                                'documentName': documentNamePathRemoved
                                }
                            )
                elif len(documentNamePathRemoved) > 500:
                    return Response(
                        status_code=400,
                        headers={'Content-Type': 'application/json'},
                        body = {
                            'message': 'Bad Parameter.  documentName (after path is removed) is too large for database column.',
                            'documentName': documentNamePathRemoved
                            }
                        )

    try:
        documentOriginationDate = request_body['documentOriginationDate']
        documentOriginationDate = documentOriginationDate.strip()
    except:
        documentOriginationDate = None
    if documentOriginationDate is None \
        or documentOriginationDate == '' \
        or not CheckValidDate(documentOriginationDate):
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  documentOriginationDate is required, must be a valid date, and must be in the format YYYY-MM-DD.',
                    'documentOriginationDate': documentOriginationDate
                    }
                )

    if documentOriginationDate is not None \
        and documentExpirationDate is not None \
        and not CheckDateEarlier(documentOriginationDate, documentExpirationDate):
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter(s).  documentOriginationDate must be earlier than documentExpirationDate.',
                    'documentOriginationDate': documentOriginationDate,
                    'documentExpirationDate': documentExpirationDate
                    }
                )

    try:
        documentSearchTags = request_body['documentSearchTags']
        documentSearchTags = documentSearchTags.strip()
        documentSearchTags = documentSearchTags.lower()
    except:
        documentSearchTags = None
    if documentSearchTags == '':
        documentSearchTags = None
    elif documentSearchTags is not None \
        and len(documentSearchTags) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  documentSearchTags is too large for database column.',
                    'documentSearchTags': documentSearchTags
                    }
                )

    try:
        documentSubType = request_body['documentSubType']
        documentSubType = documentSubType.strip()
    except:
        documentSubType = None
    if documentSubType == '':
        documentSubType = None
    elif documentSubType is not None \
        and len(documentSubType) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  documentSubType is too large for database column.',
                    'documentSubType': documentSubType
                    }
                )

    try:
        documentType = request_body['documentType']
        documentType = documentType.strip()
    except:
        documentType = None
    if documentType is None \
        or documentType == '':
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Missing Parameter.  documentType is required.',
                    'documentType': documentType
                    }
                )
    elif documentType is not None \
        and len(documentType) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  documentType is too large for database column.',
                    'documentType': documentType
                    }
                )

    try:
        employeeId = request_body['employeeId']
        employeeId = employeeId.strip()
    except:
        employeeId = None
    if employeeId == '':
        employeeId = None
    elif employeeId is not None \
        and len(employeeId) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  employeeId is too large for database column.',
                    'employeeId': employeeId
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
        orderId = request_body['orderId']
        orderId = orderId.strip()
    except:
        orderId = None
    if orderId == '':
        orderId = None
    elif orderId is not None \
        and len(orderId) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  orderId is too large for database column.',
                    'orderId': orderId
                    }
                )

    try:
        organizationId = request_body['organizationId']
        organizationId = organizationId.strip()
    except:
        organizationId = None
    if organizationId == '':
        organizationId = None
    elif organizationId is not None \
        and len(organizationId) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  organizationId is too large for database column.',
                    'organizationId': organizationId
                    }
                )

    try:
        productId = request_body['productId']
        productId = productId.strip()
    except:
        productId = None
    if productId == '':
        productId = None
    elif productId is not None \
        and len(productId) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  productId is too large for database column.',
                    'productId': productId
                    }
                )

    try:
        rmaId = request_body['rmaId']
        rmaId = rmaId.strip()
    except:
        rmaId = None
    if rmaId == '':
        rmaId = None
    elif rmaId is not None \
        and len(rmaId) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  rmaId is too large for database column.',
                    'rmaId': rmaId
                    }
                )

    try:
        serviceRequestId = request_body['serviceRequestId']
        serviceRequestId = serviceRequestId.strip()
    except:
        serviceRequestId = None
    if serviceRequestId == '':
        serviceRequestId = None
    elif serviceRequestId is not None \
        and len(serviceRequestId) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  serviceRequestId is too large for database column.',
                    'serviceRequestId': serviceRequestId
                    }
                )

    try:
        shipmentId = request_body['shipmentId']
        shipmentId = shipmentId.strip()
    except:
        shipmentId = None
    if shipmentId == '':
        shipmentId = None
    elif shipmentId is not None \
        and len(shipmentId) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  shipmentId is too large for database column.',
                    'shipmentId': shipmentId
                    }
                )

    try:
        sourceDocumentId = request_body['sourceDocumentId']
        sourceDocumentId = sourceDocumentId.strip()
    except:
        sourceDocumentId = None
    if sourceDocumentId == '':
        sourceDocumentId = None
    elif sourceDocumentId is not None \
        and len(sourceDocumentId) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  sourceDocumentId is too large for database column.',
                    'sourceDocumentId': sourceDocumentId
                    }
                )

    try:
        sourceSystem = request_body['sourceSystem']
        sourceSystem = sourceSystem.strip()
    except:
        sourceSystem = None
    if sourceSystem == '':
        sourceSystem = None
    elif sourceSystem is not None \
        and len(sourceSystem) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  sourceSystem is too large for database column.',
                    'sourceSystem': sourceSystem
                    }
                )

    try:
        sourceTransactionAmount = request_body['sourceTransactionAmount']
        sourceTransactionAmount = sourceTransactionAmount.strip()
    except:
        sourceTransactionAmount = None
    if sourceTransactionAmount == '':
        sourceTransactionAmount = None
    elif sourceTransactionAmount is not None \
        and not CheckValidAmount(sourceTransactionAmount):
        return Response(
            status_code=400,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'Bad Parameter.  sourceTransactionAmount must be in a non-negative integer or currency format (e.g. 100 or 100.00).',
                'sourceTransactionAmount': sourceTransactionAmount
                }
            )

    try:
        sourceTransactionId = request_body['sourceTransactionId']
        sourceTransactionId = sourceTransactionId.strip()
    except:
        sourceTransactionId = None
    if sourceTransactionId == '':
        sourceTransactionId = None
    elif sourceTransactionId is not None \
        and len(sourceTransactionId) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  sourceTransactionId is too large for database column.',
                    'sourceTransactionId': sourceTransactionId
                    }
                )

    try:
        sourceTransactionType = request_body['sourceTransactionType']
        sourceTransactionType = sourceTransactionType.strip()
    except:
        sourceTransactionType = None
    if sourceTransactionType == '':
        sourceTransactionType = None
    elif sourceTransactionType is not None \
        and len(sourceTransactionType) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  sourceTransactionType is too large for database column.',
                    'sourceTransactionType': sourceTransactionType
                    }
                )

    try:
        storeId = request_body['storeId']
        storeId = storeId.strip()
    except:
        storeId = None
    if storeId == '':
        storeId = None
    elif storeId is not None \
        and len(storeId) > 255:
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  storeId is too large for database column.',
                    'storeId': storeId
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

    # Only 4 of the S3 Storage Classes are permitted.  Other Storage Classes do not have high redundancy or will be too slow to retrieve.
    # INTELLIGENT_TIERING is used as the default value.
    # https://aws.amazon.com/s3/storage-classes/ 
    try:
        s3StorageClass = request_body['s3StorageClass']
        s3StorageClass = s3StorageClass.strip()
        s3StorageClass = s3StorageClass.upper()
    except:
        s3StorageClass = None
    if s3StorageClass is None \
        or s3StorageClass == '':
            s3StorageClass = 'INTELLIGENT_TIERING' # set a default value
    elif s3StorageClass != 'STANDARD' \
        and s3StorageClass != 'INTELLIGENT_TIERING' \
        and s3StorageClass != 'STANDARD_IA' \
        and s3StorageClass != 'GLACIER_IR':
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  s3StorageClass must be STANDARD, INTELLIGENT_TIERING, STANDARD_IA, or GLACIER_IR.',
                    's3StorageClass': s3StorageClass
                    }
                )

    # Generate the Folder structure and internal Document Name
    # Folder structure is based on YYYY-MM of Document Origination Date, and then Document Type
    documentInternalName = documentOriginationDate[0:7] + '/' + documentType + '/' + documentUUId + '.' + extensionName
            
    # system-related attributes
    createdUTCDateTime = currentUTCDateTime
    updatedUTCDateTime = currentUTCDateTime
    accessedCount = 0
    lastAccessedUTCDateTime = None
    databaseDocumentConsistencyCheck = 'OK'

    try:
        s3ExpirationDate = documentExpirationDate + ' 23:59:59 GMT'
        s3FileTags = 'businessArea=' + (businessArea or 'Not Specified')
        s3FileTags = s3FileTags + '&' + 'documentOriginationYear=' + (documentOriginationDate[0:4] or '0000')
        s3FileTags = s3FileTags + '&' + 'documentType=' + (documentType or 'Not Specified')
        s3FileTags = s3FileTags + '&' + 'organizationId=' + (organizationId or 'Not Specified')

        s3Client = boto3.client('s3',region_name=S3REGIONNAME)
        fileName = open(documentName, 'rb').read()
        fileAsBinary = io.BytesIO(fileName)
        s3Client.upload_fileobj(
            fileAsBinary
            , S3BUCKETNAME
            , documentInternalName
            , ExtraArgs=
            {
                'Expires': s3ExpirationDate,
                'Metadata': {'documentstorage-documentUUId': documentUUId},
                'ServerSideEncryption': S3SERVERSIDEENCRYPTION,
                'StorageClass': s3StorageClass,
                'Tagging': s3FileTags
            }
            )
        fileName = None
        s3Client = None
    except Exception as e:
        documentsPOST_routes.log.error('Could not upload file to S3 Bucket due to {}'.format(e))
        return Response(
            status_code=500,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'Could not upload file to S3 Bucket due to {}'.format(e),
                'documentName': documentName
                }
            )

    if legalHold == 'Y':
        try:
            s3Client = boto3.client('s3',region_name=S3REGIONNAME)
            s3Client.put_object_legal_hold(
                Bucket = S3BUCKETNAME
                , Key = documentInternalName
                , LegalHold =
                {
                    'Status': 'ON',
                }
                )
            s3Client = None
        except Exception as e:
            documentsPOST_routes.log.error('Could not put_object_legal_hold on S3 Object due to {}'.format(e))

            try:
                # delete from S3 due to S3 failure
                s3Client = boto3.client('s3',region_name=S3REGIONNAME)
                s3Client.delete_object(
                    Bucket = S3BUCKETNAME
                    , Key = documentInternalName
                )
                s3Client = None
            except:
                None

            return Response(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Could not put_object_legal_hold on S3 Object due to {}'.format(e),
                    'documentName': documentName
                    }
                )

    (dbConnection, errorMessage) = CreateDBConnection()
    if dbConnection is None \
        or errorMessage != 'OK':
        documentsPOST_routes.log.error('Could not create Database Connection.  ' + errorMessage)

        try:
            # delete from S3 due to DB connection failure
            if legalHold == 'Y':
                s3Client = boto3.client('s3',region_name=S3REGIONNAME)
                s3Client.put_object_legal_hold(
                    Bucket = S3BUCKETNAME
                    , Key = documentInternalName
                    , LegalHold =
                    {
                        'Status': 'OFF',
                    }
                    )
                s3Client = None
            s3Client = boto3.client('s3',region_name=S3REGIONNAME)
            s3Client.delete_object(
                Bucket = S3BUCKETNAME
                , Key = documentInternalName
            )
            s3Client = None
        except:
            None

        return Response(
            status_code=500,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'Could not create Database Connection.  ' + errorMessage
                }
            )

    sqlStatement = 'insert into tdocument ' \
        + '( agreementId ' \
        + ', businessArea ' \
        + ', containsSensitiveData ' \
        + ', customerCompanyName ' \
        + ', customerFirstName ' \
        + ', customerId1 ' \
        + ', customerId2 ' \
        + ', customerId3 ' \
        + ', customerLastName ' \
        + ', customerType ' \
        + ', descriptionText ' \
        + ', documentExpirationDate ' \
        + ', documentInternalName ' \
        + ', documentName ' \
        + ', documentOriginationDate ' \
        + ', documentSearchTags ' \
        + ', documentSubType ' \
        + ', documentType ' \
        + ', documentUUId ' \
        + ', employeeId ' \
        + ', legalHold ' \
        + ', orderId ' \
        + ', organizationId ' \
        + ', productId ' \
        + ', rmaId ' \
        + ', serviceRequestId ' \
        + ', shipmentId ' \
        + ', sourceDocumentId ' \
        + ', sourceSystem ' \
        + ', sourceTransactionAmount ' \
        + ', sourceTransactionId ' \
        + ', sourceTransactionType ' \
        + ', storeId ' \
        + ', createdUTCDateTime ' \
        + ', updatedUTCDateTime ' \
        + ', accessedCount ' \
        + ', lastAccessedUTCDateTime ' \
        + ', databaseDocumentConsistencyCheck ' \
        + ') ' \
        + 'values ' \
        + '( ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', %s ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', %s ' \
        + ', %s ' \
        + ', %s ' \
        + ', %s ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', %s ' \
        + ', %s ' \
        + ', ifnull(null, %s) ' \
        + ', %s ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', ifnull(null, %s) ' \
        + ', %s ' \
        + ', %s ' \
        + ', %s ' \
        + ', ifnull(null, %s) ' \
        + ', %s ' \
        + ')'

    sqlArguments = \
          agreementId \
        , businessArea \
        , containsSensitiveData \
        , customerCompanyName \
        , customerFirstName \
        , customerId1 \
        , customerId2 \
        , customerId3 \
        , customerLastName \
        , customerType \
        , descriptionText \
        , documentExpirationDate \
        , documentInternalName \
        , documentNamePathRemoved \
        , documentOriginationDate \
        , documentSearchTags \
        , documentSubType \
        , documentType \
        , documentUUId \
        , employeeId \
        , legalHold \
        , orderId \
        , organizationId \
        , productId \
        , rmaId \
        , serviceRequestId \
        , shipmentId \
        , sourceDocumentId \
        , sourceSystem \
        , sourceTransactionAmount \
        , sourceTransactionId \
        , sourceTransactionType \
        , storeId \
        , createdUTCDateTime \
        , updatedUTCDateTime \
        , accessedCount \
        , lastAccessedUTCDateTime \
        , databaseDocumentConsistencyCheck

    dbCursor = dbConnection.cursor(prepared=True)
    try:
        dbCursor.execute(sqlStatement,sqlArguments)
        dbConnection.commit()
    except Exception as e:
        dbConnection.rollback()
        documentsPOST_routes.log.error('INSERT into tdocument failed due to  {}'.format(e))

        try:
            # delete from S3 due to SQL failure
            if legalHold == 'Y':
                s3Client = boto3.client('s3',region_name=S3REGIONNAME)
                s3Client.put_object_legal_hold(
                    Bucket = S3BUCKETNAME
                    , Key = documentInternalName
                    , LegalHold =
                    {
                        'Status': 'OFF',
                    }
                    )
                s3Client = None
            s3Client = boto3.client('s3',region_name=S3REGIONNAME)
            s3Client.delete_object(
                Bucket = S3BUCKETNAME
                , Key = documentInternalName
            )
            s3Client = None
        except:
            None

        return Response(
            status_code=500,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'INSERT into tdocument failed due to {}'.format(e),
                'documentName': documentName
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
        , createdUTCDateTime \
        , 'POST' \
        , userId \
        , userType

    dbCursor = dbConnection.cursor(prepared=True)
    try:
        dbCursor.execute(sqlStatement,sqlArguments)
        dbConnection.commit()
    except Exception as e:
        dbConnection.rollback()
        documentsPOST_routes.log.error('INSERT into tdocument_auditlog failed due to {}'.format(e))

        # delete from tdocument due to SQL failure
        sqlStatement = 'delete from tdocument where documentUUId = ? '
        sqlArguments = (documentUUId,)
        dbCursor = dbConnection.cursor(prepared=True)
        try:
            dbCursor.execute(sqlStatement,sqlArguments)
            dbConnection.commit()
        except:
            dbConnection.rollback()

        try:
            # delete from S3 due to SQL failure
            if legalHold == 'Y':
                s3Client = boto3.client('s3',region_name=S3REGIONNAME)
                s3Client.put_object_legal_hold(
                    Bucket = S3BUCKETNAME
                    , Key = documentInternalName
                    , LegalHold =
                    {
                        'Status': 'OFF',
                    }
                    )
                s3Client = None
            s3Client = boto3.client('s3',region_name=S3REGIONNAME)
            s3Client.delete_object(
                Bucket = S3BUCKETNAME
                , Key = documentInternalName
            )
            s3Client = None
        except:
            None

        return Response(
            status_code=500,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'INSERT into tdocument_auditlog failed due to {}'.format(e),
                'documentName': documentName                    
                }
            )   

    if dbCursor:
        dbCursor.close()

    if dbConnection:
        dbConnection.close()

    # Successful POST
    # 201 Created
    return Response(
        status_code=201,
        headers={'Content-Type': 'application/json'},
        body = {
            'documentUUid': documentUUId,
            'createdUTCDateTime': currentUTCDateTime
            }
        )




# END
