# TryMe: Automatic JSON Builder for Model Inference

TryMe is a user-friendly tool that automates the process of generating JSON objects required for making predictions with machine learning models. It simplifies the input preparation for non-technical users, such as business teams or product managers, enabling them to leverage the predictive capabilities of machine learning models without requiring in-depth technical knowledge.

## Features

- Automatic generation of JSON objects for model inference
- User-friendly interface for uploading training data and obtaining JSON outputs
- Customizable JSON object structure to match specific model's input requirements

## Getting Started

### Prerequisites

- Python 3.8.x
- Required Python packages listed in `requirements.txt`

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/jegun19/try-me.git
   cd try-me
   ```

2. Install the required Python packages:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Install the frontend dependencies:

   ```bash
   cd frontend
   npm install
   ```

### Usage

1. Run the backend server:

   ```bash
   cd backend
   python main.py
   ```

2. Run the frontend server:

   ```bash
   cd frontend
   npm run dev
   ```

3. Access the application in your web browser at `http://localhost:5173/`
4. Upload your training data file in CSV format using the provided interface.
5. Modify the feature values using the input fields accordingly. Or better, use the `Copy Value` button!
6. Use the generated JSON object with your machine learning model for making predictions.
7. For detailed usage and walkthrough, please refer to the [Wiki](https://github.com/jegun19/try-me/wiki) section of this repo.

### License

This project is licensed under the MIT License.
