# Audio Amplitude Analysis Application

## Description

This project is a web application for performing amplitude analysis on audio files. It uses Flask as the web server and Dash for the interactive data visualization components. The application allows users to upload audio files, visualize their amplitude, select regions for DFT (Discrete Fourier Transform) analysis, and view inverse DFT (IDFT) plots.

## Features
- **Upload Audio File**: Users can upload an audio file in formats supported by `librosa`;
- **Amplitude Plot**: The waveform of the uploaded audio file is displayed;
- **Region Selection**: Users can select a region of the audio waveform for detailed analysis;
- **DFT Plot**: Perform FFT on the selected region and visualize the magnitude and phase spectra；
- **IDFT Plot**: The inverse DFT of the selected region is displayed, showing the reconstructed time domain signal.
## Screenshot display
<table>
  <tr>
    <td><img width="1044" alt="Snipaste_2024-03-17_15-46-47" src="https://github.com/kingback156/Amplitude-Analysis/assets/146167978/de46f1e3-c620-43ac-a4ba-445b1281e85e" scale=0.5></td>
    <td><img width="1057" alt="Snipaste_2024-03-17_15-47-37" src="https://github.com/user-attachments/assets/d6fa1c2c-48ad-4493-b353-c2453431bae7" scale=0.5></td>
    <td><img width="1044" alt="Snipaste_2024-03-17_15-46-47" src="https://github.com/user-attachments/assets/d43d3366-8388-4edd-9c76-7d2e8bdd5598" scale=0.5></td>
    <td><img width="1044" alt="Snipaste_2024-03-17_15-46-47" src="https://github.com/user-attachments/assets/0a6450aa-0586-4f05-bf85-e09f17c8512d" scale=0.5></td>
  </tr>
</table>

## Installation and run
**Step 1:** Clone the repository:
```
git clone https://github.com/kingback156/Amplitude-Analysis
```
**Step 2:** Please enter the following command in conda's virtual environment;
```
conda create --name analysis python=3.9
conda activate analysis
pip install -r requirements.txt
```
**Step 3:** Then, start the program with the following command：
```
python app.py
```
Open your browser and visit "http://127.0.0.1:5000" to access the application;

**Step 4:** After entering the homepage, click "Let's try it!" (as shown in Figure 1 above) to enter the analysis interface.
## Test Cases Introduce
- audio_[1,2,3]: The audio of people talking;
- sine_wave_[1,2]: Sine wave signal.
## Callbacks
- `parse_contents`: Parses the uploaded audio file and returns the amplitude plot;
- `set_line_color_update`: Sets the line color update status based on the confirm button clicks;
- `update_amplitude_plot`: Updates the amplitude plot based on the uploaded audio file, confirm button clicks, and rectangle drawing;
- `update_fft_and_inverse_plots`: Performs FFT and inverse FFT on the selected region and updates the corresponding plots.
## A few notes
<img width="478" alt="Snipaste_2024-07-13_20-01-21" src="https://github.com/user-attachments/assets/d31abd3c-bc28-4e07-8341-2c79ed45ce0e">

- Enter the time period you want to check in the audio and click "Confirm";
- You can of course also use the "Draw rectangle" tool to select the `Start Time` and the `End time`；
- All four graphs on the webpage can be viewed in detail using the tool in the upper right corner.;
- The choice of audio data is unimportant, you can use the Test Cases I have provided for testing.

## Contact
If you have any question, please feel free to contact me. E-mail: ltl030529@163.com.
