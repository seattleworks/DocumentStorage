DocumentStorage v1.1

Document Storage for AWS is a freemium accelerator from Seattle Software Works, Inc.
https://seattleworks.com 
seattle.software.works at gmail

You agree that:
  1. You represent your organization when reviewing and inherently agreeing to these conditions.
  2. You are using this software for your organization.
  3. You will not redistribute or sell this software in any way or any form.
  4. You will leave this entire comment block in this software to fairly attribute this software to Seattle Software Works, Inc.
  5. There is no warranty for this software from Seattle Software Works, Inc.
  6. If we publish enhancements to this software the burden is on your organization to upgrade your code.

Seattle Software Works, Inc. agrees that:
  1. You may use and modify this software for your organization so long as you comply with conditions 1 through 6 above.



Overview:
Document Storage is a repository for documents and associated meta data.  The API's may be utilized in your existing application(s).
It is assumed your organization has other solutions for document templates and document generation.

What to know:
- The accelerator uses a S3 bucket for documents, and two PostgreSQL tables for the meta data (lower operational costs than MongoDB!)
  and audit log.  The meta-data table is 'flat' for simplicity and performance.
- Add your preferred method to secure the API's.
- It is possible to use your organization's key for S3 server-side encryption.
- The accelerator timestamps are generated and saved in UTC.
- The original file name is stored in the meta data, and the file is stored in S3 using the UUID as the file name to ensure uniqueness.
- In /documentssearch the predicates in the WHERE use parameters to mitigate the risk of SQL injection.
- We recommend separate implementations based on types of documents (e.g. Customer, Employee, Product/Sales) to maximize security.

What to review and potentially change:
- Data Model and Indexes.
- In /documents remove the DELETE method for more control (e.g. create a scheduled process to delete).
- In /documentssearch review UsageMode and expected parameters for each (ie., ensure good performance using a high-cardinality parameter).
- In /documents POST review and adjust validExtensionNames for documents (e.g. your organization might only want PDF documents).
- In /documents POST the S3 folder structure is set as part of documentInternalName, but make changes before go-live for consistency.
- In /documents POST additional file tags may be added to the document as part of s3FileTags.  These may be useful for S3 reporting.
- In /documents POST the s3StorageClass should be reviewed.  You might further configure a S3 rule to lower the Storage Class after N days.
- Use /documentsvolumeload to insert random records into the meta-data table, and then test search performance for your configured
  data model and indexes.  10,000+ rows should help identify performance concerns.  After loading random records, remember to
  defragment/rebuild indexes and update table statistics to provide a good baseline.

Implementation considerations:
- Anything consuming /documentssearch must provide a usageMode (e.g. CARE, CUSTOMER) to validate minimum parameters.
- Once implemented in Production you might start converting existing documents well in advance of go-live.
- S3 should auto-delete documents after the stated expiration date, except if legalHold = Y.

What isn't here but might get added in time:
- A batch/scheduled process to delete documents where documentExpirationDate < utcnow().
- Test coverage.

END
