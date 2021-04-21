class MatrixUnexpectedResponseError(Exception):
    """RMT_UNEXPECTEDRESPONSE"""

    def __init__(self, message="An unexpected response was returned."):
        self.message = message
        super().__init__(self.message)


class MateLibNotLoadableError(Exception):
    """RMT_LIBNOTLOADABLE"""

    def __init__(self, message=f"Cannot load the MATE remote access API"):
        self.message = message
        super().__init__(self.message)


class MatrixCriticalHardwareFailureError(Exception):
    """RMT_INTERNALFAILURE"""

    def __init__(self, message="The Matrix CU has reported a hardware failure. \n "
                               "Restarting the CU and Matrix should fix this.."):
        self.message = message
        super().__init__(self.message)


class MatrixNotInitialisedError(Exception):
    """RMT_NOSERVER"""

    def __init__(self, message=f"Matrix must be open and initialised before calling IO.connect()?"):
        self.message = message
        super().__init__(self.message)


class MatrixIncompatibleProtocolError(Exception):
    """RMT_INCOMPATIBLEPROTOCOL"""

    def __init__(self, message=f"There is an incompatability between Matrix.exe and the remote access API. \n "
                               f"This may be due to a 32/64 bit iocompatiblity. \n"
                               f"Alternatively, if multiple versions of Matrix are installed, inconsistent naming \n"
                               f"between versions during installation can cause \n"
                               f"nOmicron to point to incorrect Matrix paths."):
        self.message = message
        super().__init__(self.message)


class MatrixUnsupportedReqError(Exception):
    """RMT_UNSUPPORTEDREQ"""

    def __init__(self, message=f"Req is not supported"):
        self.message = message
        super().__init__(self.message)


class MatrixUnsupportedOperationError(Exception):
    """RMT_UNKNOWNOBJECT, RMT_UNKNOWNPROPERTY"""

    def __init__(self, message=f"Requested operation is not supported \n"
                               f"in the current experiment/hardware configuration"):
        self.message = message
        super().__init__(self.message)


class MatrixInvalidDataTypeError(Exception):
    """RMT_INVALIDTYPE"""

    def __init__(self, message=f"The requested object type is not compatible with the requested operation"):
        self.message = message
        super().__init__(self.message)


class MatrixRejectedError(Exception):
    """RMT_REJECTED"""

    def __init__(self, message=f"The requested operation has been rejected"):
        self.message = message
        super().__init__(self.message)


class MatrixParameterOutOfRangeWarning(Warning):
    def __init__(self, message="Requested parameter value is outside of tolerable range. \n "
                               "Matrix may behave oddly or die "):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return repr(self.message)
