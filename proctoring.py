import tensorflow as tf
import cv2
from keras import models
from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
import mediapipe as mp
import time
import os
from datetime import datetime

proc_time = 30

RECORDINGS_DIR = "recordings"
ALERTS_DIR = "alerts"


if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)
if not os.path.exists(ALERTS_DIR):
    os.makedirs(ALERTS_DIR)


model = tf.keras.models.load_model("Models\Final Model Used in Real Time Prediction\CNN_Model2.keras")  
print("Model loaded:", model.summary())  


mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

class ProctoringApp:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user
        self.cap = None
        self.bg_color = "#2E2F5B"
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill="both")
        self.video_label = tk.Label(self.main_frame, bg=self.bg_color)
        self.video_label.pack(fill="both", expand=True)

        
        self.start_button = tk.Button(self.main_frame, text="Start Proctoring", command=self.capture_and_predict, bg="#F4A259", fg="white", font=("Helvetica", 14))
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(self.main_frame, text="Stop Proctoring", command=self.stop_proctoring, bg="#F4A259", fg="white", font=("Helvetica", 14), state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        
        self.back_button = tk.Button(self.main_frame, text="Back to Menu", command=self.go_back_to_menu, bg="#F4A259", fg="white", font=("Helvetica", 14))
        self.back_button.pack(pady=10)

        self.is_proctoring = False  

    def capture_and_predict(self):
        """Capture 2 images per second for 15 seconds, predict, and record video."""
        self.cap = cv2.VideoCapture(0)
        
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        timestamp = int(time.time())
        video_filename = f"proctoring_{timestamp}.avi"
        video_path = os.path.join(RECORDINGS_DIR, video_filename)
        out = cv2.VideoWriter(video_path, fourcc, 2.0, (640, 480))

        predictions = []
        allowed_images = []
        not_allowed_image = None
        captured_images = []

        start_time = time.time()  

       
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_proctoring = True 

        
        while time.time() - start_time < proc_time and self.cap.isOpened() and self.is_proctoring:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture an image")
                continue

          
            out.write(frame)

           
            face, processed_face = self.detect_and_preprocess_face(frame)
            if face is not None and processed_face is not None:
            
                x_min, y_min, x_max, y_max = face
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                
                captured_images.append(frame)

             
                prediction = model.predict(processed_face)
                class_index = np.argmax(prediction)
                confidence = prediction[0][class_index] * 100
                label = "Allowed" if class_index == 0 else "Not Allowed"
                predictions.append(label)

                
                cv2.putText(frame, f"{label} ({confidence:.2f}%)", (x_min, y_min - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0) if label == "Allowed" else (0, 0, 255), 2)

                if label == "Allowed":
                    allowed_images.append(frame)
                else:
                    not_allowed_image = frame  
                    self.store_cheating_alert()  
            else:
                print("No face detected.")

          
            img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.video_label.imgtk = img
            self.video_label.config(image=img)
            self.root.update()

        self.cap.release()
        out.release()  
        cv2.destroyAllWindows()

        end_time = time.time() 

       
        self.save_recording_metadata(video_filename, start_time, end_time)

      
        if not_allowed_image is not None:
            print("Aggregate Result: Not Allowed")
            self.display_aggregated_result("Not Allowed", not_allowed_image)
        else:
            print("Aggregate Result: Allowed")
            self.display_aggregated_result("Allowed", allowed_images[0] if allowed_images else None)

        print(f"Recording saved at: {video_path}")
        self.notify_recordings_page(video_filename)  

    
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.is_proctoring = False  

    def stop_proctoring(self):
        """Stop the proctoring process immediately."""
        print("Proctoring stopped.")
        self.is_proctoring = False  
        self.cap.release()  
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)

    def detect_and_preprocess_face(self, frame):
        """Detect face using Mediapipe, expand bounding box, and preprocess for CNN."""
        with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            results = face_detection.process(rgb_frame)

            if results.detections:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    h, w, _ = frame.shape
                    x_min = int(bboxC.xmin * w)
                    y_min = int(bboxC.ymin * h)
                    x_max = int((bboxC.xmin + bboxC.width) * w)
                    y_max = int((bboxC.ymin + bboxC.height) * h)

                    
                    padding_h = int(0.3 * (y_max - y_min))
                    padding_w = int(0.15 * (x_max - x_min))
                    x_min = max(0, x_min - padding_w)
                    y_min = max(0, y_min - padding_h)
                    x_max = min(w, x_max + padding_w)
                    y_max = min(h, y_max + padding_h)

                   
                    face_rgb = rgb_frame[y_min:y_max, x_min:x_max]
                    face_rgb = cv2.resize(face_rgb, (128, 128))
                    face_rgb = np.expand_dims(face_rgb, axis=0)
                    return (x_min, y_min, x_max, y_max), face_rgb

        return None, None

    def display_aggregated_result(self, result, image_to_display):
        """Display the aggregated result."""        
        if image_to_display is not None:
            img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(image_to_display, cv2.COLOR_BGR2RGB)))
            self.video_label.imgtk = img
            self.video_label.config(image=img)

        print(f"Final Result: {result}")

    def go_back_to_menu(self):
        """Navigate back to the menu page."""
        from menu import MenuPage  
        MenuPage(self.root, self.logged_in_user)

    def store_cheating_alert(self):
        """Store an alert for 'Possible Cheating'."""        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_message = f"Alert: Possible Cheating detected at {timestamp}"

      
        alert_filename = f"cheating_alert_{timestamp.replace(':', '_').replace(' ', '_')}.txt"
        alert_path = os.path.join(ALERTS_DIR, alert_filename)

        with open(alert_path, 'w') as alert_file:
            alert_file.write(alert_message)
        
        print(f"Alert saved: {alert_message}")

    def save_recording_metadata(self, video_filename, start_time, end_time):
        """Save metadata about the recording including start and end times."""        
        metadata_filename = f"{video_filename}.txt"
        metadata_path = os.path.join(RECORDINGS_DIR, metadata_filename)

        start_datetime = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')

        with open(metadata_path, 'w') as metadata_file:
            metadata_file.write(f"Start Time: {start_datetime}\n")
            metadata_file.write(f"End Time: {end_datetime}\n")

        print(f"Recording metadata saved: {metadata_path}")

    def notify_recordings_page(self, filename):
        """Notify recordings.py about the newly saved video."""        
        print(f"New recording '{filename}' added to the recordings directory.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Proctoring App")  
    root.geometry("800x600")  
    app = ProctoringApp(root, logged_in_user="test_user")  
    root.mainloop()  
