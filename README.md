# 🎓 Bulk Certificate Generator

A fast, lightweight web application built with Python and Streamlit that automates the creation of customized certificates in bulk. 

Perfect for event organizers managing college tech fests, TEDx events, webinars, or corporate training sessions, this tool eliminates the need to manually type hundreds of names onto a template.

## ✨ Features
* **No Code Required for Users:** A clean, intuitive drag-and-drop web interface.
* **Live Preview:** Instantly see how the first name on your list looks on the certificate before generating the whole batch.
* **Fully Customizable:** Adjust the Y-coordinate, font size, text color, and word spacing directly from the dashboard.
* **Bulk Export:** Generates all certificates in the background and bundles them into a single, easy-to-download `.zip` file.

## 🚀 Live Demo
https://bulk-certificate-generator.streamlit.app

## 🛠️ How to Use (Web App)
1. Open the web app link.
2. Upload your blank **Template Image** (`.png` or `.jpg`).
3. Upload your **Names List** (`.csv`). *Note: Ensure the column containing the names is titled exactly `Name`.*
4. Upload your preferred **Font File** (`.ttf`).
5. Use the sliders and inputs to adjust the vertical placement (Y-coordinate), font size, and color. Check the Live Preview to ensure perfect alignment.
6. Click **Generate All Certificates** and download your `.zip` file!

## 💻 How to Run Locally (For Developers)
If you want to clone this repository and run it on your own machine, follow these steps:

1. **Clone the repository:**
   git clone https://github.com/rubxn96/BulK-Certificate-Generator.git
2. **Install the required libraries:**
   pip install -r requirements.txt
3. **Launch the app:**
   streamlit run app.py

   
