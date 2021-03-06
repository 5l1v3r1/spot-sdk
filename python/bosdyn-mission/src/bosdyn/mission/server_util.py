# Copyright (c) 2019 Boston Dynamics, Inc.  All rights reserved.
#
# Downloading, reproducing, distributing or otherwise using the SDK Software
# is subject to the terms and conditions of the Boston Dynamics Software
# Development Kit License (20191101-BDSDK-SL).

import bosdyn.util
from bosdyn.api import header_pb2


class ResponseContext(object):
    def __init__(self, response, request):
        self.response = response
        self.response.header.request_header.CopyFrom(request.header)

    def __enter__(self):
        self.response.header.request_received_timestamp.CopyFrom(bosdyn.util.now_timestamp())
        return self.response

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.response.header.error.code == self.response.header.error.CODE_UNSPECIFIED:
            self.response.header.error.code = self.response.header.error.CODE_OK

def set_response_header(response, request, error_code=header_pb2.CommonError.CODE_OK,
                               error_message=None):
    """Sets the ResponseHeader header in the response."""
    header = header_pb2.ResponseHeader()
    header.request_received_timestamp = bosdyn.util.now_timestamp()
    header.request_header.CopyFrom(request.header)
    header.error.code = error_code
    if error_message:
        header.error.message = error_message
    response.header.CopyFrom(header)
