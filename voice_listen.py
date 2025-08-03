import speech_recognition as sr
import threading
import json
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller .exe """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_config():
    """Load configuration with fallback defaults"""
    try:
        with open(resource_path('config.json'), 'r') as f:
            config = json.load(f)
            return config
    except:
        # Fallback configuration if config.json doesn't exist
        return {
            "voice_enabled": True,
            "microphone_timeout": 5,
            "energy_threshold": 300,
            "dynamic_energy_threshold": True
        }

def test_microphone():
    """Test if microphone is available and working"""
    try:
        recognizer = sr.Recognizer()
        # Try to list available microphones
        mic_list = sr.Microphone.list_microphone_names()
        if not mic_list:
            print("❌ No microphones detected")
            return False
        
        # Try to initialize default microphone
        mic = sr.Microphone()
        with mic as source:
            print("🎤 Testing microphone...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone test successful")
            return True
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        return False

def listen_background(callback):
    """Enhanced voice listening with better error handling and device compatibility"""
    config = load_config()
    
    # Check if voice is enabled in config
    if not config.get("voice_enabled", True):
        print("🔇 Voice input disabled in configuration")
        return
    
    # Test microphone availability
    if not test_microphone():
        print("🔇 Voice input unavailable - microphone issues detected")
        return
    
    recognizer = sr.Recognizer()
    
    # Configure recognizer settings from config
    recognizer.energy_threshold = config.get("energy_threshold", 300)
    recognizer.dynamic_energy_threshold = config.get("dynamic_energy_threshold", True)
    recognizer.pause_threshold = config.get("pause_threshold", 0.8)
    
    try:
        # Try to get the best available microphone
        mic_list = sr.Microphone.list_microphone_names()
        print(f"🎤 Available microphones: {len(mic_list)}")
        
        # Use default microphone
        mic = sr.Microphone()
        
    except Exception as e:
        print(f"❌ Failed to initialize microphone: {e}")
        return

    def listen_loop():
        consecutive_errors = 0
        max_errors = 5
        
        try:
            with mic as source:
                print("🎤 Calibrating microphone...")
                recognizer.adjust_for_ambient_noise(source, duration=2)
                print("✅ Microphone calibrated successfully")
        except Exception as e:
            print(f"❌ Failed to calibrate microphone: {e}")
            return
            
        while consecutive_errors < max_errors:
            try:
                print("🎙️ Listening for voice commands...")
                
                with mic as source:
                    # Listen with timeout to prevent hanging
                    audio = recognizer.listen(
                        source, 
                        timeout=config.get("microphone_timeout", 5),
                        phrase_time_limit=config.get("phrase_time_limit", 5)
                    )
                
                print("🔄 Processing speech...")
                
                # Try Google Speech Recognition
                try:
                    text = recognizer.recognize_google(audio, language="en-US")
                    print(f"🗣️ Heard: '{text}'")
                    callback(text)
                    consecutive_errors = 0  # Reset error counter on success
                    
                except sr.UnknownValueError:
                    print("🤔 Could not understand audio")
                    consecutive_errors = 0  # This isn't really an error
                    
                except sr.RequestError as e:
                    print(f"🌐 Speech recognition service error: {e}")
                    consecutive_errors += 1
                    
            except sr.WaitTimeoutError:
                # Timeout is normal, not an error
                print("⏰ Listening timeout (normal)")
                consecutive_errors = 0
                
            except Exception as e:
                print(f"❌ Voice listening error: {e}")
                consecutive_errors += 1
                
                if consecutive_errors >= max_errors:
                    print(f"🔇 Too many consecutive errors ({max_errors}), stopping voice input")
                    break
        
        print("🔇 Voice input stopped")

    # Start listening in background thread
    voice_thread = threading.Thread(target=listen_loop, daemon=True)
    voice_thread.start()
    print("🎙️ Voice input system started")
