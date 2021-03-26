from flask_restplus import reqparse
from server.error import ValueError

def get_args(arg_name, arg_type=str):
	parser = reqparse.RequestParser()
	parser.add_argument(arg_name, type=arg_type)
	args = parser.parse_args()

	arg = args.get(arg_name)

	if arg is None:
		raise ValueError("Miss args: %s" % arg_name)

	return arg
