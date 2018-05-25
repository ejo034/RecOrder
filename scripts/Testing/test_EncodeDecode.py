import unittest
import binascii
from v2.scripts import EncodeDecode

class EncodeDecodeTesting(unittest.TestCase):

	#TESTING ENCODING

	def testEncodeTrue(self):
		message = "hello world"
		encoded = EncodeDecode.encodeMessage(message)
		encodedTrue = b'aGVsbG8gd29ybGQ='
		self.assertEqual(encoded, encodedTrue)

	def testEncodeFalse(self):
		message = "hello world"
		encoded = EncodeDecode.encodeMessage(message)
		encodedFalse = b'hello world'
		self.assertNotEqual(encoded, encodedFalse)

	def testEncodeWrongInput(self):
		message = 1
		encode = EncodeDecode.encodeMessage(message)
		self.assertEqual(encode, None)


	#TESTING DECODING

	def testDecodeTrue(self):
		message = b'aGVsbG8gd29ybGQ='
		decode = EncodeDecode.decodeMessage(message)
		decodedTrue = "hello world"
		self.assertEqual(decode, decodedTrue)


	def testDecodeFalse(self):
		message = b'bGVsbG8gd29ybGQ=='
		decode = EncodeDecode.decodeMessage(message)
		decodedTrue = "hello world"
		self.assertNotEqual(decode, decodedTrue)


	def testDecodeWrongInput(self):
		message = 1
		decode = EncodeDecode.decodeMessage(message)

		self.assertEqual(decode, None)




if __name__ == '__main__':
	unittest.main()