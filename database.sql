# Document Storage for AWS
# July, 2022
#
# Document Storage for AWS is a freemium accelerator from Seattle Software Works, Inc.
# https://seattleworks.com 
#
# Download the Installation Guide from our website.  Learn about our related consulting services for this free accelerator.
#
# You agree that:
#   1. You are using this software for your organization.
#   2. You will not take the software and attempt to redistribute it.
#   3. You will leave this comment block in the software to fairly attribute the source to Seattle Software Works, Inc.
#   4. There is no warranty for this software from Seattle Software Works, Inc.
#
# Seattle Software Works, Inc. agrees that:
#   1. You may freely use and modify this software for your organization.
#   2. ?
#




-- Create Database

-- Use caution if uncommenting this first SQL statement since it will immediately drop the database, all objects, and all data.
-- drop database if exists documentstorage;
commit;

-- UTF8 character set chosen so as to support more than Western European characters.
CREATE DATABASE IF NOT EXISTS documentstorage
    WITH
    OWNER = sswdba
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
commit;




-- Create Tables

CREATE TABLE IF NOT EXISTS public.tdocument
(
    documentUUId character(36) COLLATE pg_catalog.default NOT NULL,
    agreementId character varying(255) COLLATE pg_catalog.default NULL,
    businessArea character varying(255) COLLATE pg_catalog.default NULL,
    containsSensitiveData character(1) COLLATE pg_catalog.default NOT NULL,
    customerCompanyName character varying(255) COLLATE pg_catalog.default NULL,
    customerFirstName character varying(255) COLLATE pg_catalog.default NULL,
    customerId1 character varying(255) COLLATE pg_catalog.default NULL,
    customerId2 character varying(255) COLLATE pg_catalog.default NULL,
    customerId3 character varying(255) COLLATE pg_catalog.default NULL,
    customerLastName character varying(255) COLLATE pg_catalog.default NULL,
    customerType character varying(255) COLLATE pg_catalog.default NULL,
    descriptionText character varying(2000) COLLATE pg_catalog.default NULL,
    documentExpirationDate date NOT NULL,
    documentInternalName character varying(255) COLLATE pg_catalog.default NOT NULL,
    documentName character varying(500) COLLATE pg_catalog.default NOT NULL,
    documentOriginationDate date NOT NULL,
    documentSearchTags character varying(255) COLLATE pg_catalog.default NULL,
    documentSubType character varying(255) COLLATE pg_catalog.default NULL,
    documentType character varying(255) COLLATE pg_catalog.default NOT NULL,
    employeeId character varying(255) COLLATE pg_catalog.default NULL,
    legalHold character(1) COLLATE pg_catalog.default NOT NULL,
    orderId character varying(255) COLLATE pg_catalog.default NULL,
    organizationId character varying(255) COLLATE pg_catalog.default NULL,
    productId character varying(255) COLLATE pg_catalog.default NULL,
    rmaId character varying(255) COLLATE pg_catalog.default NULL,
    serviceRequestId character varying(255) COLLATE pg_catalog.default NULL,
    shipmentId character varying(255) COLLATE pg_catalog.default NULL,
    sourceDocumentId character varying(255) COLLATE pg_catalog.default NULL,
    sourceSystem character varying(255) COLLATE pg_catalog.default NULL,
    sourceTransactionAmount numeric(25,2) NULL,
    sourceTransactionId character varying(255) COLLATE pg_catalog.default NULL,
    sourceTransactionType character varying(255) COLLATE pg_catalog.default NULL,
    storeId character varying(255) COLLATE pg_catalog.default NULL,
    createdUTCDateTime timestamp without time zone NOT NULL,
    updatedUTCDateTime timestamp without time zone NOT NULL,
    accessedCount integer NOT NULL,
    lastAccessedUTCDateTime timestamp without time zone NULL,
    databaseDocumentConsistencyCheck character varying(255) COLLATE pg_catalog.default NOT NULL
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tdocument
    OWNER to sswdba;
commit;

CREATE UNIQUE INDEX IF NOT EXISTS documentUUId
    ON public.tdocument USING btree
    (documentUUId COLLATE pg_catalog.default ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

ALTER TABLE IF EXISTS public.tdocument
    CLUSTER ON documentUUId;
commit;




CREATE TABLE IF NOT EXISTS public.tdocument_auditlog
(
    documentUUId character(36) COLLATE pg_catalog.default NOT NULL,
    createdUTCDateTime timestamp without time zone NOT NULL,
    accessType character varying(255) COLLATE pg_catalog.default NOT NULL,
    userId character varying(255) COLLATE pg_catalog.default NULL,
    userType character varying(255) COLLATE pg_catalog.default NULL
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tdocument_auditlog
    OWNER to sswdba;
commit;

CREATE UNIQUE INDEX IF NOT EXISTS documentUUId_AuditLog
    ON public.tdocument_auditlog USING btree
    (documentUUId COLLATE pg_catalog.default ASC NULLS LAST,
     accessType COLLATE pg_catalog.default ASC NULLS LAST,
     createdUTCDateTime ASC NULLS LAST
    )
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

ALTER TABLE IF EXISTS public.tdocument_auditlog
    CLUSTER ON documentUUId_AuditLog;
commit;

CREATE UNIQUE INDEX IF NOT EXISTS createdUTCDateTime_AuditLog
    ON public.tdocument_auditlog USING btree
    (createdUTCDateTime ASC NULLS LAST,
     accessType COLLATE pg_catalog.default ASC NULLS LAST,
     documentUUId COLLATE pg_catalog.default ASC NULLS LAST
    )
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX IF NOT EXISTS userId_AuditLog
    ON public.tdocument_auditlog USING btree
    (userId COLLATE pg_catalog.default ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;




-- Once any data migration is complete, selectively add additional non-unique Indexes based on your requirements.

CREATE INDEX IF NOT EXISTS agreementId
    ON public.tdocument USING btree
    (agreementId COLLATE pg_catalog.default ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX IF NOT EXISTS customerCompanyName
    ON public.tdocument USING btree
    (customerCompanyName COLLATE pg_catalog.default ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX IF NOT EXISTS customerId1
    ON public.tdocument USING btree
    (customerId1 COLLATE pg_catalog.default ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX IF NOT EXISTS customerId2
    ON public.tdocument USING btree
    (customerId2 COLLATE pg_catalog.default ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX IF NOT EXISTS customerId3
    ON public.tdocument USING btree
    (customerId3 COLLATE pg_catalog.default ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX IF NOT EXISTS customerLastName
    ON public.tdocument USING btree
    (customerLastName COLLATE pg_catalog.default ASC NULLS LAST,
     customerFirstName COLLATE pg_catalog.default ASC NULLS LAST
    )
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX employeeId
    ON public.tdocument USING btree
    (employeeId ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX orderId
    ON public.tdocument USING btree
    (orderId ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX productId
    ON public.tdocument USING btree
    (productId ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX rmaId
    ON public.tdocument USING btree
    (rmaId ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX serviceRequestId
    ON public.tdocument USING btree
    (serviceRequestId ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX shipmentId
    ON public.tdocument USING btree
    (shipmentId ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX sourceDocumentId
    ON public.tdocument USING btree
    (sourceDocumentId ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX sourceTransactionId
    ON public.tdocument USING btree
    (sourceTransactionId ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;

CREATE INDEX storeId
    ON public.tdocument USING btree
    (storeId ASC NULLS LAST)
    WITH (FILLFACTOR=85)
    TABLESPACE pg_default;
commit;




REINDEX TABLE CONCURRENTLY tdocument;
ANALYZE VERBOSE tdocument;

REINDEX TABLE CONCURRENTLY tdocument_auditlog;
ANALYZE VERBOSE tdocument_auditlog;




-- working SQL, remove later

-- need to verify this works as expected in Postgres
update tdocument as d
set (documentUUId, accessedCount, lastAccessedUTCDateTime) =
(select a.documentUUId
, count(1)
, max(createdUTCDateTime)
from tdocument_auditlog as a
where a.accessType = 'GET'
group by a.documentUUId
having a.documentUUId in
(
  select ar.documentUUId
  from tdocument_auditlog as ar
  where ar.createdUTCDateTime >= (current_date - integer '14')
  and ar.accessType = 'GET'
)
where a.documentUUId = d.documentUUId
);

# END 
