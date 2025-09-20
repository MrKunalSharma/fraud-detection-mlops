# 🛡️ Real-time Fraud Detection System with MLOps Pipeline

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)
[![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-orange.svg)](https://prometheus.io/)

A production-ready machine learning system for real-time credit card fraud detection, featuring automated model training, API deployment, and comprehensive monitoring.

![Fraud Detection Dashboard](monitoring_dashboard.png)

## 🌟 Key Features

- **Real-time Fraud Detection**: REST API endpoint for instant fraud prediction
- **MLOps Pipeline**: Automated data preprocessing, model training, and evaluation
- **Model Comparison**: Evaluates Random Forest, Logistic Regression, and Decision Tree
- **Production Monitoring**: Prometheus metrics and Grafana dashboards
- **Containerized Deployment**: Docker Compose for easy deployment
- **High Performance**: Sub-100ms prediction latency

## 🏗️ Architecture



                
┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ FastAPI App │────▶│ Prometheus │────▶│ Grafana │
│ (Port 8000) │ │ (Port 9090) │ │ (Port 3000) │
└─────────────────┘ └──────────────────┘ └─────────────────┘
│
▼
┌─────────────────┐
│ ML Model │
│ (Scikit-learn) │
└─────────────────┘




## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker Desktop
- 8GB RAM minimum

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/fraud-detection-mlops.git
cd fraud-detection-mlops


          
Run with Docker Compose

          

bash


docker-compose up --build


                
Access the services
API Documentation: http://localhost:8000/docs
Prometheus Metrics: http://localhost:9090
Grafana Dashboard: http://localhost:3000 (admin/admin)
💻 Local Development
Create virtual environment

          

bash


python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac


                
Install dependencies

          

bash


pip install -r requirements.txt


                
Download dataset

          

bash


python download_data.py


                
Train models

          

bash


python -m src.data_preprocessing
python -m src.model_training


                
Run API locally

          

bash


python run_api.py


                
📊 Model Performance
Model	Accuracy	Precision	Recall	F1-Score	ROC-AUC
Random Forest	99.95%	95.12%	82.93%	88.61%	0.9146
Logistic Regression	99.91%	91.67%	73.33%	81.48%	0.8666
Decision Tree	99.89%	86.21%	83.33%	84.75%	0.9165
🔄 API Usage
Health Check

          

bash


curl http://localhost:8000/health


                
Fraud Prediction

          

bash


curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "Time": 0,
       "V1": -1.359807,
       "V2": -0.072781,
       ...
       "Amount": 149.62
     }'


                
Response

          

json


{
  "prediction": 0,
  "probability": 0.02,
  "risk_level": "Low",
  "message": "Transaction seems legitimate"
}


                
📈 Monitoring & Metrics
The system tracks:

Total predictions count by type (fraud/legitimate)
Prediction latency histogram
API request success/error rates
Model performance metrics
Access Grafana dashboards to visualize:

Real-time fraud detection rate
Transaction risk distribution
API response times
System health metrics
🗂️ Project Structure



fraud-detection-mlops/
├── src/
│   ├── config.py              # Configuration settings
│   ├── data_preprocessing.py  # Data pipeline
│   ├── model_training.py      # Model training logic
│   ├── model_serving.py       # FastAPI application
│   └── monitoring.py          # Metrics tracking
├── models/                    # Trained models
├── data/                      # Dataset storage
├── docker/                    # Docker configurations
├── monitoring/                # Prometheus & Grafana configs
├── tests/                     # Unit tests
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container definition
└── docker-compose.yml         # Multi-container setup


          
🔧 Configuration
Key configurations in src/config.py:

Model hyperparameters
API settings
Monitoring intervals
Data paths
📝 Key Learnings
This project demonstrates:

End-to-end ML pipeline development
REST API design with FastAPI
Containerization with Docker
Monitoring with Prometheus/Grafana
MLOps best practices
🤝 Contributing
Fork the repository
Create feature branch (git checkout -b feature/AmazingFeature)
Commit changes (git commit -m 'Add AmazingFeature')
Push to branch (git push origin feature/AmazingFeature)
Open Pull Request
📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Dataset: Kaggle Credit Card Fraud Detection
Inspired by real-world fraud detection systems
Built with modern MLOps practices
📧 Contact
Your Kunal Sharma - https://www.linkedin.com/in/kunal-sharma-1a8457257/ - kunalsharma13579kunals@gmail.com

Project Link: https://github.com/yourusername/fraud-detection-mlops

⭐ If you found this project helpful, please consider giving it a star!




### Additional Files to Create:

1. **Create `.gitignore`** (update the existing one):


          
Python
pycache/
*.py[cod]
.env
venv/
env/

Data
data/raw/
*.csv
*.parquet

Models
models/.pkl
models/.pt

IDEs
.vscode/
.idea/

OS
.DS_Store
Thumbs.db

Docker
*.log




2. **Create `LICENSE`** file (MIT License):


          
MIT License

Copyright (c) 2024 Kunal Sharma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...