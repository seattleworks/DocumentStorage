# Document Storage for AWS
# March, 2024
#
# Document Storage for AWS is a freemium accelerator from Seattle Software Works, Inc.
# https://seattleworks.com 
#
# Please see README.md
#



NUMBERROWS = 7500



from chalice import Blueprint, Response

from chalicelib.common import CheckValidAmount, CheckValidDate, CheckValidUUId, CreateDBConnection, CreateUUId, GetCurrentUTCDateTime

import sys
import boto3
import io
import os
import re
import random

from boto3.s3.transfer import S3UploadFailedError
from botocore.exceptions import ClientError

volumeload_routes = Blueprint(__name__)




@volumeload_routes.route('/customers/v2/documentsvolumeload', methods=['POST'], content_types=['application/json'], cors=False)
# Notes
# - Loads the database table but not any binary documents.
# - Randomly generate some attributes

def volumeload():

    (dbConnection, errorMessage) = CreateDBConnection()
    if dbConnection is None \
        or errorMessage != 'OK':
        volumeload_routes.log.error('Could not create Database Connection.  ' + errorMessage)
        return Response(
            status_code=500,
            headers={'Content-Type': 'application/json'},
            body = {
                'message': 'Could not create Database Connection.  ' + errorMessage
                }
            )

    loopcounter = 0
    while loopcounter < NUMBERROWS:

        documentUUId = CreateUUId()
        if documentUUId is None:
            volumeload_routes.log.error("Could not generate a new documentUUId.")
            return Response(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Could not generate a new documentUUId.'
                    }
                )

        currentUTCDateTime = GetCurrentUTCDateTime()
        if currentUTCDateTime is None:
            volumeload_routes.log.error("Could not generate a current UTC DateTime.")
            return Response(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'Could not generate a current UTC DateTime.'
                    }
                )

        # system-related attributes
        createdUTCDateTime = currentUTCDateTime
        updatedUTCDateTime = currentUTCDateTime
        accessedCount = 0
        lastAccessedUTCDateTime = None
        databaseDocumentConsistencyCheck = 'OK'

        if int(currentUTCDateTime[17:19]) > 55:
            agreementId = str(random.randint(1000,9999))
        else:
            agreementId = None

        randomNumber = random.randint(1,10)
        if randomNumber == 1:
            businessArea =  'Legal'
        elif randomNumber == 2:
            businessArea =  'Finance'
        elif randomNumber == 3:
            businessArea =  'Care'
        elif randomNumber == 4:
            businessArea =  'Retail'
        elif randomNumber == 5:
            businessArea =  'Dealer'
        elif randomNumber == 6:
            businessArea =  'Telesales'
        elif randomNumber == 7:
            businessArea =  'Credit'
        else:
            businessArea = None

        if int(currentUTCDateTime[17:19]) >= 45:
            containsSensitiveData = 'Y'
        else:
            containsSensitiveData = 'N'

        customerCompanyName = str(random.randint(10000,99999)) + 'Company'

        customerFirstName = str(random.randint(100,999)) + 'Peter'

        customerId1 = str(random.randint(1000,9999))

        customerId2 = None

        customerId3 = None

        customerLastName = str(random.randint(100,999)) + 'son'

        customerType = str(random.randint(100,999)) + 'Type'

        descriptionText = None

        documentExpirationDate = '2022-' + str(random.randint(7,12)) + '-' + str(random.randint(1,28))

        documentName = 'x.pdf'

        documentOriginationDate = str(random.randint(2012,2021)) + '-' + str(random.randint(1,12)) + '-' + str(random.randint(1,28))

        documentSearchTags = None
 
        documentSubType = None

        documentType = str(random.randint(11,29)) + 'Type'

        employeeId = str(random.randint(1000,99999))

        if int(currentUTCDateTime[17:19]) >= 57:
            legalHoldIndicator = 'Y'
        else:
            legalHoldIndicator = 'N'

        if int(currentUTCDateTime[17:19]) > 55:
            orderId = str(random.randint(1000,9999))
        else:
            orderId = None

        if int(currentUTCDateTime[17:19]) > 55:
            organizationId = str(random.randint(1,9))
        else:
            organizationId = None

        if int(currentUTCDateTime[17:19]) > 55:
            productId = str(random.randint(100,999))
        else:
            productId = None

        if int(currentUTCDateTime[17:19]) > 55:
            rmaId = 'RMA' + str(random.randint(1000,9999))
        else:
            rmaId = None

        if int(currentUTCDateTime[17:19]) > 55:
            serviceRequestId = str(random.randint(100000,999999))
        else:
            serviceRequestId = None

        if int(currentUTCDateTime[17:19]) > 55:
            shipmentId = str(random.randint(1000,9999))
        else:
            shipmentId = None

        if int(currentUTCDateTime[17:19]) > 55:
            sourceDocumentId = str(random.randint(1000,9999))
        else:
            sourceDocumentId = None

        sourceSystem = None

        sourceTransactionAmount = None

        if int(currentUTCDateTime[17:19]) > 55:
            sourceTransactionId = str(random.randint(1000,9999))
        else:
            sourceTransactionId = None

        sourceTransactionType = None

        if int(currentUTCDateTime[17:19]) > 55:
            storeId = str(random.randint(1000,9999)) + ' Store'
        else:
            storeId = None

        documentInternalName = documentType + '/' + documentOriginationDate[0:7] + '/' + documentUUId + '.pdf'
            
        sqlStatement = 'insert into tdocument ' \
            + '( agreementId ' \
            + ', businessArea ' \
            + ', containsSensitiveData ' \
            + ', CustomerCompanyName ' \
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
            + ', legalHoldIndicator ' \
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
            , documentName \
            , documentOriginationDate \
            , documentSearchTags \
            , documentSubType \
            , documentType \
            , documentUUId \
            , employeeId \
            , legalHoldIndicator \
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
            volumeload_routes.log.error('INSERT into tdocument failed due to {}'.format(e))
            return Response(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'INSERT into tdocument failed due to {}'.format(e),
                    'documentName': documentName                    }
                )

        # Add a POST record to the Audit Log
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
        userId = None
        userType = 'SYSTEM'
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
            volumeload_routes.log.error('INSERT into tdocument_auditlog failed due to {}'.format(e))
            return Response(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body = {
                    'message': 'INSERT into tdocument_auditlog failed due to {}'.format(e),
                    'documentName': documentName                    }
                )

        # Add a GET record to the Audit Log once in a while
        if int(currentUTCDateTime[17:19]) > 45:
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
            if int(currentUTCDateTime[17:19]) > 55:
                userId = customerId1
                userType = 'EMPLOYEE'
            if int(currentUTCDateTime[17:19]) > 50:
                userId = customerId1
                userType = 'CUSTOMER'
            else:
                userId = employeeId
                userType = 'CARE'
            sqlArguments = \
                  documentUUId \
                , createdUTCDateTime \
                , 'GET' \
                , userId \
                , userType
            dbCursor = dbConnection.cursor(prepared=True)
            try:
                dbCursor.execute(sqlStatement,sqlArguments)
                dbConnection.commit()
            except Exception as e:
                dbConnection.rollback()
                volumeload_routes.log.error('INSERT into tdocument_auditlog failed due to {}'.format(e))
                return Response(
                    status_code=500,
                    headers={'Content-Type': 'application/json'},
                    body = {
                        'message': 'INSERT into tdocument_auditlog failed due to {}'.format(e),
                        'documentName': documentName                    }
                    )

        loopcounter += 1

        # END LOOP

    if dbConnection:
        dbConnection.close()

    return Response(
        status_code=201,
        headers={'Content-Type': 'application/json'},
        body = {
            }
        )




# END
