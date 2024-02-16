from config import FUNC_DELIMITER
import sys
import pickle
import base64
'''
This file serve as a template file to run invokee functions
#!DO NOT MODIFY THIS FILE!
'''

def main():
    return_signature = f'#function-return: {FUNC_DELIMITER}'
    params = sys.argv[1]
    decoded_params = pickle.loads(base64.b64decode(params))
    result = func(*decoded_params)
    print(f'{return_signature}')
    print(base64.b64encode(pickle.dumps(result)).decode()) # func's return value

#start-function: KEYPHRASE
#end-function: KEYPHRASE

if __name__ == "__main__":
    main()
