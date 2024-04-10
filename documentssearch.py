# Document Storage for AWS
#
# Document Storage for AWS is a freemium accelerator from Seattle Software Works, Inc.
# https://seattleworks.com 
#
# Please see README.md
#



from chalice import Blueprint, Response

from chalicelib.common import CheckContainsSQLWildcard, CheckContainsWildcard, CheckValidAmount, CheckValidDate, CheckValidUUId, CreateDBConnection, TransformWildcards

import collections
import os
import json

documentssearch_routes = Blueprint(__name__)




@documentssearch_routes.route('/customers/v1/documentssearch', methods=['POST'], content_types=['application/json'], cors=False)
# Notes
# - POST method is used instead of GET since there may be many search parameters,
#   and to avoid having sensitive attributes (e.g. Last Name) in the logged URL.
# - The parameter usageMode must be CARE, CUSTOMER, EMPLOYEE, or PRODUCT.
# - Additional parameters may be required for a specific usageMode.

# Dev Notes
# Authentication
# testing of every parameter, and parameters with wildcards

def documentsSEARCH():

    request = documentssearch_routes.current_request
    request_body = documentssearch_routes.current_request.json_body

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

    try:
        usageMode = request_body['usageMode']
        usageMode = usageMode.strip()
        usageMode = usageMode.upper()
    except:
        usageMode = None
    if usageMode != 'CARE' \
        and usageMode != 'CUSTOMER' \
        and usageMode != 'EMPLOYEE' \
        and usageMode != 'PRODUCT':
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  usageMode must be CARE, CUSTOMER, EMPLOYEE, or PRODUCT.',
                    'usageMode': usageMode
                    }
                )

    try:
        agreementId = request_body['agreementId']
        agreementId = agreementId.strip()
        agreementId = TransformWildcards(agreementId)
        if agreementId == '':
            agreementId = None
    except:
        agreementId = None

    try:
        businessArea = request_body['businessArea']
        businessArea = businessArea.strip()
        businessArea = TransformWildcards(businessArea)
        if businessArea == '':
            businessArea = None
    except:
        businessArea = None

    try:
        containsSensitiveData = request_body['containsSensitiveData']
        containsSensitiveData = containsSensitiveData.strip()
        containsSensitiveData = containsSensitiveData.upper()
    except:
        containsSensitiveData = None
    if containsSensitiveData is not None \
        and containsSensitiveData != 'N' \
        and containsSensitiveData != 'Y':
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
        customerCompanyName = TransformWildcards(customerCompanyName)
        if customerCompanyName == '':
            customerCompanyName = None
    except:
        customerCompanyName = None

    try:
        customerFirstName = request_body['customerFirstName']
        customerFirstName = customerFirstName.strip()
        customerFirstName = TransformWildcards(customerFirstName)
        if customerFirstName == '':
            customerFirstName = None
    except:
        customerFirstName = None

    try:
        customerId1 = request_body['customerId1']
        customerId1 = customerId1.strip()
        customerId1 = TransformWildcards(customerId1)
        if customerId1 == '':
            customerId1 = None
    except:
        customerId1 = None

    try:
        customerId2 = request_body['customerId2']
        customerId2 = customerId2.strip()
        customerId2 = TransformWildcards(customerId2)
        if customerId2 == '':
            customerId2 = None
    except:
        customerId2 = None

    try:
        customerId3 = request_body['customerId3']
        customerId3 = customerId3.strip()
        customerId3 = TransformWildcards(customerId3)
        if customerId3 == '':
            customerId3 = None
    except:
        customerId3 = None

    try:
        customerLastName = request_body['customerLastName']
        customerLastName = customerLastName.strip()
        customerLastName = TransformWildcards(customerLastName)
        if customerLastName == '':
            customerLastName = None
    except:
        customerLastName = None

    try:
        customerType = request_body['customerType']
        customerType = customerType.strip()
        customerType = TransformWildcards(customerType)
        if customerType == '':
            customerType = None
    except:
        customerType = None

    try:
        descriptionText = request_body['descriptionText']
        descriptionText = descriptionText.strip()
        descriptionText = TransformWildcards(descriptionText)
        if descriptionText == '':
            descriptionText = None
    except:
        descriptionText = None

    try:
        documentExpirationDate = request_body['documentExpirationDate']
        documentExpirationDate = documentExpirationDate.strip()
        documentExpirationDate = TransformWildcards(documentExpirationDate)
        if documentExpirationDate == '':
            documentExpirationDate = None
    except:
        documentExpirationDate = None
    if documentExpirationDate is not None \
        and not CheckContainsSQLWildcard(documentExpirationDate) \
        and not CheckValidDate(documentExpirationDate):
        return Response(
            status_code=400,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'Bad Parameter.  documentExpirationDate must be a valid date and format must be YYYY-MM-DD.',
                'documentExpirationDate': documentExpirationDate
                }
            )

    try:
        documentOriginationDate = request_body['documentOriginationDate']
        documentOriginationDate = documentOriginationDate.strip()
        documentOriginationDate = TransformWildcards(documentOriginationDate)
        if documentOriginationDate == '':
            documentOriginationDate = None
    except:
        documentOriginationDate = None
    if documentOriginationDate is not None \
        and not CheckContainsSQLWildcard(documentOriginationDate) \
        and not CheckValidDate(documentOriginationDate):
        return Response(
            status_code=400,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'Bad Parameter.  documentOriginationDate must be a valid date and format must be YYYY-MM-DD.',
                'documentOriginationDate': documentOriginationDate
                }
            )

    try:
        documentSearchTags = request_body['documentSearchTags']
        documentSearchTags = documentSearchTags.strip()
        documentSearchTags = TransformWildcards(documentSearchTags)
        # Additional replaces for spaces between provided keywords
        documentSearchTags = documentSearchTags.replace('   ','%')
        documentSearchTags = documentSearchTags.replace('  ','%')
        documentSearchTags = documentSearchTags.replace(' ','%')
        if documentSearchTags == '':
            documentSearchTags = None
    except:
        documentSearchTags = None

    try:
        documentSubType = request_body['documentSubType']
        documentSubType = documentSubType.strip()
        documentSubType = TransformWildcards(documentSubType)
        if documentSubType == '':
            documentSubType = None
    except:
        documentSubType = None

    try:
        documentType = request_body['documentType']
        documentType = documentType.strip()
        documentType = TransformWildcards(documentType)
        if documentType == '':
            documentType = None
    except:
        documentType = None

    try:
        documentUUId = request_body['documentUUId']
        documentUUId = documentUUId.strip()
        documentUUId = documentUUId.lower()
        documentUUId = TransformWildcards(documentUUId)
        if documentUUId == '':
            documentUUId = None
    except:
        documentUUId = None

    try:
        employeeId = request_body['employeeId']
        employeeId = employeeId.strip()
        employeeId = TransformWildcards(employeeId)
        if employeeId == '':
            employeeId = None
    except:
        employeeId = None

    try:
        legalHold = request_body['legalHold']
        legalHold = legalHold.strip()
        legalHold = legalHold.upper()
    except:
        legalHold = None
    if legalHold is not None \
        and legalHold != 'N' \
        and legalHold != 'Y':
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
        orderId = TransformWildcards(orderId)
        if orderId == '':
            orderId = None
    except:
        orderId = None

    try:
        organizationID = request_body['organizationId']
        organizationID = organizationID.strip()
        organizationID = TransformWildcards(organizationID)
        if organizationID == '':
            organizationID = None
    except:
        organizationID = None

    try:
        productId = request_body['productId']
        productId = rmaId.strip()
        productId = TransformWildcards(productId)
        if productId == '':
            productId = None
    except:
        productId = None

    try:
        rmaId = request_body['rmaId']
        rmaId = rmaId.strip()
        rmaId = TransformWildcards(rmaId)
        if rmaId == '':
            rmaId = None
    except:
        rmaId = None

    try:
        serviceRequestId = request_body['serviceRequestId']
        serviceRequestId = serviceRequestId.strip()
        serviceRequestId = TransformWildcards(serviceRequestId)
        if serviceRequestId == '':
            serviceRequestId = None
    except:
        serviceRequestId = None

    try:
        shipmentId = request_body['shipmentId']
        shipmentId = shipmentId.strip()
        shipmentId = TransformWildcards(shipmentId)
        if shipmentId == '':
            shipmentId = None
    except:
        shipmentId = None

    try:
        sourceDocumentId = request_body['sourceDocumentId']
        sourceDocumentId = sourceDocumentId.strip()
        sourceDocumentId = TransformWildcards(sourceDocumentId)
        if sourceDocumentId == '':
            sourceDocumentId = None
    except:
        sourceDocumentId = None

    try:
        sourceSystem = request_body['sourceSystem']
        sourceSystem = sourceSystem.strip()
        sourceSystem = TransformWildcards(sourceSystem)
        if sourceSystem == '':
            sourceSystem = None
    except:
        sourceSystem = None

    try:
        sourceTransactionAmount = request_body['sourceTransactionAmount']
        sourceTransactionAmount = sourceTransactionAmount.strip()
        sourceTransactionAmount = TransformWildcards(sourceTransactionAmount)
        if sourceTransactionAmount == '':
            sourceTransactionAmount = None
    except:
        sourceTransactionAmount = None
    if sourceTransactionAmount is not None \
        and not CheckContainsSQLWildcard(sourceTransactionAmount) \
        and not CheckValidAmount(sourceTransactionAmount):
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Bad Parameter.  sourceTransactionAmount must be in an integer or currency format (e.g. 100 or 100.00).',
                    'sourceTransactionAmount': sourceTransactionAmount
                    }
                )            

    try:
        sourceTransactionId = request_body['sourceTransactionId']
        sourceTransactionId = sourceTransactionId.strip()
        sourceTransactionId = TransformWildcards(sourceTransactionId)
        if sourceTransactionId == '':
            sourceTransactionId = None
    except:
        sourceTransactionId = None

    try:
        sourceTransactionType = request_body['sourceTransactionType']
        sourceTransactionType = sourceTransactionType.strip()
        sourceTransactionType = TransformWildcards(sourceTransactionType)
        if sourceTransactionType == '':
            sourceTransactionType = None
    except:
        sourceTransactionType = None

    try:
        storeId = request_body['storeId']
        storeId = storeId.strip()
        storeId = TransformWildcards(storeId)
        if storeId == '':
            storeId = None
    except:
        storeId = None

    # Require 1+ DB-indexed parameters for a CARE search to ensure good query performance.
    # The elements in this logic should have a corresponding index on the DB table where the element is
    # the leading column in a DB index.
    if (usageMode == 'CARE' \
        and agreementId is None \
        and customerCompanyName is None \
        and customerId1 is None \
        and customerId2 is None \
        and customerId3 is None \
        and customerLastName is None \
        and documentUUId is None \
        and employeeId is None \
        and orderId is None \
        and productId is None \
        and rmaId is None \
        and serviceRequestId is None \
        and shipmentId is None \
        and sourceDocumentId is None \
        and sourceTransactionId is None \
        and storeId is None \
        ):
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Missing Parameter.  Must provide 1+ DB-indexed parameters (e.g. orderId) for a CARE search.'
                    }
                )
    # Require 1+ of 3 customerId's for a CUSTOMER search.
    elif (usageMode == 'CUSTOMER' \
        and customerId1 is None \
        and customerId2 is None \
        and customerId3 is None \
        ):
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Missing Parameter.  Must provide 1+ customerId for a CUSTOMER search.'
                    }
                )
    # Require employeeId for an EMPLOYEE search.
    elif (usageMode == 'EMPLOYEE' \
        and employeeId is None \
        ):
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Missing Parameter.  Must provide employeeId for an EMPLOYEE search.'
                    }
                )
    # Require productId for a PRODUCT search.
    elif (usageMode == 'PRODUCT' \
        and productId is None \
        ):
            return Response(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Missing Parameter.  Must provide productId for a PRODUCT search.'
                    }
                )

    # Build the SQL statement.
    # Returned values will return '' instead of NULL to ensure consistent transformation to JSON.
    # Excluding N/Y indicator columns, predicates in the WHERE clause use parameters to mitigate
    # risk of a SQL-injection attack.
    dbQueryBase = 'select ' \
        + '  ifnull(agreementId,"") ' \
        + ', ifnull(businessArea,"") ' \
        + ', ifnull(containsSensitiveData,"") ' \
        + ', ifnull(customerCompanyName,"") ' \
        + ', ifnull(customerFirstName,"") ' \
        + ', ifnull(customerId1,"") ' \
        + ', ifnull(customerId2,"") ' \
        + ', ifnull(customerId3,"") ' \
        + ', ifnull(customerLastName,"") ' \
        + ', ifnull(customerType,"") ' \
        + ', ifnull(descriptionText,"") ' \
        + ', ifnull(documentExpirationDate,"") ' \
        + ', ifnull(documentInternalName,"") ' \
        + ', ifnull(documentName,"") ' \
        + ', ifnull(documentOriginationDate,"") ' \
        + ', ifnull(documentSearchTags,"") ' \
        + ', ifnull(documentSubType,"") ' \
        + ', ifnull(documentType,"") ' \
        + ', ifnull(documentUUId,"") ' \
        + ', ifnull(employeeId,"") ' \
        + ', ifnull(legalHold,"") ' \
        + ', ifnull(orderId,"") ' \
        + ', ifnull(organizationId,"") ' \
        + ', ifnull(productId,"") ' \
        + ', ifnull(rmaId,"") ' \
        + ', ifnull(serviceRequestId,"") ' \
        + ', ifnull(shipmentId,"") ' \
        + ', ifnull(sourceDocumentId,"") ' \
        + ', ifnull(sourceSystem,"") ' \
        + ', ifnull(sourceTransactionAmount,"") ' \
        + ', ifnull(sourceTransactionId,"") ' \
        + ', ifnull(sourceTransactionType,"") ' \
        + ', ifnull(storeId,"") ' \
        + ', ifnull(createdUTCDateTime,"") ' \
        + ', ifnull(updatedUTCDateTime,"") ' \
        + ', ifnull(accessedCount,"") ' \
        + ', ifnull(lastAccessedUTCDateTime,"") ' \
        + ', ifnull(databaseDocumentConsistencyCheck,"") ' \
        + 'from tdocument '

    # set a 'base' to simplify logic below when appending to WHERE portion with predicates
    dbQueryWhere = 'where 1=1 '

    if agreementId is None:
        agreementId = '%'
        dbQueryWhere = dbQueryWhere + 'and (agreementId like ? or agreementId is null) '
    elif CheckContainsSQLWildcard(agreementId):
        dbQueryWhere = dbQueryWhere + 'and agreementId like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and agreementId = ? '

    if businessArea is None:
            businessArea = '%'
            dbQueryWhere = dbQueryWhere + 'and (businessArea like ? or businessArea is null) '
    elif businessArea is not None \
        and CheckContainsSQLWildcard(businessArea):
            dbQueryWhere = dbQueryWhere + 'and businessArea like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and businessArea = ? '

    if containsSensitiveData == 'N':
        dbQueryWhere = dbQueryWhere + "and containsSensitiveData = 'N' "
    elif containsSensitiveData == 'Y':
        dbQueryWhere = dbQueryWhere + "and containsSensitiveData = 'Y' "

    if customerCompanyName is None:
        customerCompanyName = '%'
        dbQueryWhere = dbQueryWhere + 'and (customerCompanyName like ? or customerCompanyName is null) '
    elif customerCompanyName is not None \
        and CheckContainsSQLWildcard(customerCompanyName):
            dbQueryWhere = dbQueryWhere + 'and customerCompanyName like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and customerCompanyName = ? '

    if customerFirstName is None:
        customerFirstName = '%'
        dbQueryWhere = dbQueryWhere + 'and (customerFirstName like ? or customerFirstName is null) '
    elif customerFirstName is not None \
        and CheckContainsSQLWildcard(customerFirstName):
            dbQueryWhere = dbQueryWhere + 'and customerFirstName like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and customerFirstName = ? '

    if customerId1 is None:
        customerId1 = '%'
        dbQueryWhere = dbQueryWhere + 'and (customerId1 like ? or customerId1 is null) '
    elif customerId1 is not None \
        and CheckContainsSQLWildcard(customerId1):
        dbQueryWhere = dbQueryWhere + 'and customerId1 like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and customerId1 = ? '

    if customerId2 is None:
        customerId2 = '%'
        dbQueryWhere = dbQueryWhere + 'and (customerId2 like ? or customerId2 is null) '
    elif customerId2 is not None \
        and CheckContainsSQLWildcard(customerId2):
        dbQueryWhere = dbQueryWhere + 'and customerId2 like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and customerId2 = ? '

    if customerId3 is None:
        customerId3 = '%'
        dbQueryWhere = dbQueryWhere + 'and (customerId3 like ? or customerId3 is null) '
    elif customerId3 is not None \
        and CheckContainsSQLWildcard(customerId3):
        dbQueryWhere = dbQueryWhere + 'and customerId3 like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and customerId3 = ? '

    if customerLastName is None:
        customerLastName = '%'
        dbQueryWhere = dbQueryWhere + 'and (customerLastName like ? or customerLastName is null) '
    elif customerLastName is not None \
        and CheckContainsSQLWildcard(customerLastName):
            dbQueryWhere = dbQueryWhere + 'and customerLastName like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and customerLastName = ? '

    if customerType is None:
        customerType = '%'
        dbQueryWhere = dbQueryWhere + 'and (customerType like ? or customerType is null) '
    elif customerType is not None \
        and CheckContainsSQLWildcard(customerType):
            dbQueryWhere = dbQueryWhere + 'and customerType like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and customerType = ? '

    if descriptionText is None:
        descriptionText = '%'
        dbQueryWhere = dbQueryWhere + 'and (descriptionText like ? or descriptionText is null) '
    elif descriptionText is not None \
        and CheckContainsSQLWildcard(descriptionText):
            dbQueryWhere = dbQueryWhere + 'and descriptionText like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and descriptionText = ? '

    if documentExpirationDate is None:
        documentExpirationDate = '%'
        dbQueryWhere = dbQueryWhere + 'and (documentExpirationDate like ? or documentExpirationDate is null) '
    elif documentExpirationDate is not None \
        and CheckContainsSQLWildcard(documentExpirationDate):
            dbQueryWhere = dbQueryWhere + 'and documentExpirationDate like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and documentExpirationDate = ? '

    if documentOriginationDate is None:
        documentOriginationDate = '%'
        dbQueryWhere = dbQueryWhere + 'and (documentOriginationDate like ? or documentOriginationDate is null) '
    elif documentOriginationDate is not None \
        and CheckContainsSQLWildcard(documentOriginationDate):
            dbQueryWhere = dbQueryWhere + 'and documentOriginationDate like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and documentOriginationDate = ? '

    if documentSearchTags is None:
        documentSearchTags = '%'
        dbQueryWhere = dbQueryWhere + 'and (documentSearchTags like ? or documentSearchTags is null) '
    elif documentSearchTags is not None \
        and CheckContainsSQLWildcard(documentSearchTags):
            dbQueryWhere = dbQueryWhere + 'and documentSearchTags like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and documentSearchTags = ? '

    if documentSubType is None:
        documentSubType = '%'
        dbQueryWhere = dbQueryWhere + 'and (documentSubType like ? or documentSubType is null) '
    elif documentSubType is not None \
        and CheckContainsSQLWildcard(documentSubType):
            dbQueryWhere = dbQueryWhere + 'and documentSubType like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and documentSubType = ? '

    if documentType is None:
        documentType = '%'
        dbQueryWhere = dbQueryWhere + 'and (documentType like ? or documentType is null) '
    elif documentType is not None \
        and CheckContainsSQLWildcard(documentType):
            dbQueryWhere = dbQueryWhere + 'and documentType like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and documentType = ? '

    if documentUUId is None:
        documentUUId = '%'
        dbQueryWhere = dbQueryWhere + 'and (documentUUId like ? or documentUUId is null) '
    elif documentUUId is not None \
        and CheckContainsSQLWildcard(documentUUId):
            dbQueryWhere = dbQueryWhere + 'and documentUUId like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and documentUUId = ? '

    if employeeId is None:
        employeeId = '%'
        dbQueryWhere = dbQueryWhere + 'and (employeeId like ? or employeeId is null) '
    elif employeeId is not None \
        and CheckContainsSQLWildcard(employeeId):
            dbQueryWhere = dbQueryWhere + 'and employeeId like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and employeeId = ? '

    if legalHold == 'N':
        dbQueryWhere = dbQueryWhere + "and legalHold = 'N' "
    elif legalHold == 'Y':
        dbQueryWhere = dbQueryWhere + "and legalHold = 'Y' "

    if orderId is None:
        orderId = '%'
        dbQueryWhere = dbQueryWhere + 'and (orderId like ? or orderId is null) '
    elif orderId is not None \
        and CheckContainsSQLWildcard(orderId):
            dbQueryWhere = dbQueryWhere + 'and orderId like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and orderId = ? '

    if organizationID is None:
        organizationID = '%'
        dbQueryWhere = dbQueryWhere + 'and (organizationID like ? or organizationID is null) '
    elif organizationID is not None \
        and CheckContainsSQLWildcard(organizationID):
            dbQueryWhere = dbQueryWhere + 'and organizationID like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and organizationID = ? '

    if productId is None:
        productId = '%'
        dbQueryWhere = dbQueryWhere + 'and (productId like ? or productId is null) '
    elif productId is not None \
        and CheckContainsSQLWildcard(productId):
            dbQueryWhere = dbQueryWhere + 'and productId like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and productId = ? '

    if rmaId is None:
        rmaId = '%'
        dbQueryWhere = dbQueryWhere + 'and (rmaId like ? or rmaId is null) '
    elif rmaId is not None \
        and CheckContainsSQLWildcard(rmaId):
            dbQueryWhere = dbQueryWhere + 'and rmaId like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and rmaId = ? '

    if serviceRequestId is None:
        serviceRequestId = '%'
        dbQueryWhere = dbQueryWhere + 'and (serviceRequestId like ? or serviceRequestId is null) '
    elif serviceRequestId is not None \
        and CheckContainsSQLWildcard(serviceRequestId):
            dbQueryWhere = dbQueryWhere + 'and serviceRequestId like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and serviceRequestId = ? '

    if shipmentId is None:
        shipmentId = '%'
        dbQueryWhere = dbQueryWhere + 'and (shipmentId like ? or shipmentId is null) '
    elif shipmentId is not None \
        and CheckContainsSQLWildcard(shipmentId):
            dbQueryWhere = dbQueryWhere + 'and shipmentId like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and shipmentId = ? '

    if sourceDocumentId is None:
        sourceDocumentId = '%'
        dbQueryWhere = dbQueryWhere + 'and (sourceDocumentId like ? or sourceDocumentId is null) '
    elif sourceDocumentId is not None \
        and CheckContainsSQLWildcard(sourceDocumentId):
            dbQueryWhere = dbQueryWhere + 'and sourceDocumentId like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and sourceDocumentId = ? '

    if sourceSystem is None:
        sourceSystem = '%'
        dbQueryWhere = dbQueryWhere + 'and (sourceSystem like ? or sourceSystem is null) '
    elif sourceSystem is not None \
        and CheckContainsSQLWildcard(sourceSystem):
            dbQueryWhere = dbQueryWhere + 'and sourceSystem like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and sourceSystem = ? '

    if sourceTransactionAmount is None:
        sourceTransactionAmount = '%'
        dbQueryWhere = dbQueryWhere + 'and (sourceTransactionAmount like ? or sourceTransactionAmount is null) '
    elif sourceTransactionAmount is not None \
        and CheckContainsSQLWildcard(sourceTransactionAmount):
            dbQueryWhere = dbQueryWhere + 'and sourceTransactionAmount like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and sourceTransactionAmount = ? '

    if sourceTransactionId is None:
        sourceTransactionId = '%'
        dbQueryWhere = dbQueryWhere + 'and (sourceTransactionId like ? or sourceTransactionId is null) '
    elif sourceTransactionId is not None \
        and CheckContainsSQLWildcard(sourceTransactionId):
            dbQueryWhere = dbQueryWhere + 'and sourceTransactionId like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and sourceTransactionId = ? '

    if sourceTransactionType is None:
        sourceTransactionType = '%'
        dbQueryWhere = dbQueryWhere + 'and (sourceTransactionType like ? or sourceTransactionType is null) '
    elif sourceTransactionType is not None \
        and CheckContainsSQLWildcard(sourceTransactionType):
            dbQueryWhere = dbQueryWhere + 'and sourceTransactionType like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and sourceTransactionType = ? '

    if storeId is None:
        storeId = '%'
        dbQueryWhere = dbQueryWhere + 'and (storeId like ? or storeId is null) '
    elif storeId is not None \
        and CheckContainsSQLWildcard(storeId):
            dbQueryWhere = dbQueryWhere + 'and storeId like ? '
    else:
        dbQueryWhere = dbQueryWhere + 'and storeId = ? '

    # Set the ORDER BY and a limit on returned rows
    if usageMode == 'CARE':
        dbQueryOrderBy =  'order by documentOriginationDate desc limit 500 '
    elif usageMode == 'CUSTOMER':
        dbQueryOrderBy =  'order by documentOriginationDate desc limit 100 '
    elif usageMode == 'EMPLOYEE':
        dbQueryOrderBy =  'order by documentOriginationDate desc limit 500 '
    elif usageMode == 'PRODUCT':
        dbQueryOrderBy = 'order by documentType asc, documentOriginationDate asc limit 500 '
    else:
        dbQueryOrderBy = 'limit 500 '

    sqlStatement = dbQueryBase + dbQueryWhere + dbQueryOrderBy

    # Arguments are never provided for containsSensitiveData and legalHold
    # since the logic and resulting SQL will only specify N or Y
    sqlArguments = \
        agreementId \
        , businessArea \
        , customerCompanyName \
        , customerFirstName \
        , customerId1 \
        , customerId2 \
        , customerId3 \
        , customerLastName \
        , customerType \
        , descriptionText \
        , documentExpirationDate \
        , documentOriginationDate \
        , documentSearchTags \
        , documentSubType \
        , documentType \
        , documentUUId \
        , employeeId \
        , orderId \
        , organizationID \
        , productId \
        , rmaId \
        , serviceRequestId \
        , shipmentId \
        , sourceDocumentId \
        , sourceSystem \
        , sourceTransactionAmount \
        , sourceTransactionId \
        , sourceTransactionType \
        , storeId

    (dbConnection, errorMessage) = CreateDBConnection()
    if dbConnection is None \
        or errorMessage != 'OK':
            documentssearch_routes.log.error('Could not create Database Connection.  ' + errorMessage)
            return Response(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Could not create Database Connection.  ' + errorMessage
                    }
                )

    try:
        dbCursor = dbConnection.cursor(prepared=True)
        dbCursor.execute(sqlStatement, sqlArguments)
        dbResults = dbCursor.fetchall()
        if dbResults is not None:
            dbResultsRecordCount = len(dbResults)
        else:
            dbResultsRecordCount = 0
        dbConnection.commit()
        if dbCursor:
            dbCursor.close()
        if dbConnection:
            dbConnection.close()
    except Exception as e:
        dbConnection.commit()
        if dbCursor:
            dbCursor.close()
        if dbConnection:
            dbConnection.close()
        documentssearch_routes.log.error('SELECT from tdocument failed due to {}'.format(e))
        return Response(
            status_code=500,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'SELECT from tdocument failed due to {}'.format(e)
                }
            )

    try:
        dbResultsRows = []
        for row in dbResults:
            d = collections.OrderedDict()
            d['agreementId'] = row[0].decode('utf-8')
            d['businessArea'] = row[1].decode('utf-8')
            d['containsSensitiveData'] = row[2].decode('utf-8')
            d['customerCompanyName'] = row[3].decode('utf-8')
            d['customerFirstName'] = row[4].decode('utf-8')
            d['customerId1'] = row[5].decode('utf-8')
            d['customerId2'] = row[6].decode('utf-8')
            d['customerId3'] = row[7].decode('utf-8')
            d['customerLastName'] = row[8].decode('utf-8')
            d['customerType'] = row[9].decode('utf-8')
            d['descriptionText'] = row[10].decode('utf-8')
            d['documentExpirationDate'] = row[11].decode('utf-8')
            d['documentInternalName'] = row[12].decode('utf-8')
            d['documentName'] = row[13].decode('utf-8')
            d['documentOriginationDate'] = row[14].decode('utf-8')
            d['documentSearchTags'] = row[15].decode('utf-8')
            d['documentSubType'] = row[16].decode('utf-8')
            d['documentType'] = row[17].decode('utf-8')
            d['documentUUId'] = row[18].decode('utf-8')
            d['employeeId'] = row[19].decode('utf-8')
            d['legalHold'] = row[20].decode('utf-8')
            d['orderId'] = row[21].decode('utf-8')
            d['organizationId'] = row[22].decode('utf-8')
            d['productId'] = row[23].decode('utf-8')
            d['rmaId'] = row[24].decode('utf-8')
            d['serviceRequestId'] = row[25].decode('utf-8')
            d['shipmentId'] = row[26].decode('utf-8')
            d['sourceDocumentId'] = row[27].decode('utf-8')
            d['sourceSystem'] = row[28].decode('utf-8')
            d['sourceTransactionAmount'] = row[29].decode('utf-8')
            d['sourceTransactionId'] = row[30].decode('utf-8')
            d['sourceTransactionType'] = row[31].decode('utf-8')
            d['storeId'] = row[32].decode('utf-8')
            d['createdUTCDateTime'] = row[33].decode('utf-8')
            d['updatedUTCDateTime'] = row[34].decode('utf-8')
            d['accessedCount'] = row[35].decode('utf-8')
            d['lastAccessedUTCDateTime'] = row[36].decode('utf-8')
            d['databaseDocumentConsistencyCheck'] = row[37].decode('utf-8')
            dbResultsRows.append(d)
        dbResultsJSON = json.dumps(dbResultsRows, indent=1, default=str)

    except Exception as e:
        return Response(
            status_code=500,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'Could not convert SQL result set to JSON due to {}'.format(e)
                }
            )

    if dbResultsRecordCount is not None \
        and dbResultsRecordCount > 0:
            # 200 OK
            return Response(
                status_code=200,
                headers={'Content-Type': 'application/json'},
                body = dbResultsJSON 
                )
    else:
        # 404 Not Found
        return Response(
            status_code=404,
            headers={'Content-Type': 'application/json'},
            body = {
                }
            )




# END
