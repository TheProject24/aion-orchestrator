use aion::model_orchestrator_client::ModelOrchestratorClient;
use aion::InferenceRequest;

pub mod aion {
    tonic::include_proto!("aion");
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Gateway: Attempting to connect to Python Worker...");

    let mut client = ModelOrchestratorClient::connect("http://127.0.0.1:50051").await?;
        
    println!("Gateway: Connected Successfully!");

    let request = tonic::Request::new(InferenceRequest {
        model_name: "resnet50_v1".to_string(),
        input_data: vec![1,2,3,4,5], //Mocked Tensor bytes
    });

    let start_time = std::time::Instant::now();
    let response = client.predict(request).await?;
    let elapsed = start_time.elapsed();

    let response_data = response.into_inner();

    println!("----------------------------------------------------------");
    println!("Gateway: Received Response in {:?}", elapsed);
    println!("Gateway: Prediction -> {}", response_data.prediction);
    println!("Gateway: Confidence -> {}%", response_data.confidence * 100.0);
    println!("Gateway: Handled By -> {}", response_data.worker_id);
    println!("--------------------------------------------------");

    Ok(())
}
