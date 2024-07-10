from flask import Flask, render_template
from dash import dcc, html, Dash
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
import librosa
import base64
import io

# Initialize the Flask app
server = Flask(__name__)

# Initialize the Dash app
app = Dash(__name__, server=server, url_base_pathname='/analyse/')

app.layout = html.Div([
    html.H1('Amplitude Analysis', style={'textAlign': 'center'}),
    html.Div(
        dcc.Upload(
            id='upload-audio',
            children=html.Button('Upload Audio File', style={'fontSize': 20}),
            multiple=False
        ),
        style={'textAlign': 'center', 'marginBottom': '20px'}
    ),
    dcc.Loading(
        id='loading',
        type='default',
        children=dcc.Graph(id='amplitude-plot',config={
            'modeBarButtonsToAdd': ['drawrect', 'eraseshape', 'zoom', 'zoomIn', 'zoomOut', 'resetScale2d'],
            'displaylogo': False
        })
    ),
    html.Div([
        'Start Time (s): ',
        dcc.Input(id='start-time', type='number', value=0, step=0.0001, style={'fontSize': 20, 'height': '25px', 'width': '100px'}),
        html.Span(' ', style={'margin': '0 10px'}),
        ' End Time (s): ',
        dcc.Input(id='end-time', type='number', value=0, step=0.0001, style={'fontSize': 20, 'height': '25px', 'width': '100px'}),
        html.Span(' ', style={'margin': '0 10px'}),
        html.Button('Confirm', id='confirm-button', n_clicks=0, style={'fontSize': 20, 'height': '30px'})
    ], style={'textAlign': 'center', 'fontSize': 20, 'marginBottom': 10}),
    html.Div(id='output-container', style={'textAlign': 'center', 'fontSize': 20}),
    dcc.Graph(id='fft-plot', config={
        'modeBarButtonsToAdd': ['drawrect', 'eraseshape', 'zoom', 'zoomIn', 'zoomOut', 'resetScale2d'],
        'displaylogo': False
    }),
    dcc.Graph(id='inverse-amplitude-plot', style={'marginTop': '-30px'})  # Placeholder for inverse FFT plot
])

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    audio_data, sr = librosa.load(io.BytesIO(decoded), sr=None)
    
    # Calculate the amplitude
    amplitude = audio_data
    time = np.linspace(0, len(audio_data) / sr, num=len(audio_data))

    # Convert amplitude and time to standard Python float
    amplitude = amplitude.astype(float)
    time = time.astype(float)

    # Create the initial amplitude plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=amplitude, mode='lines', name='Amplitude'))
    fig.update_layout(
        title='Audio Waveform',
        xaxis_title='Time (s)',
        yaxis_title='Amplitude'
    )
    
    return fig, time, amplitude, sr

@app.callback(
    Output('amplitude-plot', 'figure'),
    [Input('upload-audio', 'contents')]
)
def update_amplitude_plot(contents):
    if contents is not None:
        amplitude_fig, time, amplitude, sr = parse_contents(contents)
        amplitude_fig.update_layout(
            shapes=[]
        )
        return amplitude_fig
    return go.Figure()

@app.callback(
    [Output('output-container', 'children'),
     Output('fft-plot', 'figure'),
     Output('inverse-amplitude-plot', 'figure')],
    [Input('confirm-button', 'n_clicks')],
    [State('amplitude-plot', 'figure'),
     State('start-time', 'value'),
     State('end-time', 'value')]
)
def update_fft_and_inverse_plots(n_clicks, figure, start_time, end_time):
    if figure is None or 'data' not in figure or len(figure['data']) == 0:
        return 'Upload an audio file to analyze.', go.Figure(), go.Figure()

    time = np.array(figure['data'][0]['x'])
    amplitude = np.array(figure['data'][0]['y'])
    sr = 1 / (time[1] - time[0])
    
    x0, x1 = None, None

    if n_clicks > 0 and start_time is not None and end_time is not None:
        x0 = start_time
        x1 = end_time

    if x0 is not None and x1 is not None:
        if x0 > x1:
            x0, x1 = x1, x0

        selected_points = [{'time': time[i], 'amplitude': amplitude[i]} for i in range(len(time)) if x0 <= time[i] <= x1]

        amplitudes = np.array([point['amplitude'] for point in selected_points])
        window = np.hanning(len(amplitudes))
        amplitudes_windowed = amplitudes * window

        N = len(amplitudes_windowed)
        yf_segment = np.fft.fft(amplitudes_windowed)
        xf_segment = np.fft.fftfreq(N, 1 / sr)

        idx = np.arange(1, N // 2)
        xf_segment = xf_segment[idx]
        yf_segment = np.abs(yf_segment[idx])

        fft_fig = go.Figure()
        fft_fig.add_trace(go.Scatter(x=xf_segment, y=yf_segment, mode='lines', name='FFT'))
        fft_fig.update_layout(
            title='The frequency domain of the selected time domain after DFT transformation',
            xaxis_title='Frequency (Hz)',
            yaxis_title='Amplitude'
        )

        # Create a symmetric spectrum for inverse FFT
        yf_symmetric = np.zeros(N, dtype=complex)
        yf_symmetric[:len(yf_segment)] = yf_segment
        yf_symmetric[-len(yf_segment):] = yf_segment[::-1]

        # Compute inverse FFT
        inverse_signal = np.fft.ifft(yf_symmetric).real

        # Create time domain
        time = np.linspace(0, len(inverse_signal) / sr, num=len(inverse_signal))

        # Create inverse amplitude plot
        inverse_amplitude_fig = go.Figure()
        inverse_amplitude_fig.add_trace(go.Scatter(x=time, y=inverse_signal, mode='lines', name='Inverse Amplitude'))
        inverse_amplitude_fig.update_layout(
            title='After the IDFT transformation',
            xaxis_title='Time (s)',
            yaxis_title='Amplitude'
        )

        return f'Selected Region: Start = {x0:.4f}, End = {x1:.4f}. Number of points selected: {len(selected_points)}.', fft_fig, inverse_amplitude_fig

    return 'Select a region to see the coordinates.', go.Figure(), go.Figure()

# Define Flask route
@server.route('/')
def index():
    return render_template('index.html')

@server.route('/analyse.html')
def render_analysis():
    return app.index()

# Run the server
if __name__ == '__main__':
    server.run(debug=True)
