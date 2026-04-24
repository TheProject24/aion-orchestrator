import argparse
import grpc
from concurrent import futures
import time
import uuid

import service_pb2
import service_pb2_grpc

class ModelOrchestrator(service_pb2_grpc.ModelOrchestratorServicer):
    def __init__(self):
        
        self.worker_id = f"worker--{str(uuid.uuid4())[:6]}"

    def Predict(self, request, context):
        print(f"[{self.worker_id}] Received request for model: {request.model_name}")

        # MOCK ML INFERENCE: 
        # Here is where we would normally pass request.input_data to PyTorch or Scikit-Learn.
        # For now, we will just sleep for 50ms to simulate the GPU/CPU doing math.
        time.sleep(0.05)

        return service_pb2.InferenceResponse(
            prediction="mock_predict_cat",
            confidence=0.98,
            worker_id=self.worker_id
        )
    
def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    my_orchestrator = ModelOrchestrator()

    service_pb2_grpc.add_ModelOrchestratorServicer_to_server(my_orchestrator, server)

    server.add_insecure_port(f"[::]:{port}")
    server.start()

    print(f"Python Worker [{my_orchestrator.worker_id}] started. Listening on port {port}...")
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aion ML Worker")
    parser.add_argument("--port", type=str, default="50051", help="The port to listen on")
    args = parser.parse_args()

    serve(args.port)

