# Document Storage for AWS
# March, 2024
#
# Document Storage for AWS is a freemium accelerator from Seattle Software Works, Inc.
# https://seattleworks.com 
#
# Please see README.md
#



# https://www.ontestautomation.com/writing-tests-for-restful-apis-in-python-using-requests-part-1-basic-tests/ 
# pytests tests.py




import requests
import pytest
import json

SERVERURL = 'http://127.0.0.1:8000/customers/v2/'
PATHTODOCUMENTS = '/Users/petersamson/Download/'




# Heartbeat
def test_heartbeat_ok():
     testmimetype = 'application/json'
     testheaders = {
          'Content-Type': testmimetype,
          'Accept': testmimetype
     }
     response = requests.get(SERVERURL + 'documentsheartbeat', headers=testheaders)
     assert response.status_code == 200

def test_heartbeat_mimetype_bad():
     testmimetype = 'application/xml'
     testheaders = {
          'Content-Type': testmimetype,
          'Accept': testmimetype
     }
     response = requests.get(SERVERURL + 'documentsheartbeat', headers=testheaders)
     assert response.status_code == 415




# Document POST
def test_post_request_mimetype_ok():
     testmimetype = 'application/json'
     testheaders = {
          'Content-Type': testmimetype,
          'Accept': testmimetype
     }
     response = requests.post(SERVERURL + 'documents', headers=testheaders)
     assert response.status_code == 400

def test_post_request_mimetype_bad():
     testmimetype = 'application/xml'
     testheaders = {
          'Content-Type': testmimetype,
          'Accept': testmimetype
     }
     response = requests.post(SERVERURL + 'documents', headers=testheaders)
     assert response.status_code == 415

def test_post_usageMode_bad():
     testmimetype = 'application/json'
     testheaders = {
          'Content-Type': testmimetype,
          'Accept': testmimetype
     }
     testdata = {
          "usageMode": ""
     }
     response = requests.post(SERVERURL + 'documents'
          , data={
               "usageMode": ""
          }
          , headers=testheaders
          )
     assert response.status_code == 400




# Document PATCH
def test_patch_mimetype_ok():
     testmimetype = 'application/json'
     testheaders = {
          'Content-Type': testmimetype,
          'Accept': testmimetype
     }
     response = requests.patch(SERVERURL + 'documents', headers=testheaders)
     assert response.status_code == 400

def test_patch_mimetype_bad():
     testmimetype = 'application/xml'
     testheaders = {
          'Content-Type': testmimetype,
          'Accept': testmimetype
     }
     response = requests.patch(SERVERURL + 'documents', headers=testheaders)
     assert response.status_code == 415




# Document Search (always done as a POST to not have sensitive data in URL)
def test_search_mimetype_ok():
     testmimetype = 'application/json'
     testheaders = {
          'Content-Type': testmimetype,
          'Accept': testmimetype
     }
     response = requests.post(SERVERURL + 'documentssearch', headers=testheaders)
     assert response.status_code == 400

def test_search_mimetype_bad():
     testmimetype = 'application/xml'
     testheaders = {
          'Content-Type': testmimetype,
          'Accept': testmimetype
     }
     response = requests.post(SERVERURL + 'documentssearch', headers=testheaders)
     assert response.status_code == 415




# Document DELETE
def test_delete_mimetype_ok():
     testmimetype = 'application/json'
     testheaders = {
          'Content-Type': testmimetype,
          'Accept': testmimetype
     }
     response = requests.delete(SERVERURL + 'documents', headers=testheaders)
     assert response.status_code == 400

def test_delete_mimetype_bad():
     testmimetype = 'application/xml'
     testheaders = {
          'Content-Type': testmimetype,
          'Accept': testmimetype
     }
     response = requests.delete(SERVERURL + 'documents', headers=testheaders)
     assert response.status_code == 415





# Document PUT (not supported)
def test_put_not_supported():
     testmimetype = 'application/json'
     testheaders = {
          'Content-Type': testmimetype,
          'Accept': testmimetype
     }
     response = requests.put(SERVERURL + 'documents', headers=testheaders)
     assert response.status_code == 405




# END
