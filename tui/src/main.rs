use std::{io, time::Duration};
use tokio::time::interval;
use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use ratatui::backend::CrosstermBackend;
use ratatui::Terminal;
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

async fn update_data_periodically(app_state: std::sync::Arc<app::AppState>, json_url: String) {
    let mut interval = interval(Duration::from_secs(5 * 60)); // 5 minutes
    loop {
        interval.tick().await;
        match fetch_data(&json_url).await {
            Ok(json) => {
                let parsed_data = parse_data(&json);
                let mut data_guard = app_state.data.lock().unwrap();
                *data_guard = parsed_data;
            }
            Err(e) => {
                eprintln!("Error fetching data: {}", e);
            }
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
    let app_state = std::sync::Arc::new(app::AppState::new());
    let json_url = "http://localhost:8000/api/sensor_data".to_string(); // Corrected URL

    // Spawn a background task to update data periodically
    let app_state_clone = app_state.clone();
    let url_clone = json_url.clone();
    tokio::spawn(async move {
        update_data_periodically(app_state_clone, url_clone.to_string()).await;
    });

    // Main application loop
    let mut should_quit = false;
    while !should_quit {
        {
            let app_state_ref = app_state.clone();
            terminal.draw(|f| ui::render::<CrosstermBackend<std::io::Stdout>>(f, &app_state_ref))?;
        }

        if event::poll(Duration::from_millis(100))? {
            if let Event::Key(key) = event::read()? {
                if let KeyCode::Char('q') = key.code {
                    should_quit = true;
                }
            }
        }
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