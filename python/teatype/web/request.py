# Copyright (c) 2024-2025 enamentis GmbH. All rights reserved.
#
# This software module is the proprietary property of enamentis GmbH.
# Unauthorized copying, modification, distribution, or use of this software
# is strictly prohibited unless explicitly authorized in writing.
# 
# THIS SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES, OR OTHER LIABILITY ARISING FROM THE USE OF THIS SOFTWARE.
# 
# For more details, check the LICENSE file in the root directory of this repository.

# Package imports
import requests
import aiohttp

# As system imports
import json as json_util

# From system imports
from enum import Enum

# From package imports
from teatype.logging import err, log, warn
from teatype.util import stopwatch
from urllib.parse import urlparse

class _CRUD_METHOD(Enum):
    """
    Enumeration of CRUD HTTP methods.
    """
    DELETE = 'DELETE'
    GET = 'GET'
    PATCH = 'PATCH'
    POST = 'POST'
    PUT = 'PUT'
    
class _Response:
    """
    Conversion class to represent an HTTP response object.
    """
    data:any
    headers:dict
    status:int
    
    def __init__(self, status_code:int, content:any, headers:dict, json:bool=True):
        """
        Initialize the HTTP response object.

        Args:
            status_code (int): The HTTP status code.
            content (any): The response content.
        """
        self.status = status_code
        self.data = json_util.loads(content) if json else content
        self.headers = headers
    
def _request(crud_method:str,
             url:str,
             data:any=None,
             params:dict=None,
             measure_time:bool=False,
             json:bool=True,
             verbose:bool=False,
             headers:dict={},
             _async:aiohttp.ClientSession=None) -> requests.Response|aiohttp.ClientResponse|None:
    """
    Internal helper function to perform HTTP requests based on CRUD methods.

    Args:
        crud_method (str): The CRUD method (DELETE, GET, PATCH, POST, PUT).
        url (str): The URL to send the request to.
        data (any, optional): The data to include in the request body. Defaults to None.
        params (dict, optional): Query parameters to include in the request URL. Defaults to None.
        measure_time (str, optional): Label to measure the time taken for the request. Defaults to None.
        json (bool, optional): Whether to return the response as JSON. Defaults to True.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.
        _async (aiohttp.ClientSession, optional): Async HTTP session for asynchronous requests. Defaults to None.

    Returns:
        requests.Response or aiohttp.ClientResponse or None: The HTTP response object or None if an error occurs.
    """
    # Parse the request URL to validate its structure
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        err(f'Invalid URL: {url}') # Log an error if URL is invalid
        return None

    request_label = f'{crud_method} {url}'
    # Start the stopwatch if a measure time is specified for performance tracking
    if measure_time:
        # Set the request data to an empty dictionary if not provided
        stopwatch(request_label)

    # Determine whether to use synchronous requests or the provided async session
    call = requests if not _async else _async
    # Match the CRUD method to perform the corresponding HTTP request
    match crud_method:
        case _CRUD_METHOD.DELETE.value:
            # Perform a DELETE request
            response = call.delete(url, data=data, params=params, headers=headers)
        case _CRUD_METHOD.GET.value:
            if data:
                # Maybe construct a response instead?
                err('GET requests do not support request data')
                return None
            # Perform a GET request
            response = call.get(url, params=params, headers=headers)
        case _CRUD_METHOD.PATCH.value:
            # Perform a PATCH request
            response = call.patch(url, data=data, params=params, headers=headers)
        case _CRUD_METHOD.POST.value:
            # Perform a POST request
            response = call.post(url, data=data, params=params, headers=headers)
        case _CRUD_METHOD.PUT.value:
            # Perform a PUT request
            response = call.put(url, data=data, params=params, headers=headers)
        case _:
            err(f'Invalid CRUD method: {crud_method}') # Log an error for invalid CRUD methods
            return None

    if verbose:
        if not _async:
            # Log the type of request and the target URL for debugging purposes
            log(f'Synchronous request: {request_label}')
        else:
            log(f'Asynchronous request: {request_label}')

    # Stop the stopwatch if a measure time was specified
    if measure_time:
        stopwatch()

    # Retrieve the response content based on the json flag
    _response = _Response(response.status_code, response.content, response.headers, json)
    # If verbose logging is enabled, log the result of the request
    if verbose:
        if _response.status >= 400:
            err(f'Synchronous request failed: [{_response.status}] {_response.data}') # Log failure
        else:
            log(f'Synchronous request success: [{_response.status}] {_response.data}') # Log success
    return _response # Return the HTTP response object

def sync_request(crud_method:str,
                 url:str,
                 data:any=None,
                 params:dict=None,
                 measure_time:bool=False,
                 json:bool=True,
                 verbose:bool=False,
                 headers:dict={}) -> requests.Response:
    """
    Perform a synchronous HTTP request based on the specified CRUD method.
    This exists as a wrapper function to call the internal _request function and it allows
    dynamic selection of the CRUD method to use for testing or debugging purposes.

    Args:
        crud_method (str): The CRUD method (DELETE, GET, PATCH, POST, PUT).
        url (str): The URL to send the request to.
        data (any, optional): The data to include in the request body. Defaults to None.
        params (dict, optional): Query parameters to include in the request URL. Defaults to None.
        measure_time (str, optional): Label to measure the time taken for the request. Defaults to None.
        json (bool, optional): Whether to return the response as JSON. Defaults to True.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.

    Returns:
        requests.Response: The HTTP response object.
    """
    # Call the internal _request function with the provided parameters to perform the synchronous request
    return _request(crud_method, url, data, params, measure_time, json, verbose, headers)

def get(url:str,
        params:dict=None,
        measure_time:bool=False,
        json:bool=True,
        verbose:bool=False,
        headers:dict={}) -> requests.Response:
    """
    Perform a synchronous GET request.

    Args:
        url (str): The URL to send the request to.
        params (dict, optional): Query parameters to include in the request URL. Defaults to None.
        measure_time (str, optional): Label to measure the time taken for the request. Defaults to None.
        json (bool, optional): Whether to return the response as JSON. Defaults to True.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.

    Returns:
        requests.Response: The HTTP response object.
    """
    # Call the internal _request function with the provided parameters to perform the synchronous GET request
    return _request(_CRUD_METHOD.GET.value, url, None, params, measure_time, json, verbose)

def post(url:str,
         data:any=None,
         params:dict=None,
         measure_time:bool=False,
         json:bool=True,
         verbose:bool=False,
         headers:dict={}) -> requests.Response:
    """
    Perform a synchronous POST request.

    Args:
        url (str): The URL to send the request to.
        data (any, optional): The data to include in the request body. Defaults to None.
        params (dict, optional): Query parameters to include in the request URL. Defaults to None.
        measure_time (str, optional): Label to measure the time taken for the request. Defaults to None.
        json (bool, optional): Whether to return the response as JSON. Defaults to True.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.

    Returns:
        requests.Response: The HTTP response object.
    """
    # Call the internal _request function with the provided parameters to perform the synchronous POST request
    return _request(_CRUD_METHOD.POST.value, url, data, params, measure_time, json, verbose, headers)

def put(url:str,
        data:any=None,
        params:dict=None,
        measure_time:bool=False,
        json:bool=True,
        verbose:bool=False,
        headers:dict={}) -> requests.Response:
    """
    Perform a synchronous PUT request.

    Args:
        url (str): The URL to send the request to.
        data (any, optional): The data to include in the request body. Defaults to None.
        params (dict, optional): Query parameters to include in the request URL. Defaults to None.
        measure_time (str, optional): Label to measure the time taken for the request. Defaults to None.
        json (bool, optional): Whether to return the response as JSON. Defaults to True.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.

    Returns:
        requests.Response: The HTTP response object.
    """
    # Call the internal _request function with the provided parameters to perform the synchronous PUT request
    return _request(_CRUD_METHOD.PUT.value, url, data, params, measure_time, json, verbose, headers)
    
def patch(url:str,
          data:any=None,
          params:dict=None,
          measure_time:bool=False,
          json:bool=True,
          verbose:bool=False,
          headers:dict={}) -> requests.Response:
    """
    Perform a synchronous PATCH request.

    Args:
        url (str): The URL to send the request to.
        data (any, optional): The data to include in the request body. Defaults to None.
        params (dict, optional): Query parameters to include in the request URL. Defaults to None.
        measure_time (str, optional): Label to measure the time taken for the request. Defaults to None.
        json (bool, optional): Whether to return the response as JSON. Defaults to True.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.

    Returns:
        requests.Response: The HTTP response object.
    """
    # Call the internal _request function with the provided parameters to perform the synchronous PATCH request
    return _request(_CRUD_METHOD.PATCH.value, url, data, params, measure_time, json, verbose, headers)

def delete(url:str,
           data:any=None,
           params:dict=None,
           measure_time:bool=False,
           json:bool=True,
           verbose:bool=False,
           headers:dict={}) -> requests.Response:
    """
    Perform a synchronous DELETE request.

    Args:
        url (str): The URL to send the request to.
        data (any, optional): The data to include in the request body. Defaults to None.
        params (dict, optional): Query parameters to include in the request URL. Defaults to None.
        measure_time (str, optional): Label to measure the time taken for the request. Defaults to None.
        json (bool, optional): Whether to return the response as JSON. Defaults to True.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.

    Returns:
        requests.Response: The HTTP response object.
    """
    # Call the internal _request function with the provided parameters to perform the synchronous DELETE request
    return _request(_CRUD_METHOD.DELETE.value, url, data, params, measure_time, json, verbose, headers)

async def async_request(crud_method:str,
                        url:str,
                        data:any=None,
                        params:dict=None,
                        measure_time:bool=False,
                        json:bool=True,
                        verbose:bool=False,
                        headers:dict={}) -> aiohttp.ClientResponse:
    """
    Perform an asynchronous HTTP request based on the specified CRUD method.

    Args:
        crud_method (str): The CRUD method (DELETE, GET, PATCH, POST, PUT).
        url (str): The URL to send the request to.
        data (any, optional): The data to include in the request body. Defaults to None.
        params (dict, optional): Query parameters to include in the request URL. Defaults to None.
        measure_time (str, optional): Label to measure the time taken for the request. Defaults to None.
        json (bool, optional): Whether to return the response as JSON. Defaults to True.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.

    Returns:
        aiohttp.ClientResponse: The HTTP response object.
    """
    # Create an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Call the internal _request function with the provided parameters and session to perform the async request
        async with _request(crud_method,
                            url,
                            data,
                            params,
                            measure_time,
                            json,
                            verbose,
                            session) as response:
            return response # Return the HTTP response object

def async_get(url:str,
              params:dict=None,
              measure_time:bool=False,
              json:bool=True,
              verbose:bool=False,
              headers:dict={}) -> aiohttp.ClientResponse:
    """
    Perform an asynchronous GET request.

    Args:
        url (str): The URL to send the request to.
        params (dict, optional): Query parameters to include in the request URL. Defaults to None.
        measure_time (str, optional): Label to measure the time taken for the request. Defaults to None.
        json (bool, optional): Whether to return the response as JSON. Defaults to True.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.

    Returns:
        aiohttp.ClientResponse: The HTTP response object.
    """
    # Call the internal _request function with the provided parameters to perform the asynchronous GET request
    return _request(_CRUD_METHOD.GET.value, url, None, params, measure_time, json, verbose, _async=aiohttp.ClientSession())