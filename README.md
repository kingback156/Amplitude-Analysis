# Amplitude Analysis of Audio Files

## Description

This project is a web application built with Flask and Dash that allows users to upload audio files, analyze their amplitude, and visualize the results. Users can also select regions of the audio for detailed frequency spectrum analysis using FFT (Fast Fourier Transform).

## Features
$\bullet$ **Upload Audio Files:** Supports various audio file formats (e.g., WAV, MP3).

$\bullet$ **Amplitude Visualization:** Displays the amplitude of the audio signal over time.

$\bullet$ **Frequency Spectrum Analysis:** Allows users to select regions of the audio for FFT analysis and visualizes the frequency spectrum.

$\bullet$ **Interactive Tools:** Provides tools for zooming, selecting, and drawing on the amplitude plot.
## Screenshot display
<table>
  <tr>
    <td><img width="1044" alt="Snipaste_2024-03-17_15-46-47" src="https://github.com/kingback156/Amplitude-Analysis/assets/146167978/de46f1e3-c620-43ac-a4ba-445b1281e85e" scale=0.5></td>
    <td><img width="1057" alt="Snipaste_2024-03-17_15-47-37" src="https://github.com/kingback156/Amplitude-Analysis/assets/146167978/ad3bc2e0-1465-425a-8ada-a05bd2005837" scale=0.5></td>
    <td><img width="1044" alt="Snipaste_2024-03-17_15-46-47" src="https://github.com/kingback156/Amplitude-Analysis/assets/146167978/76679ccb-1ac0-4605-975e-1538280feed6" scale=0.5></td>
    <td><img width="1057" alt="Snipaste_2024-03-17_15-47-37" src="https://github.com/kingback156/Amplitude-Analysis/assets/146167978/956fc4d5-10c0-451d-99a0-a1489adce802" scale=0.5></td>
  </tr>
</table>

## Installation and run
**Step 1:** Clone the repository:
```
git clone https://github.com/your-username/amplitude-analysis.git
cd amplitude-analysis
```
**Step 2:** Please enter the following command in conda's virtual environment;
```
conda install librosa numpy plotly dash
```
**Step 3:** Then, start the program with the following command：
```
python app.py
```
Open your browser and visit "http://127.0.0.1:5000" to access the application;

**Step 4:** After entering the homepage, click "Let's try it!" (as shown in Figure 1 above) to enter the analysis interface.
## Test Cases Introduce

## Functionality
### Flask Routes
$\bullet$ `/`: Renders the main index page.

$\bullet$ `/analyse.html:` Renders the analysis page where the Dash application is embedded.
### Dash Application
$\bullet$ Layout:

   - Header with title "Amplitude Analysis".

   - Upload button for uploading audio files.

   - Amplitude plot area.

   - Output container for displaying selected region information.

   - FFT plot area for frequency spectrum visualization.

$\bullet$ Callbacks:

- `update_amplitude_plot`: Updates the amplitude plot based on the uploaded audio file.

- `update_fft_plot`: Updates the FFT plot based on the selected region or zoomed area in the amplitude plot.

## A few notes
<img src="https://github.com/kingback156/Amplitude-Analysis/assets/146167978/51f622d3-be52-4531-86be-b8c7babd8189" width="30%" height="30%">

$\bullet$ Both the "Zoom" tool and the "Draw" tool can be used to manipulate selected areas;

$\bullet$ The "Draw" tool allows multiple FFT calculations at one scale;

$\bullet$ The choice of audio data is unimportant, but in my experiments I mainly used this dataset: https://commonvoice.mozilla.org/en/datasets.

## Contact
If you have any question, please feel free to contact me. E-mail: ltl030529@163.com.
