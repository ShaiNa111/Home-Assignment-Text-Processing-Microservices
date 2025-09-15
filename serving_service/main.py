import grpc
import logging
import sys
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from proto import text_pb2_grpc, text_pb2


logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Text Summarizer API")


class TextRequestModel(BaseModel):
    text: str


# gRPC channel to processing service
channel = grpc.insecure_channel("processing_service:50051")
stub = text_pb2_grpc.TextProcessorStub(channel)


@app.post("/summarize")
async def summarize(request: TextRequestModel):
    try:
        grpc_request = text_pb2.TextRequest(text=request.text)
        response = stub.ProcessText(grpc_request)

        # Convert protobuf response to dict
        result = {
            "tokens": list(response.tokens),
            "sentences": list(response.sentences)
        }
        return result

    except grpc.RpcError as e:
        logging.error(f"gRPC error: {e}")
        raise HTTPException(status_code=500, detail=f"Processing error: {e.details()}")


@app.get("/health")
async def health():
    return {"status": "ok"}
