import easywebdav

webdav = easywebdav.connect('lennydune.stackstorage.com',
	username='tomsbroer',
	password='tomsbroer123',
	protocol='https',
	port=443,
	path='remote.php/webdav/',
	verify_ssl=True)

webdav.upload('triangulation.py', 'triangulation.py')