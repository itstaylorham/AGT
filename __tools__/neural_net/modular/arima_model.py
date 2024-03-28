from statsmodels.tsa.arima.model import ARIMA

def fit_arima_model(series, order=(1,1,1)):
    model = ARIMA(series, order=order)
    model_fit = model.fit()
    return model_fit

def calculate_residuals(model_fit, series):
    predictions = model_fit.predict(start=series.index[0], end=series.index[-1])
    residuals = series - predictions
    return residuals
