use serde::Deserialize;
use std::sync::{Arc, Mutex};
use std::time::Instant;

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
    pub data: Vec<SensorData>,
    pub last_update_time: Option<Instant>,
    pub previous_data_len: usize,
}

impl AppState {
    pub fn new() -> Self {
        AppState {
            data: vec![],
            last_update_time: None,
            previous_data_len: 0,
        }
    }
}