# Code Function Description
This document provides a detailed description of each function in the Flask and Dash application for amplitude analysis of audio files.
## 1. Flask Initialization and Routes
`server = Flask(__name__)`

- **Purpose:** Initializes the Flask server.
- **Description:** This statement creates an instance of the Flask application, which will be used to handle HTTP requests and manage the routing of the application.
  
`@server.route('/')`
- **Purpose:** Defines the route for the home page.
- **Description:** This route renders the home page of the application by returning the index.html template when the root URL (/) is accessed.

`@server.route('/analyse.html')`
- **Purpose:** Defines the route for the analysis page.
- **Description:** This route renders the Dash application when the /analyse.html URL is accessed, integrating the Dash application into the Flask framework.
## 2. Dash Initialization and Layout
`app = Dash(__name__, server=server, url_base_pathname='/analyse/')`
- **Purpose:** Initializes the Dash application.
- **Description:** This creates an instance of the Dash application and links it to the Flask server, setting the base URL path for the Dash app to /analyse/.

`app.layout`
- **Purpose:** Defines the layout of the Dash application. 
- **Description:** Specifies the structure and components of the Dash application, including:
  - An H1 header displaying "Amplitude Analysis".
  - A file upload component for uploading audio files.
  - A placeholder for the amplitude plot (dcc.Graph).
  - A container for displaying messages.
  - A placeholder for the FFT plot (dcc.Graph).
## 3. Utility Functions

`parse_contents(contents)`
- Purpose: Parses the uploaded audio file and generates the amplitude plot.
- Parameters:
  - contents: The contents of the uploaded audio file in base64 format.
- Returns: A tuple containing a Plotly figure of the amplitude plot, the time array, the amplitude array, and the sample rate.
- Description:
  - Decodes the base64-encoded audio file.
  - Uses librosa to load the audio data and sample rate.
  - Calculates the amplitude of the audio signal.
  - Generates a time array corresponding to the audio data.
  - Creates an initial Plotly figure for the amplitude plot with time on the x-axis and amplitude on the y-axis.

## 4. Dash Callbacks
`@app.callback(Output('amplitude-plot', 'figure'), [Input('upload-audio', 'contents')])`
`def update_amplitude_plot(contents)`
- Purpose: Updates the amplitude plot when an audio file is uploaded.
- Parameters:
  - contents: The contents of the uploaded audio file in base64 format.
- Returns: An updated Plotly figure for the amplitude plot.
- Description:
  - Checks if an audio file has been uploaded.
  - Calls parse_contents to generate the amplitude plot.
  - Updates the Dash graph component with the new amplitude plot.
`@app.callback([Output('output-container', 'children'), Output('fft-plot', 'figure')], [Input('amplitude-plot', 'relayoutData')], [State('amplitude-plot', 'figure')])`
`def update_fft_plot(relayoutData, figure)`
- Purpose: Updates the FFT plot based on user interactions with the amplitude plot.
- Parameters:
  - relayoutData: Data about the user's interactions with the amplitude plot (e.g., drawing rectangles, zooming).
  - figure: The current state of the amplitude plot.
- Returns: A message about the selected region and an updated FFT plot.
- Description:
  - Checks if the amplitude plot contains valid data.
  - Handles user interactions:
    - Drawing rectangles: Extracts the selected time range, applies a window function to the selected amplitude points, computes the FFT, and updates the FFT plot.
    - Zooming: Similar to drawing rectangles, extracts the selected time range, applies a window function, computes the FFT, and updates the FFT plot.
  - Updates the amplitude plot to include the user's selected shapes or zoom range.
  - Returns a message indicating the selected region and an updated FFT plot.
## 5. Handling FFT Computation and Plotting
`FFT Computation within update_fft_plot(relayoutData, figure)`
- Purpose: Computes the Fast Fourier Transform (FFT) of the selected amplitude data points.
- Process:
  - Rectangle Selection:
    - When the user draws a rectangle on the amplitude plot, the function extracts the time range (x0 to x1).
    - It identifies the indices of the amplitude data points within this time range.
    - Applies a Hanning window to the selected amplitude points to reduce spectral leakage.
    - Computes the FFT of the windowed amplitude data points.
    - Extracts the positive frequency components and normalizes the FFT result.
    - Removes the DC component (zero-frequency term).
    - Generates a Plotly figure for the FFT plot with frequency on the x-axis and amplitude on the y-axis.
  - Zoom Interaction:
    - Similar to rectangle selection, the function handles zoom interactions by extracting the time range from relayoutData.
    - Identifies the indices of the amplitude data points within the zoomed time range.
    - Applies a Hanning window, computes the FFT, and generates the FFT plot.
- Returns:
  - A message indicating the start and end of the selected time range and the number of selected data points.
  - An updated FFT plot showing the frequency spectrum of the selected data points.
