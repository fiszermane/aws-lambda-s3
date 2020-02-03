# aws-lambda-s3
This is another S3->Textract->S3 sample. I struggled so much to find online information so I am publishing mine.
I took the code from multiple pages I found online and made some adjustments so it can fit this use case.

# Requires
-> S3 Bucket - Input
-> Textract
-> S3 Bucket - Output

# What does this do
Code will execute once an object is uploaded to the Input S3, run Textract and return a .JSON in the Output S3.
