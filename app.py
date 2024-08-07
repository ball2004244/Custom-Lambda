from fastapi import FastAPI, APIRouter, responses
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from logic.funcs import get_funcs, add_func, invoke_func, modify_func, delete_func
from logic.libs import install_libs, get_libs, install_on_startup
from models import GetUserFuncsRequest, CreateFuncRequest, ExecFuncRequest, ModifyFuncRequest, DelFuncRequest, LibInstallRequest
from utils import create_dir
from config import FUNC_STORE, CONF_STORE

# Initialize directories
create_dir(FUNC_STORE)
create_dir(CONF_STORE)

install_on_startup(f'{CONF_STORE}/cloud_requirements.txt')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# frontend static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# router for the API endpoints
router = APIRouter(prefix="/api")

RESPONSE_TEMPLATE = {
    'status': 'error',
    'message': 'An error occurred',
    'data': None
}


@app.get("/")
def root_redirect() -> responses.RedirectResponse:
    '''
    Redirect to the frontend
    '''
    return responses.RedirectResponse(url='/static/index.html')


@router.get("/")
def read_root() -> dict:
    '''
    Welcome message
    '''
    res = RESPONSE_TEMPLATE.copy()
    try:
        res['status'] = 'success'
        res['message'] = 'Welcome to the CustomLambda API'
    except Exception as e:
        res['message'] = str(e)
    finally:
        return res


@router.get("/admin/functions")
def get_all_funcs() -> dict:
    '''
    Get all serverless functions from functions_store
    '''
    res = RESPONSE_TEMPLATE.copy()
    try:
        all_funcs = get_funcs(target_dir='functions_store')

        if all_funcs is None:
            raise Exception('No functions found')

        res['data'] = {
            'total': len(list(all_funcs.values())[0]),
            'functions': all_funcs
        }
        res['status'] = 'success'
        res['message'] = 'All functions retrieved successfully'
    except Exception as e:
        res['message'] = str(e)
    finally:
        return res


@router.get("/admin/functions/{func_name}")
def get_func(func_name: str) -> dict:
    '''
    Get a specific serverless function from functions_store
    Permission: ADMIN
    '''
    res = RESPONSE_TEMPLATE.copy()
    try:

        all_funcs = get_funcs(target_dir='functions_store')
        if func_name not in all_funcs:
            raise Exception('Function not found')

        res['data'] = {
            'function': func_name
        }
        res['status'] = 'success'
        res['message'] = f'Successfully retrieved function {func_name}'
    except Exception as e:
        res['message'] = str(e)
    finally:
        return res

@router.post("/users/functions")
def get_user_funcs(get_request: GetUserFuncsRequest) -> dict:
    '''
    Get all serverless functions from functions_store
    Permission: Normal USER
    '''
    res = RESPONSE_TEMPLATE.copy()
    try:
        all_funcs = get_funcs(target_dir='functions_store', author=get_request.username,
                          password=get_request.password)
        if all_funcs is None:
            raise Exception('No functions found')

        res['data'] = {
            'total': len(list(all_funcs.values())[0]),
            'functions': all_funcs
        }
        res['status'] = 'success'
        res['message'] = 'All functions retrieved successfully'
    except Exception as e:
        res['message'] = str(e)
    finally:
        return res

@router.post("/functions")
def add_new_func(func_request: CreateFuncRequest) -> dict:
    '''
    Add a new serverless function to functions_store
    '''
    res = RESPONSE_TEMPLATE.copy()
    try:
        content = func_request.content
        print('Function request:', func_request)
        output = add_func(content, target_dir='functions_store', author=func_request.username,
                          password=func_request.password)
        if output is None:
            raise Exception('Function already exists')

        res['status'] = 'success'
        res['message'] = f'Successfully added function to store {output}'

    except Exception as e:
        res['message'] = str(e)
    finally:
        return res


@router.post("/execute/{func_name}")
def execute_func(func_name: str, exec_request: ExecFuncRequest) -> dict:
    '''
    Execute a function from functions_store
    Expect user to call get functions first to get the function name and target file
    '''
    res = RESPONSE_TEMPLATE.copy()
    try:
        params = exec_request.params
        target_file = exec_request.target
        output = invoke_func(
            func_name, params, target_dir='functions_store', target_file=target_file,
            author=exec_request.username, password=exec_request.password)

        if output is None:
            raise Exception('Your function did not run successfully')

        res['status'] = 'success'
        res['message'] = f'Successfully executed function {func_name}'
        res['data'] = output
    except Exception as e:
        res['message'] = str(e)
    finally:
        return res


@router.put("/functions/{func_name}")
def modify_existing_func(func_name: str, modify_request: ModifyFuncRequest) -> dict:
    '''
    Modify an existing serverless function in functions_store
    Expect user to call get functions first to get the function name and target file
    '''
    res = RESPONSE_TEMPLATE.copy()
    try:
        content = modify_request.content
        target_file = modify_request.target
        target_file = modify_func(
            func_name, content, target_dir='functions_store', target_file=target_file)
        if target_file is None:
            raise Exception('Function not found')
        res['status'] = 'success'
        res['message'] = f'Successfully modified function {func_name}'
    except Exception as e:
        res['message'] = str(e)
    finally:
        return res


@router.delete("/functions/{func_name}")
def delete_existing_func(func_name: str, del_request: DelFuncRequest) -> dict:
    '''
    Delete an existing serverless function from functions_store
    Expect user to call get functions first to get the function name and target file
    '''
    res = RESPONSE_TEMPLATE.copy()
    try:
        target_file = del_request.target
        delete_func(func_name, target_dir='functions_store',
                    target_file=target_file)
        res['status'] = 'success'
        res['message'] = f'Successfully deleted function {func_name}'
    except Exception as e:
        res['message'] = str(e)
    finally:
        return res


@router.get("/libs")
def get_installed_libs() -> dict:
    '''
    Get all installed libraries in the virtual environment
    '''
    res = RESPONSE_TEMPLATE.copy()
    try:
        res['status'] = 'success'
        res['message'] = 'All installed libraries retrieved successfully'
        res['data'] = get_libs()

    except Exception as e:
        res['message'] = str(e)
    finally:
        return res


@router.post("/libs")
def install_libraries(lib_request: LibInstallRequest) -> dict:
    '''
    Install Python libraries required by users
    '''
    res = RESPONSE_TEMPLATE.copy()
    try:
        libs = lib_request.libs
        print('Installing libraries:', libs)
        
        install_libs(libs, f'{CONF_STORE}/cloud_requirements.txt')
        res['status'] = 'success'
        res['message'] = 'Successfully installed libraries'

    except Exception as e:
        res['message'] = str(e)
    finally:
        return res


app.include_router(router)
