# Document Storage for AWS
#
# Document Storage for AWS is a freemium accelerator from Seattle Software Works, Inc.
# https://seattleworks.com 
#
# Please see README.md
#



import psycopg
import sys
import boto3
import os
import datetime
import uuid
import re




def GetGlobalVariables():
# Notes
# S3 Region Name.  e.g. 'us-east-1'
# S3 Server Side Encryption 'AES256' is recommended as a minimum.  Or, review boto3 documentation and enhance code to use your own key.

    S3BUCKETNAME = 'sswdocumentstorage'
    S3REGIONNAME = 'us-east-1'
    S3SERVERSIDEENCRYPTION = 'AES256'

    return (S3BUCKETNAME, S3REGIONNAME, S3SERVERSIDEENCRYPTION)




def CheckContainsSQLWildcard(searchStr):
# Notes
# Returns TRUE if percent (%) in string.
# Assumes any asterisk (*) has already been transformed to percent (%).

    if searchStr is not None \
        and searchStr != '' \
        and re.search("\%", searchStr):
            return True
    else:
        return False




def CheckContainsWildcard(searchStr):
# Notes
# Returns TRUE if asterisk (*) or percent (%) in string

    if searchStr is not None \
        and searchStr != '' \
        and re.search("\*\%", searchStr):
            return True
    else:
        return False




def CheckDateEarlier(dateStr1, dateStr2):
# Notes
# Both dates are assumed to be passed as strings in format of YYYY-MM-DD.
# date1 should be earlier than date2.

    if dateStr1 is not None \
        and len(dateStr1) == 10 \
        and dateStr2 is not None \
        and len(dateStr2) == 10:
            try:
                dateYear1, dateMonth1, dateDay1 = dateStr1.split('-')
                date1 = datetime.datetime(int(dateYear1), int(dateMonth1), int(dateDay1))
                dateYear2, dateMonth2, dateDay2 = dateStr2.split('-')
                date2 = datetime.datetime(int(dateYear2), int(dateMonth2), int(dateDay2))
                if date1 < date2:
                    return True
                else:
                    return False
            except:
                return False
    else:
        return False




def CheckValidAmount(amountNbr):
# Notes
# Remove related characters that may have been passed.
# If needed, append a decimal place and two digits to keep the subsequent regex simple.
# Confirm Amount is numeric, to a maximum of two decimal places, and greater than zero.

    if amountNbr is not None \
        and amountNbr != '':
            amountNbr = amountNbr.replace('$','')
            amountNbr = amountNbr.replace(',','')
            amountNbr = amountNbr.replace('-','')
            amountNbr = amountNbr.replace('(','')
            amountNbr = amountNbr.replace(')','')

            decimalPlace = amountNbr.rfind('.')
            if decimalPlace is None \
                or decimalPlace < 1:
                    amountNbr = amountNbr + '.00'

            if re.match("^\d+\.\d{0,2}$$", amountNbr) \
                and float(amountNbr) > 0.00:
                    return True
            else:
                return False
    else:
        return False




def CheckValidUUId(documentUUId):
# Notes
# Only lower-case characters or dashes (-), 36 characters in length, and four dashes in expected positions.
# e.g. e3372709-8e0e-414b-96e8-89f6d797059f

    if documentUUId is not None \
        and re.match("^[a-z0-9\-]{36}$", documentUUId) \
        and documentUUId[8] == '-' \
        and documentUUId[13] == '-' \
        and documentUUId[18] == '-' \
        and documentUUId[23] == '-':
            return True
    else:
        return False




def CheckValidDate(dateStr):
# Notes
# Confirm Date is valid based on the required format of YYYY-MM-DD

    if dateStr is not None \
        and len(dateStr) == 10:
        try:
            dateYear, dateMonth, dateDay = dateStr.split('-')
            datetime.datetime(int(dateYear), int(dateMonth), int(dateDay))
            return True
        except:
            return False
    else:
        return False




def CheckValidUserType(userType):
# Notes
# If changing the permissible values, then change error/400 messages elsewhere in the code where function is used.

    if userType is not None \
        and (userType == 'CUSTOMER' \
        or userType == 'EMPLOYEE' \
        or userType == 'MIGRATION' \
        or userType == 'SYSTEM'):
        return True
    else:
        return False




def CreateDBConnection():
# Notes
# Create a database connection

# Dev Notes
# fix process to get and use a token

    ENDPOINT="documentstoragepostgresql.cluster-covgueplbahh.us-east-1.rds.amazonaws.com"
    PORT="5432"
    USER="sswdba"
    REGION="us-east-1"
    DBNAME="documentstorage"
    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

    # Gets the credentials from .aws/credentials
    #session = boto3.Session(profile_name='default')
    #client = session.client('rds')

    #token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)
    token="SOMEVALUE"

    try:
        # dbConnection = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca='SSLCERTIFICATE')
        # dbConnection = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME)
        dbConnection = psycopg.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME)
        dbConnection.autocommit = False
        return (dbConnection, 'OK')
    except Exception as e:
        return (None, 'Database connection failed due to {}'.format(e))




def CreateUUId():
# Notes
# Generate a 36-character UUId.  e.g. e3372709-8e0e-414b-96e8-89f6d797059f
# Verify documentUUId layout before returning it.
# Only lower-case characters or dashes (-), 36 characters in length, and four dashes in expected positions.

    try:
        documentUUId = str(uuid.uuid4())
        documentUUId = documentUUId.strip()
        documentUUId = documentUUId.lower()
    except:
        return None

    if documentUUId is not None \
        and len(documentUUId) == 36 \
        and re.match("^[a-z0-9\-]{36}$", documentUUId) \
        and documentUUId[8] == '-' \
        and documentUUId[13] == '-' \
        and documentUUId[18] == '-' \
        and documentUUId[23] == '-':
            return documentUUId
    else:
        return None




def GetCurrentUTCDateTime():
# Notes
# Returns YYYY-MM-DD HH:MM:SS in UTC
# Intentionally discards any microseconds (ie., .654321)

    try:
        currentDateTimeFull = datetime.datetime.utcnow()
        currentDateTime = currentDateTimeFull.strftime("%Y-%m-%d %H:%M:%S")
        currentDateTime = currentDateTime.strip()
    except:
        return None

    if currentDateTime is not None \
        and len(currentDateTime) == 19:
            return currentDateTime
    else:
        return None




def TransformWildcards(searchStr):
# Notes
# Transform any occurences of * to % for SQL compatibility
# Transform any occurrences of %%%%%, %%%%, %%% or %% to a single percent (%) character.
# Avoid occurrences of 2+ percent (%) characters to ensure expected behavior of SQL statements

    if searchStr is not None \
        and searchStr != '':
        try:
            searchStrTransformed = searchStrTransformed.replace('*','%')
            searchStrTransformed = searchStrTransformed.replace('\%\%\%\%\%','%')
            searchStrTransformed = searchStrTransformed.replace('\%\%\%\%','%')
            searchStrTransformed = searchStrTransformed.replace('\%\%\%','%')
            searchStrTransformed = searchStrTransformed.replace('\%\%','%')
        except:
            return searchStr

    return searchStrTransformed




# END
