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
    dcc.Graph(id='amplitude-plot', config={
        'modeBarButtonsToAdd': ['drawrect', 'eraseshape', 'zoom', 'zoomIn', 'zoomOut', 'resetScale2d'],
        'displaylogo': False
    }),
    html.Div(id='output-container', style={'textAlign': 'center', 'fontSize': 20}),
    dcc.Graph(id='fft-plot', config={
        'modeBarButtonsToAdd': ['drawrect', 'eraseshape', 'zoom', 'zoomIn', 'zoomOut', 'resetScale2d'],
        'displaylogo': False
    }),
    dcc.Graph(id='inverse-amplitude-plot')  # Placeholder for inverse FFT plot
])

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    audio_data, sr = librosa.load(io.BytesIO(decoded), sr=None)
    
    # Calculate the amplitude
    amplitude = np.abs(audio_data)
    time = np.linspace(0, len(audio_data) / sr, num=len(audio_data))

    # Convert amplitude and time to standard Python float
    amplitude = amplitude.astype(float)
    time = time.astype(float)

    # Create the initial amplitude plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=amplitude, mode='lines', name='Amplitude'))
    fig.update_layout(
        title='Amplitude of Audio Signal',
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
     Output('fft-plot', 'figure')],
    [Input('amplitude-plot', 'relayoutData')],
    [State('amplitude-plot', 'figure')]
)
def update_fft_plot(relayoutData, figure):
    if figure is None or 'data' not in figure or len(figure['data']) == 0:
        return 'Upload an audio file to analyze.', go.Figure()

    time = np.array(figure['data'][0]['x'])
    amplitude = np.array(figure['data'][0]['y'])
    sr = 1 / (time[1] - time[0])

    if relayoutData:
        # Handling draw rectangle tool
        if 'shapes' in relayoutData:
            shape = relayoutData['shapes'][-1]
            if 'x0' in shape and 'x1' in shape:
                x0 = shape['x0']
                x1 = shape['x1']
                if x0 > x1:
                    x0, x1 = x1, x0  # Ensure x0 is less than x1

                # Extract points within the selected range
                selected_indices = np.where((time >= x0) & (time <= x1))[0]
                selected_points = amplitude[selected_indices]

                # Apply a window function to the selected points
                window = np.hanning(len(selected_points))
                selected_points_windowed = selected_points * window

                # Compute FFT of the selected points
                N = len(selected_points_windowed)
                yf_segment = np.fft.fft(selected_points_windowed)
                xf_segment = np.fft.fftfreq(N, 1 / sr)

                # Only keep the positive frequency part
                idx = np.arange(1, N // 2)
                xf_segment = xf_segment[idx]
                yf_segment = np.abs(yf_segment[idx]) / N  # Normalize FFT result

                # Remove DC component
                yf_segment[0] = 0

                # Create FFT plot
                fft_fig = go.Figure()
                fft_fig.add_trace(go.Scatter(x=xf_segment, y=yf_segment, mode='lines', name='FFT'))
                fft_fig.update_layout(
                    title='Frequency Spectrum of the Selected Points',
                    xaxis_title='Frequency (Hz)',
                    yaxis_title='Amplitude',
                    xaxis=dict(range=[0, 5000])
                )

                # Update the amplitude plot to keep the shapes
                figure['layout']['shapes'] = relayoutData['shapes']

                # Return the updated plots
                return f'Selected Region: Start = {x0:.2f}, End = {x1:.2f}. Number of points selected: {len(selected_indices)}.', fft_fig
        
        # Handling zoom tool
        if 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
            x0 = relayoutData['xaxis.range[0]']
            x1 = relayoutData['xaxis.range[1]']
            
            # Extract points within the selected range
            selected_indices = np.where((time >= x0) & (time <= x1))[0]
            selected_points = amplitude[selected_indices]

            # Apply a window function to the selected points
            window = np.hanning(len(selected_points))
            selected_points_windowed = selected_points * window

            # Compute FFT of the selected points
            N = len(selected_points_windowed)
            yf_segment = np.fft.fft(selected_points_windowed)
            xf_segment = np.fft.fftfreq(N, 1 / sr)

            # Only keep the positive frequency part
            idx = np.arange(1, N // 2)
            xf_segment = xf_segment[idx]
            yf_segment = np.abs(yf_segment[idx]) / N  # Normalize FFT result

            # Remove DC component
            yf_segment[0] = 0

            # Create FFT plot
            fft_fig = go.Figure()
            fft_fig.add_trace(go.Scatter(x=xf_segment, y=yf_segment, mode='lines', name='FFT'))
            fft_fig.update_layout(
                title='Frequency Spectrum of the Selected Points',
                xaxis_title='Frequency (Hz)',
                yaxis_title='Amplitude'
            )

            # Return the updated plots
            return f'Selected Region: Start = {x0:.2f}, End = {x1:.2f}. Number of points selected: {len(selected_indices)}.', fft_fig

    return 'Select a region to see the coordinates.', go.Figure()

@app.callback(
    Output('inverse-amplitude-plot', 'figure'),
    [Input('fft-plot', 'relayoutData')],
    [State('fft-plot', 'figure')]
)
def update_inverse_amplitude_plot(relayoutData, figure):
    if figure is None or 'data' not in figure or len(figure['data']) == 0:
        return go.Figure()

    freq = np.array(figure['data'][0]['x'])
    amplitude = np.array(figure['data'][0]['y'])

    if relayoutData:
        if 'shapes' in relayoutData:
            shape = relayoutData['shapes'][-1]
            if 'x0' in shape and 'x1' in shape:
                x0 = shape['x0']
                x1 = shape['x1']
                if x0 > x1:
                    x0, x1 = x1, x0  # Ensure x0 is less than x1

                # Extract points within the selected range
                selected_indices = np.where((freq >= x0) & (freq <= x1))[0]
                selected_points = amplitude[selected_indices]

                # Create a symmetric spectrum for inverse FFT
                yf_symmetric = np.zeros(len(freq) * 2, dtype=complex)
                yf_symmetric[selected_indices] = selected_points * len(freq)
                yf_symmetric[-selected_indices] = selected_points * len(freq)

                # Compute inverse FFT
                inverse_signal = np.fft.ifft(yf_symmetric).real

                # Create time domain
                time = np.linspace(0, len(inverse_signal), num=len(inverse_signal))

                # Create inverse amplitude plot
                inverse_amplitude_fig = go.Figure()
                inverse_amplitude_fig.add_trace(go.Scatter(x=time, y=inverse_signal, mode='lines', name='Inverse Amplitude'))
                inverse_amplitude_fig.update_layout(
                    title='Reconstructed Amplitude from Frequency Spectrum',
                    xaxis_title='Time',
                    yaxis_title='Amplitude'
                )

                return inverse_amplitude_fig
        
        # Handling zoom tool
        if 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
            x0 = relayoutData['xaxis.range[0]']
            x1 = relayoutData['xaxis.range[1]']
            
            # Extract points within the selected range
            selected_indices = np.where((freq >= x0) & (freq <= x1))[0]
            selected_points = amplitude[selected_indices]

            # Create a symmetric spectrum for inverse FFT
            yf_symmetric = np.zeros(len(freq) * 2, dtype=complex)
            yf_symmetric[selected_indices] = selected_points * len(freq)
            yf_symmetric[-selected_indices] = selected_points * len(freq)

            # Compute inverse FFT
            inverse_signal = np.fft.ifft(yf_symmetric).real

            # Create time domain
            time = np.linspace(0, len(inverse_signal), num=len(inverse_signal))

            # Create inverse amplitude plot
            inverse_amplitude_fig = go.Figure()
            inverse_amplitude_fig.add_trace(go.Scatter(x=time, y=inverse_signal, mode='lines', name='Inverse Amplitude'))
            inverse_amplitude_fig.update_layout(
                title='Reconstructed Amplitude from Frequency Spectrum',
                xaxis_title='Time',
                yaxis_title='Amplitude'
            )

            return inverse_amplitude_fig

    return go.Figure()

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
