from logic.signature import get_return_signature
import sys
import pickle
import base64
'''
This file serve as a template file to run invokee functions
'''
#!DO NOT MODIFY THIS FILE!

# Call invokee function here


def invoker() -> None:
    params = sys.argv[1]
    decoded_params = pickle.loads(base64.b64decode(params))
    result = func(*decoded_params)
    # return signature, separate std output with return value
    print(get_return_signature())
    print(base64.b64encode(pickle.dumps(result)).decode())  # func's return value

# start-function: KEYPHRASE
# end-function: KEYPHRASE


if __name__ == "__main__":
    invoker()
