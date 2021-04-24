status_codes = {
	"100": "Success",
	"200": "Error",
	"201": "Missing Information",
	"202": "Not Found"
}

class Response:
	def __init__(self, code, content=""):
		self.code = code
		self.content = content
		self.meaning = status_codes[str(code)]
		self.success = code == 100
		self.json = {"code": code, "content": content, "meaning": self.meaning, "success": self.success}