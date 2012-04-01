def extractVideoCode(rawUrl):
	length = len(rawUrl)
	start = -1
	start = rawUrl.find('v=')
	if start >= 0 :
		start += 2
		end = rawUrl[start:length].find('&')
		if end < 0 :
			end = length
		else
			end += start
		videoCode = rawUrl[start:end]
		return videoCode
	else
		return -1
