#!/usr/bin/env python3

import boto3
import time
import sys
import subprocess

# time.sleep(144)
# minmum time to finish 144 seconds; 2 mins 24 seconds

print("""
	############################################################

	Before starting you will need,
		1. Your own Security Group created
			Hint: (Security Group looks like this: sg-056c7d46fd3cf76a3)

		2. Your own Key
			Hint: (Make sure your key is in the same folder
			       of the python and type the Key Name without .pem)

	############################################################
	""")

ContinueStatement = input("Do You Want To Continue? [y/n]")

while ContinueStatement == "y":

	sg = input('Enter your Security Group: ')

	kn = input('Enter your KeyName: ')

	# (1) Creating a ec2 and installation of server
	ec2 = boto3.resource('ec2')

	instance = ec2.create_instances(
	    ImageId='ami-0713f98de93617bb4',
	    MinCount=1,
	    MaxCount=1,
	    InstanceType='t2.nano',
	    SecurityGroupIds=[
	        sg
	    ],
	    KeyName= kn,
	    TagSpecifications=[
	        {
	            'ResourceType': 'instance',
	            'Tags': [
	                {
	                    'Key': 'Name',
	                    'Value': 'Ciaran-Whitty'
	                },
	            ]
	        },
	    ],
	    UserData=""" #!/bin/bash
	                 yum update -y
	                 yum install httpd -y
	                 systemctl enable httpd
	                 systemctl start httpd
	             """)


	print('---please wait, server is starting...')

	time.sleep(10)

	print('---Getting Instance ID...')

	time.sleep(10)

	runninginstance = instance[0].id
	print ('---Instance ID: '+ runninginstance)

	time.sleep(5)

	print ('---Getting IP...')

	time.sleep(10)

	for instance in ec2.instances.all():
	  if(runninginstance == instance.id):
	    instance.wait_until_running()
	    ipinstance = instance.public_ip_address
	    print ('---Instance Ip: ' + ipinstance)

	time.sleep(5)

	print('---Creating Website...')

	# (2) Create a s3 bucket and upload an image to the created Web Server

	s3 = boto3.resource('s3')

	time.sleep(10)

	order66 = 'rm image.jpg'
	subprocess.run(order66, shell=True)
	print('---Deleting image.jpg if it exists')

	object_name = 'image.jpg'

	# Downloads image from s3 bucket
	s3.Bucket('witacsresources').download_file(object_name, 'image.jpg')

	# Creating a s3 Bucket

	bucket_name = '20085909-' + str(time.time())

	try:
	  response = s3.create_bucket(Bucket= bucket_name, ACL = 'public-read', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
	  print (response)
	except Exception as error:
	  print (error)

	# put into bucket

	try:
	  response = s3.Object(bucket_name, object_name).put(Body=open(object_name, 'rb'))
	  object = s3.Bucket(bucket_name).Object(object_name)
	  object.Acl().put(ACL='public-read')
	  
	  print (response)
	except Exception as error:
	  print (error)


	###

	# (3) ssh to server and installing python3 on the server

	print('---Installing Python on Web Server...')

	time.sleep(2)

	python1 = 'ssh -o StrictHostKeyChecking=no -i ' + kn + '.pem ec2-user@' + ipinstance + ' sudo yum install -y python37'
	subprocess.run(python1, shell=True)

	print('---Python is now installed...')

	time.sleep(2)

	###

	# (4) Code to to display image on website

	time.sleep(2)

	print('---Creating webpage file...')

	html_1 = "echo '<html>' > index.html"
	subprocess.run(html_1, shell=True)
	#print('-Debug-html_1')

	# styling index.html

	style1 = "echo '<style> ' >> index.html"
	subprocess.run(style1, shell=True)

	style2 = "echo 'h2 {color:red;} ' >> index.html"
	subprocess.run(style2, shell=True)

	style3 = "echo 'Body {color: darkgreen; font-size: 30px; text-align: center; font-family: sans-serif; } ' >> index.html"
	subprocess.run(style3, shell=True)

	style4 = "echo '</style> ' >> index.html"
	subprocess.run(style4, shell=True)

	# styling index.html

	html_2 = "echo '<h2>Assignment 1 SSD</h2>Instance ID: ' >> index.html"
	subprocess.run(html_2, shell=True)
	#print('-Debug-html_2')

	html_3 = 'ssh -o StrictHostKeyChecking=no -i' + kn + '.pem ec2-user@' + ipinstance + """ curl --silent http://169.254.169.254/latest/meta-data/instance-id/ >> index.html"""
	subprocess.run(html_3, shell=True)
	#print('-Debug-html_3')

	html_4 = "echo '<br>Availability zone:' >> index.html"
	subprocess.run(html_4, shell=True)
	#print('-Debug-html_4')

	html_5 = 'ssh -o StrictHostKeyChecking=no -i ' + kn + '.pem ec2-user@' + ipinstance + """ curl --silent http://169.254.169.254/latest/meta-data/placement/availability-zone/ >> index.html"""
	subprocess.run(html_5, shell=True)
	#print('-Debug-html_5')

	html_6 = "echo '<br>IP address: ' >> index.html"
	subprocess.run(html_6, shell=True)
	#print('-Debug-html_6')

	html_7 = 'ssh -o StrictHostKeyChecking=no -i ' + kn + '.pem ec2-user@' + ipinstance + """ curl http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html"""
	subprocess.run(html_7, shell=True)
	#print('-Debug-html_7')

	html_8 = "echo '<br>Here is the image:<br> ' >> index.html"
	subprocess.run(html_8, shell=True)
	#print('-Debug-html_8')

	html_9 = "echo '<img src=https://s3-eu-west-1.amazonaws.com/'" + bucket_name + "'/image.jpg>' >> index.html"
	subprocess.run(html_9, shell=True)
	#print('-Debug-html_9')

	time.sleep(10)

	print('---Pushing webpage file to instance...')

	time.sleep(10)

	print('---copying index file up now...')

	cmd_1 = 'scp -o StrictHostKeyChecking=no -i ' + kn + '.pem index.html ec2-user@' + ipinstance + ':.'
	subprocess.run(cmd_1, shell=True)
	#print('-Debug-cmd_1')

	time.sleep(60)

##### (Start) loop until server is ready for index file
	#
	#flag = 0
	#while (flag == 0):
    #  for instance in ec2.instances.all():
	#    if(runninginstance == instance.id):
	#      if (instance.describe-instance-status == 10 ):
	#	    cmd_2 = 'ssh -i ' + kn + '.pem ec2-user@' + ipinstance + " sudo cp index.html /var/www/html/index.html"
	#		subprocess.run(cmd_2, shell=True)
	#		print('-Debug-cmd_2')
	#	  else:
	#		time.sleep(10)
	#	
	#print('Now enter this' + ipinstance + 'into your brower! and enjoy the webpage')

    #ContinueStatement = "n"

#print('---Done')

##### (End) loop until server is ready for index file

	cmd_2 = 'ssh -i ' + kn + '.pem ec2-user@' + ipinstance + " sudo cp index.html /var/www/html/index.html"
	subprocess.run(cmd_2, shell=True)
	#print('-Debug-cmd_2')

	print('Now enter this ' + ipinstance + ' into your browser! enjoy the webpage')

	ContinueStatement = "n"


print('---Done')


