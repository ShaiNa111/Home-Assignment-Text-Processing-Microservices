import pytest
import grpc
from concurrent import futures

from processing_service.main import TextProcessorServicer
from proto import text_pb2, text_pb2_grpc


@pytest.fixture(scope="module")
def grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    text_pb2_grpc.add_TextProcessorServicer_to_server(TextProcessorServicer(), server)
    port = server.add_insecure_port("[::]:50052")
    server.start()
    yield f"localhost:{port}"
    server.stop(0)


def test_grpc_process_text(grpc_server):
    channel = grpc.insecure_channel(grpc_server)
    stub = text_pb2_grpc.TextProcessorStub(channel)

    request = text_pb2.TextRequest(text="Hello world.")
    response = stub.ProcessText(request)

    assert "Hello" in response.tokens
    assert "Hello world." in response.sentences
    assert response.sentiment == "Neutral"
