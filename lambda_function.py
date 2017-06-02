import tarfile
import requests
import boto3
import os
import PyPDF2 as pypdf2

def lambda_handler(event, context):
    print 'creating archive'
    with tarfile.open('/tmp/files.tar', mode='w') as out:
        out.add('SCWorks.cls')
        out.add('gost780uv.bst')
        out.add('report.tex')

    print 'get generated pdf file'
    with open('/tmp/files.tar', 'rb') as f:
        r = requests.post('https://latexonline.cc/data?target=report.tex&force=true', 
                files={'files.tar': f})
        with open('/tmp/file.pdf', 'wb') as fd:
            for chunk in r.iter_content(2000):
                fd.write(chunk)

    print 'delete pages'
    infile = pypdf2.PdfFileReader('/tmp/file.pdf', 'rb')
    output = pypdf2.PdfFileWriter()
    for i in xrange(infile.getNumPages()):
        p = infile.getPage(i)
        output.addPage(p)
        break
    with open('/tmp/file2.pdf', 'wb') as f:
        output.write(f)

    print 'upload to s3'
    s3 = boto3.resource('s3')
    data = open('/tmp/file2.pdf', 'rb')
    s3.Bucket('ssu-files').put_object(Key='file2.pdf', Body=data,
            ContentType='application/pdf', ACL='public-read')

    #print 'cleanup'
    #os.remove('files.tar')
    #os.remove('file.pdf')
    #os.remove('file2.pdf')

    url = 'https://s3-us-west-1.amazonaws.com/ssu-files/file2.pdf'
    print url
    return url

if __name__ == '__main__':
    lambda_handler(None, None)

