DocumentStorage v1.1

Document Storage for AWS is a freemium accelerator from Seattle Software Works, Inc.
https://seattleworks.com 

You agree that:
  1. You represent your organization when reviewing and inherently agreeing to these conditions.
  2. You are using this software for your organization.
  3. You will not redistribute or sell this software in any way or any form.
  4. You will leave this entire comment block in this software to fairly attribute this software to Seattle Software Works, Inc.
  5. There is no warranty for this software from Seattle Software Works, Inc.
  6. If we publish enhancements to this software the burden is on your organization to upgrade your code.

Seattle Software Works, Inc. agrees that:
  1. You may use and modify this software for your organization so long as you comply with conditions 1 through 6 above.



What to know
- The accelerator uses a S3 bucket for documents and two PostgreSQL tables for the meta data (cheaper to run than MongoDB?!).
- Add your preferred method and code to secure the API's.
- We recommend separate implementations for documents (e.g. Customer, Employee, Product/Sales) to maximize security.

What to review and change
- It is possible to use your own key for S3 server-side encryption.
- Data Model and Indexes.
- Accelerator timestamps are generated and saved in UTC.
- In /documents remove the DELETE method for more control (e.g. scheduled process).
- In /documentssearch review UsageMode and expected parameters for each (ie., ensure good performance using a high-cardinality parameter).
- In /documents POST the S3 folder structure may be changed as part of documentInternalName, but do this before go-live for consistency.
- In /documents POST additional file tags may be added to the document as part of s3FileTags.

Implementation considerations
- The UI's accessing /documentssearch must provide a usageMode (e.g. CARE, CUSTOMER) to ensure passed parameters and performance.
- Once implemented in Production you could start converting existing documents well in advance of go-live.
- S3 should auto-delete documents after the stated expiration date, except if legalHold = Y.

END
