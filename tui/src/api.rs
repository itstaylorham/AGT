use warp::Filter;
use chrono::{NaiveDateTime, Utc, Duration, TimeZone};
use serde::{Deserialize, Serialize};
use std::fs;
use serde_json::Value;

#[derive(Serialize, Deserialize)]
pub struct SensorData {
    pub timestamp: String,
    pub mac_address: String,
    pub temperature: f64,
    pub light: f64,
    pub moisture: f64,
    pub conductivity: f64,
}

pub fn sensor_data_route() -> impl Filter<Extract = impl warp::Reply, Error = warp::Rejection> + Clone {
    warp::path!("api" / "sensor_data")
        .map(|| {
            let file_path = "sesh.json";
            match get_filtered_sensor_data(file_path) {
                Ok(filtered_data) => warp::reply::json(&filtered_data),
                Err(_) => warp::reply::json(&Vec::<SensorData>::new()),
            }
        })
}

fn get_filtered_sensor_data(file_path: &str) -> Result<Vec<SensorData>, Box<dyn std::error::Error>> {
    let content = fs::read_to_string(file_path)?;
    if content.trim().is_empty() {
        return Ok(Vec::new());
    }

    let raw_data: Value = serde_json::from_str(&content)?;
    let twenty_four_hours_ago = Utc::now() - Duration::hours(24);
    let mut filtered_data = Vec::new();

    if let Some(sensor_data_list) = raw_data.as_array() {
        for entry in sensor_data_list {
            if let Some(timestamp_str) = entry.get("Timestamp").and_then(|v| v.as_str()) {
                if let Ok(timestamp) = NaiveDateTime::parse_from_str(timestamp_str, "%Y-%m-%d %H:%M:%S") {
                    let timestamp_utc = Utc.from_local_datetime(&timestamp).unwrap();
                    if timestamp_utc >= twenty_four_hours_ago {
                        let sensor_data = SensorData {
                            timestamp: timestamp_utc.to_string(),
                            mac_address: entry.get("MAC").and_then(|v| v.as_str()).unwrap_or("").to_string(),
                            temperature: entry.get("Temperature").and_then(|v| v.as_f64()).unwrap_or(0.0),
                            light: entry.get("Light").and_then(|v| v.as_f64()).unwrap_or(0.0),
                            moisture: entry.get("Moisture").and_then(|v| v.as_f64()).unwrap_or(0.0),
                            conductivity: entry.get("Conductivity").and_then(|v| v.as_f64()).unwrap_or(0.0),
                        };
                        filtered_data.push(sensor_data);
                    }
                }
            }
        }
    }

    Ok(filtered_data)
}
