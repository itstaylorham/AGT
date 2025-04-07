// src/app.rs (Modified)
use serde::Deserialize;
use std::sync::{Arc, Mutex};

#[derive(Deserialize, Clone)]
pub struct SensorData {
    pub timestamp: String,
    #[serde(rename = "mac_address")] // Add this serde attribute
    pub mac: String,
    pub temperature: f64,
    pub moisture: i32,
    pub light: i32,
    pub conductivity: i32,
}

#[derive(Clone)]
pub struct AppState {
    pub data: Arc<Mutex<Vec<SensorData>>>,
}

impl AppState {
    pub fn new() -> Self {
        AppState {
            data: Arc::new(Mutex::new(vec![])),
        }
    }
}