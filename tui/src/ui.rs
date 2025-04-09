use ratatui::{
    layout::{Constraint, Direction, Layout},
    style::{Color, Modifier, Style},
    widgets::{Block, Borders, Paragraph, Row, Table},
    Frame,
};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

use crate::app::AppState;

pub fn render(
    f: &mut Frame,
    app_state: &AppState,
    refresh_interval_ui: Duration,
    manual_refresh_flag: Arc<Mutex<bool>>,
    api_url: &str, // added this
) {
    let chunks = Layout::default()
        .direction(Direction::Vertical)
        .margin(1)
        .constraints([
            Constraint::Min(0),        // Data table
            Constraint::Length(1),     // Countdown timer
            Constraint::Length(1),     // Source URL
        ])
        .split(f.size());

    let mut reversed_data = app_state.data.clone();
    reversed_data.reverse();

    let rows = reversed_data.iter().enumerate().map(|(i, item)| {
        let mut style = Style::default();
        if let Some(last_update) = app_state.last_update_time {
            let original_index = app_state.data.len().saturating_sub(1) - i;
            if last_update.elapsed() < Duration::from_secs(3) && original_index >= app_state.previous_data_len {
                style = style.add_modifier(Modifier::BOLD).fg(Color::Green);
            }
        }
        Row::new(vec![
            item.timestamp.clone(),
            item.mac.clone(),
            format!("{:.2}", item.temperature),
            format!("{}", item.moisture),
            format!("{}", item.light),
            format!("{}", item.conductivity),
        ])
        .style(style)
    });

    let table = Table::new(rows, &[
        Constraint::Percentage(20),
        Constraint::Percentage(15),
        Constraint::Percentage(15),
        Constraint::Percentage(15),
        Constraint::Percentage(15),
        Constraint::Percentage(15),
    ])
    .header(
        Row::new(vec!["Timestamp", "MAC", "Temperature", "Moisture", "Light", "Conductivity"])
            .style(Style::default().fg(Color::Yellow)),
    )
    .block(Block::default().title("Sensor Data").borders(Borders::ALL));

    f.render_widget(table, chunks[0]);

    // Countdown timer
    let now = Instant::now();
    let elapsed_since_update = app_state
        .last_update_time
        .map_or(refresh_interval_ui, |t| now.duration_since(t));

    let remaining_secs = if elapsed_since_update < refresh_interval_ui {
        (refresh_interval_ui - elapsed_since_update).as_secs()
    } else {
        let mut refresh_flag_guard = manual_refresh_flag.lock().unwrap();
        *refresh_flag_guard = true;
        refresh_interval_ui.as_secs()
    };

    // API source URL display
    let source_text = format!("Source: {}", api_url);
    let source = Paragraph::new(source_text).style(Style::default().fg(Color::DarkGray));
    f.render_widget(source, chunks[2]);
}
