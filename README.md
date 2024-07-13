# Amplitude Analysis of Audio Files

## Description

This project is a web application for performing amplitude analysis on audio files. It uses Flask as the web server and Dash for the interactive data visualization components. The application allows users to upload audio files, visualize their amplitude, select regions for DFT (Discrete Fourier Transform) analysis, and view inverse DFT (IDFT) plots.

## Features
- **Upload Audio File**: Users can upload an audio file in formats supported by `librosa`;
- **Amplitude Plot**: The waveform of the uploaded audio file is displayed;
- **Region Selection**: Users can select a region of the audio waveform for detailed analysis;
- **DFT Plot**: The frequency domain representation of the selected region is shown;
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
conda install flask dash numpy
conda install -c conda-forge librosa
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
## Functionality
### Flask Routes
- `/`: Renders the main index page.
- `/analyse.html:` Renders the analysis page where the Dash application is embedded.
### Dash Application
- Layout:
   - Header with title "Amplitude Analysis".
   - Upload button for uploading audio files.
   - Amplitude plot area.
   - Output container for displaying selected region information.
   - FFT plot area for frequency spectrum visualization.
   - IDFT plot area.

- Callbacks:
- `update_amplitude_plot`: Updates the amplitude plot based on the uploaded audio file.
- `update_fft_plot`: Updates the DFT plot based on the selected region or zoomed area in the amplitude plot.
- `update_inverse_amplitude_plot`: Updates the IDFT plot based on the selected region.

## A few notes
<table>
  <tr>
    <td><img width="1044" alt="Snipaste_2024-03-17_15-46-47" src="https://github.com/kingback156/Amplitude-Analysis/assets/146167978/f9a5d4e6-9000-44e7-a0a0-44d3fd8c7210" width="100px"></td>
    <td><img width="1057" alt="Snipaste_2024-03-17_15-47-37" src="https://github.com/user-attachments/assets/21f6de2f-fdfb-4fc4-8dbe-e991f2039b58" width="100px"></td>
  </tr>
</table>

- Enter the time period you want to check in the audio and click "Confirm";
- All three images on the webpage can be viewed in detail using the tool in the upper right corner.;
- The choice of audio data is unimportant, you can use the Test Cases I have provided for testing.

## Contact
If you have any question, please feel free to contact me. E-mail: ltl030529@163.com.
