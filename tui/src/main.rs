use std::{
    io,
    sync::{Arc, Mutex},
    time::{Duration, Instant},
};
use tokio::time::{interval, sleep}; // Import sleep
use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use ratatui::{backend::CrosstermBackend, Terminal};
use serde_json::Value;
use std::error::Error;

mod app;
mod ui;

async fn fetch_data(url: &str) -> Result<Value, Box<dyn Error>> {
    let response = reqwest::get(url).await?;
    let json: Value = response.json().await?;
    Ok(json)
}

fn parse_data(json_value: &Value) -> Vec<app::SensorData> {
    let mut data: Vec<app::SensorData> = Vec::new();
    if let Some(array) = json_value.as_array() {
        for item in array {
            if let Ok(sensor_data) = serde_json::from_value(item.clone()) {
                data.push(sensor_data);
            } else {
                eprintln!("Error parsing JSON object: {:?}", item);
            }
        }
    }
    data
}

<<<<<<< Updated upstream
async fn update_data_periodically(
    app_state: Arc<Mutex<app::AppState>>,
    json_url: String,
    manual_refresh_flag: Arc<Mutex<bool>>,
) {
    let mut interval = interval(Duration::from_secs(5 * 60)); // Regular interval
=======
async fn update_data_periodically(app_state: std::sync::Arc<app::AppState>, json_url: String) {
    let mut interval = interval(Duration::from_secs(10)); // ten seconds
>>>>>>> Stashed changes
    loop {
        tokio::select! {
            biased; // Apply biased selection to the entire block
            _ = interval.tick() => {
                fetch_and_update(app_state.clone(), &json_url).await;
            }
            manual_refresh = async {
                let should_refresh;
                {
                    let flag_guard = manual_refresh_flag.lock().unwrap();
                    should_refresh = *flag_guard;
                } // flag_guard is dropped here

                if should_refresh {
                    Some(())
                } else {
                    tokio::time::sleep(Duration::from_millis(100)).await; // Use tokio::time::sleep
                    None
                }
            } => {
                if manual_refresh.is_some() {
                    fetch_and_update(app_state.clone(), &json_url).await;
                    let mut flag_guard = manual_refresh_flag.lock().unwrap();
                    *flag_guard = false; // Reset the flag
                }
            }
        }
    }
}

async fn fetch_and_update(app_state: Arc<Mutex<app::AppState>>, url: &str) {
    match fetch_data(url).await {
        Ok(json) => {
            let parsed_data = parse_data(&json);
            let mut app_state_guard = app_state.lock().unwrap();
            let previous_len = app_state_guard.data.len();
            app_state_guard.data = parsed_data;
            if app_state_guard.data.len() > previous_len {
                app_state_guard.last_update_time = Some(Instant::now());
            }
        }
        Err(e) => {
            eprintln!("Error fetching data: {}", e);
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // Setup terminal
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen, EnableMouseCapture)?;
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    // Application state
    let app_state = Arc::new(Mutex::new(app::AppState::new()));
    let json_url = "http://192.168.1.193:8000/api/sensor_data".to_string();

    // Flag to trigger manual refresh from the main loop
    let manual_refresh_flag = Arc::new(Mutex::new(false));

    // Spawn a background task to update data periodically and on manual trigger
    let app_state_clone = Arc::clone(&app_state);
    let url_clone = json_url.clone();
    let refresh_flag_clone = Arc::clone(&manual_refresh_flag);
    tokio::spawn(async move {
        update_data_periodically(app_state_clone, url_clone, refresh_flag_clone).await;
    });

    // Main application loop
    let mut should_quit = false;
    let refresh_interval_ui = Duration::from_secs(10); // UI refresh interval
    while !should_quit {
        {
            let app_state_guard = app_state.lock().unwrap();
            terminal.draw(|f| {
                ui::render::<CrosstermBackend<std::io::Stdout>>(
                    f,
                    &app_state_guard,
                    refresh_interval_ui, // Pass the UI refresh interval
                    Arc::clone(&manual_refresh_flag), // Pass the flag
                )
            })?;
        }

        if event::poll(Duration::from_millis(100))? {
            if let Event::Key(key) = event::read()? {
                if let KeyCode::Char('q') = key.code {
                    should_quit = true;
                }
            }
        }
        tokio::time::sleep(Duration::from_millis(100)).await; // Small delay for responsiveness
    }

    // Restore terminal
    disable_raw_mode()?;
    execute!(
        terminal.backend_mut(),
        LeaveAlternateScreen,
        DisableMouseCapture
    )?;
    terminal.show_cursor()?;

    Ok(())
}