import pytest

from processing_service.main import TextProcessorServicer
from proto import text_pb2


class MockGRPCContext:
    def __init__(self):
        self.code = None
        self.details = None

    def set_code(self, code):
        self.code = code

    def set_details(self, details):
        self.details = details

    def abort(self, code, details):
        self.set_code(code)
        self.set_details(details)
        raise Exception(f"RPC aborted with code {code}: {details}")


@pytest.fixture
def servicer():
    return TextProcessorServicer()

@pytest.fixture
def grpc_context():
    return MockGRPCContext()


def test_process_text_positive(servicer, grpc_context):
    request = text_pb2.TextRequest(text="I love this project!")
    response = servicer.ProcessText(request, context=grpc_context)

    assert "love" in response.tokens
    assert "I love this project!" in response.sentences
    assert response.sentiment == "Positive"


def test_process_text_negative(servicer, grpc_context):
    request = text_pb2.TextRequest(text="This is terrible!")
    response = servicer.ProcessText(request, context=grpc_context)

    assert response.sentiment == "Negative"


def test_process_text_neutral(servicer, grpc_context):
    request = text_pb2.TextRequest(text="The sky is blue.")
    response = servicer.ProcessText(request, context=grpc_context)

    assert response.sentiment == "Neutral"
