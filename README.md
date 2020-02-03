# aws-lambda-s3
This is another S3->Textract->S3 sample. I struggled so much to find online information so I am publishing mine. Perhaps it may help someone. I took the code from multiple pages I found online and made some adjustments so it can fit this use case.

Some pages like this one (https://rpadovani.com/aws-textract) where incredibly helpful. This was another one (https://auxenta.com/blog_aws_textract_with_lambda_walkthrough.php). There are a ton others so I'm sorry if you recognize your code and is not credited. Let me know and I will add this.

# Requires
-> S3 Bucket - Input
-> Textract
-> S3 Bucket - Output

# What does this do
Code will execute once an object is uploaded to the Input S3, run Textract and return a .JSON in the Output S3.
It is designed to recognize a PDF and transform it to JSON. From there it can only be done much better.
Many of the examples I've seen had an overload of Lambda Functions, SNS Topics and so many building blocks that were confusing to me as a newbie to AWS Cloud. I managed to achieve my objectives with much less than what I found online - it's likely less robust but it did serve my purposes quite well.

# Steps

1. Create an AWS account.
2. Create two S3 buckets. One for input, one for output.
3. Go to Lambda and create a standard function with standard IAM permissions.
4. Go to the IAM console.
5. Give the IAM profile access to S3, SNS [if needed] and Textract. You can tighten up permissions and be much more precise with Read/Write capabilities for this Lambda function profile.
6. You can go to Cloud Watch and tie up this Lambda function so that you can track the program.
7. As destination you can use your SNS topic and set it up for some alerts in case of Failure/Success. The logs for CloudWatch will contain everything.
8. Create & enable your S3 with the right ARN as a trigger.
9. The Destination S3 is only referenced in the code and will not show up.
10. You can enable the function and try it. I cannot remember having a valid test case for these.

# TODOs
- Tutorial to come later.
- Detect if the file is PDF.
- Define business rules for the specific PDFs uploaded
