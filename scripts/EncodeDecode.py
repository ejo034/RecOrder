import base64
import binascii

def encodeMessage(message):
	encoded = None

	try:
		binaryMessage = message.encode('ascii')
		encoded = base64.b64encode(binaryMessage)

	except binascii.Error:
		return None

	except AttributeError:
		return None

	except TypeError:
		return None

	return encoded


def decodeMessage(message):
	decode = None

	try:
		decodeBinary = base64.b64decode(message)
		decode = decodeBinary.decode('ascii')

	except binascii.Error:
		return None

	except TypeError:
		return None

	return decode