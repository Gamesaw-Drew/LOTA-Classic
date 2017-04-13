import urlib, zipfile, cStringIIO
gameFiles = urllib.urlopen('http://legendoftheamd.esy.es/gameFiles/lota.zip')
buffer = cStringIO.StringIO(zipWebFile.read())
zfile = zipfile.ZipFile(buffer)
zfile.printdir()