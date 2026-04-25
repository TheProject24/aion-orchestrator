# worker/worker.py

import uuid
import grpc
from concurrent import futures
import argparse
import joblib
import numpy as np

import service_pb2
import service_pb2_grpc

class ModelOrchestrator(service_pb2_grpc.ModelOrchestratorServicer):
    def __init__(self):
        self.worker_id = f"worker -- {uuid.uuid4().hex[:6]}"

        print(f"[{self.worker_id}] Loading ML model into RAM...")
        self.model = joblib.load("lightweight_model.joblib")
        print(f"[{self.worker_id}] Model loaded successfully!")

    def Predict(self, request, context):
        incoming_data = list(request.input_data)
        features = np.array([incoming_data])
        prediction_value = self.model.predict(features)[0]
        print(f"[{self.worker_id}] Inference requested for {incoming_data} -> Prediction: {prediction_value:.2f}")

        return service_pb2.InferenceResponse(
            prediction=f"{prediction_value:.2f}",
            confidence=1.0,
            worker_id=self.worker_id
        )

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    my_orchestrator = ModelOrchestrator()
    service_pb2_grpc.add_ModelOrchestratorServicer_to_server(my_orchestrator, server)

    server.add_insecure_port(f"[::]:{port}")
    server.start()

    print(f"Python Worker [{my_orchestrator.worker_id}] started. Listening on port {port}")
    server.wait_for_termination()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aion ML Worker")
    parser.add_argument("--port", type=str, default="50051", help="The Port to listen on")
    args = parser.parse_args()

    serve(args.port)
