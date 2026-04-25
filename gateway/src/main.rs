// gateway/src/main.rs

use aion::model_orchestrator_client::ModelOrchestratorClient;
use aion::InferenceRequest;
use tonic::transport::{Channel, Endpoint};

pub mod aion {
    tonic::include_proto!("aion");
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Gateway: Setting up,load balancer...");

    let endpoints = vec![
        Endpoint::from_static("http://127.0.0.1:50051"),
        Endpoint::from_static("http://127.0.0.1:50052"),
        Endpoint::from_static("http://127.0.0.1:50053"),
        Endpoint::from_static("http://127.0.0.1:50054"),
    ];

    let channel = Channel::balance_list(endpoints.into_iter());
    let mut client = ModelOrchestratorClient::new(channel);
        
    println!("Gateway: Connected Successfully! Beginning Infinite Loop . . . \n");

    let mut i = 1;

    loop {
        let max_retries = 4;
        let mut success = false;

        for attempt in 1..=max_retries {
            let request = tonic::Request::new(InferenceRequest {
                model_name: "resnet50_v1".to_string(),
                input_data: vec![1, 2, 3],
            });

            match client.predict(request).await {
                Ok(response) => {
                    let inner = response.into_inner();
                        println!(
                            "Request {}: Handled by -> {} Prediction: {} (Confidence: {})",
                            i,
                            inner.worker_id,
                            inner.prediction,
                            inner.confidence
                        );

                    success = true;
                    break;
                }
                Err(e) => {
                    println!(
                        "Request {}: [Attempt {}/{}] Load Balancer hit a DEAD node! Error {}", 
                        i,
                        attempt,
                        max_retries, 
                        e.message()
                    );
                    if attempt < max_retries {
                        tokio::time::sleep(std::time::Duration::from_millis(300)).await;
                    }
                }
            }
        }

        if !success {
            println!("Request {}: X Completely Failed after {} attempts", i, max_retries);
        }

        i += 1;

        tokio::time::sleep(std::time::Duration::from_millis(3000)).await;
    }
}
