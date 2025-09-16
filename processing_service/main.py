import logging
import grpc
import spacy
import os
import sys

from concurrent import futures

from textblob import TextBlob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from proto import text_pb2_grpc, text_pb2

# Initialize spaCy model
nlp = spacy.load("en_core_web_sm")

logging.basicConfig(level=logging.INFO)


class TextProcessorServicer(text_pb2_grpc.TextProcessorServicer):
    def ProcessText(self, request, context):
        """
        This function is used to processes an input text request by performing tokenization, sentence segmentation, sentiment analysis, and named entity recognition (NER).
        Args:
            request (text_pb2.TextRequest): The gRPC request object containing the input text to process. Expected field: `text` (str).
            context (grpc.ServicerContext) Provides RPC-specific information (e.g., deadlines, status codes).

        Returns text_pb2.TextResponse:
            A gRPC response message containing:
                - tokens (list of str): Extracted tokens from the text.
                - sentences (list of str): Sentences segmented from the text.
                - sentiment (str): Sentiment classification ("Positive",
                  "Negative", "Neutral").
                - entities (list of text_pb2.Entity): Named entities detected
                  in the text, each with `text` and `label`.

        """
        text = request.text
        logging.info(f"Received text for processing: {text[:50]}...")
        sentiment = ""
        try:
            doc = nlp(text)
            blob = TextBlob(text)

            tokens = [token.text for token in doc]
            sentences = [sent.text for sent in doc.sents]

            if blob.polarity > 0:
                sentiment = "Positive"
            elif blob.polarity < 0:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

            logging.info(f"Sentiment: {sentiment}, polarity: {blob.polarity}")

            entities = [text_pb2.Entity(text=ent.text, label=ent.label_) for ent in doc.ents]

            return text_pb2.TextResponse(tokens=tokens, sentences=sentences, sentiment=sentiment, entities=entities)
        except Exception as e:
            logging.error(f"Error processing text: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return text_pb2.TextResponse(tokens=[], sentences=[], sentiment=sentiment, entities=[])


def serve():
    """
    This function sets up and runs a gRPC server that listens for incoming
    RPC calls to the TextProcessor service. It uses a thread pool to handle
    multiple concurrent requests.

    Args:

    Returns:
        None: This function blocks indefinitely and only returns when the
        server is terminated.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    text_pb2_grpc.add_TextProcessorServicer_to_server(TextProcessorServicer(), server)
    server.add_insecure_port("[::]:50051")
    logging.info("gRPC Processing Service running on port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
