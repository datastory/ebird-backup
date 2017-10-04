# Automatic backup of lists from [eBird](http://ebird.org/) to S3
Script for Amazon Lambda, which backs up all your lists to S3.

Before uploading to Lambda its necessary to install

- **requests** library by running  `pip install requests -t ./` 
- **BeautifulSoup** library by running  `pip install beautifulsoup4 -t ./` 

in repo home, fill out your eBird login (not e-mail), bucket name and eBird password in `credentials.py`.

After all you have to [ZIP whole repo and upload it to Lambda](http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html).


Function needs [approval for writing to S3](http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-create-iam-role.html) and [trigger, which runs it](http://docs.aws.amazon.com/lambda/latest/dg/with-scheduled-events.html).

If you have problems with Lambda´s role settings, [follow this](https://stackoverflow.com/questions/38774798/accessdenied-for-listobjects-for-s3-bucket-when-permissions-are-s3).