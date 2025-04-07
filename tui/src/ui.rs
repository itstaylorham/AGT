use ratatui::{
    backend::Backend,
    layout::{Constraint, Direction, Layout},
    style::{Color, Style},
    widgets::{Block, Borders, Row, Table},
    Frame,
};

use crate::app::AppState;

pub fn render<B: Backend>(f: &mut Frame, app_state: &AppState) {
    let chunks = Layout::default()
        .direction(Direction::Vertical)
        .margin(1)
        .constraints([Constraint::Percentage(100)].as_ref())
        .split(f.size());

    let guard = app_state.data.lock().unwrap();
    let rows = guard.iter().map(|item| {
        Row::new(vec![
            item.timestamp.clone(),
            item.mac.clone(),
            format!("{:.2}", item.temperature),
            format!("{}", item.moisture),
            format!("{}", item.light),
            format!("{}", item.conductivity),
        ])
    });

    let table = Table::new(rows, &[
        Constraint::Percentage(20),
        Constraint::Percentage(15),
        Constraint::Percentage(15),
        Constraint::Percentage(15),
        Constraint::Percentage(15),
        Constraint::Percentage(15),
    ])
    .header(Row::new(vec!["Timestamp", "MAC", "Temperature", "Moisture", "Light", "Conductivity"]).style(Style::default().fg(Color::Yellow)))
    .block(Block::default().title("Sensor Data").borders(Borders::ALL));

    f.render_widget(table, chunks[0]);
}