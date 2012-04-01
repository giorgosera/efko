def extractVideoCode(rawUrl):
	length = len(rawUrl)
	start = rawUrl.find('v=') + 2
	end = rawUrl[start:length].find('&')
	videoCode = rawUrl[start:end]
	return videoCode
