# Google Meet Bot

A Python bot that automates joining Google Meet meetings and plays audio during the session.

## Features

- Automatically logs into Google Meet using provided credentials.
- Joins a specified meeting link.
- Plays audio through the meeting using virtual audio routing.

## Requirements

- Python 3.x
- Required Python packages (listed in `requirements.txt`):
  - playwright
  - python-dotenv
  - (any other dependencies)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/google-meet-bot.git
   cd google-meet-bot
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `.\venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your Google credentials and meeting link:
   ```plaintext
   GOOGLE_EMAIL=your_email@example.com
   GOOGLE_PASSWORD=your_password
   GOOGLE_MEET=your_meeting_link
   ```

## Audio Routing Setup

### macOS Users

To route audio through Google Meet using BlackHole, follow these steps:

#### Step 1: Install BlackHole

1. **Download BlackHole**:
   - Go to the [BlackHole GitHub page](https://github.com/ExistentialAudio/BlackHole).
   - Click on the "Releases" section and download the latest version (usually a `.dmg` file).

2. **Install BlackHole**:
   - Open the downloaded `.dmg` file.
   - Follow the installation instructions:
     - Drag the BlackHole icon to your Applications folder.

#### Step 2: Create an Aggregate Device

1. **Open Audio MIDI Setup**:
   - Go to `Applications > Utilities > Audio MIDI Setup`.

2. **Create an Aggregate Device**:
   - Click the "+" button in the bottom left corner and select **Create Aggregate Device**.
   - In the right panel, check both your microphone (the physical one you use) and **BlackHole 2ch**.
   - This allows you to use your microphone while also routing audio through BlackHole.

#### Step 3: Set Up Audio Preferences

1. **Set BlackHole as Default Input**:
   - Go to `System Preferences > Sound`.
   - Under the **Input** tab, select **BlackHole 2ch**.

2. **Set Your Output Device**:
   - Under the **Output** tab, select your regular speakers or headphones.
   - If you want to hear the audio yourself while it plays in Google Meet, you can create a **Multi-Output Device** that includes both BlackHole and your speakers:
     - In **Audio MIDI Setup**, click the "+" button and select **Create Multi-Output Device**.
     - Check both **BlackHole 2ch** and your regular output device.

#### Step 4: Configure Google Meet

1. **Open Google Meet**:
   - Join a meeting.

2. **Select BlackHole as Microphone**:
   - Click on the three dots in the bottom right corner of the Meet window.
   - Go to **Settings** > **Audio**.
   - Set the microphone to **BlackHole 2ch**.

#### Step 5: Test the Setup

1. **Play Audio**:
   - Use your bot to play audio. Ensure that the audio is routed through BlackHole.
   - For example, in your bot code, you might have:
   ```python
   os.system(f'afplay {audio_path}')  # This plays the audio through BlackHole
   ```

2. **Check in Google Meet**:
   - Ask someone in the meeting if they can hear the audio.
   - Adjust the volume as necessary.

### Windows Users

To route audio through Google Meet using VB-Audio Virtual Cable, follow these steps:

1. **Install VB-Audio Virtual Cable**:
   - Download from the [VB-Audio website](https://vb-audio.com/Cable/).
   - Follow the installation instructions.

2. **Set Up Virtual Cable**:
   - Set the virtual cable as your default playback device in your sound settings.
   - Ensure that Google Meet is set to use the virtual cable as the microphone.

### Linux Users

To route audio through Google Meet using PulseAudio, follow these steps:

1. **Install PulseAudio**:
   - Most Linux distributions come with PulseAudio pre-installed. If not, install it using your package manager.
   - For example, on Ubuntu, you can run:
     ```bash
     sudo apt-get install pulseaudio
     ```

2. **Set Up Loopback**:
   - Use the `pactl` command to create a loopback from your audio output to the microphone input:
     ```bash
     pactl load-module module-loopback
     ```

3. **Configure Google Meet**:
   - Ensure that Google Meet is set to use the PulseAudio input as the microphone.

## Usage

1. **Run the bot**:
   ```bash
   python src/bot.py
   ```

2. **Audio Playback**:
   - Ensure that the audio file you want to play is in the correct format (e.g., .mp3 or .wav) and located in the specified directory.

## Troubleshooting

- If you encounter issues with audio not being heard in Google Meet, ensure that:
  - The correct virtual audio device is set as the microphone input in Google Meet settings.
  - The audio file is playing correctly through the bot.


