# 🛡️ Real-time Fraud Detection System with MLOps Pipeline

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)
[![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-orange.svg)](https://prometheus.io/)

A production-ready machine learning system for real-time credit card fraud detection, featuring automated model training, API deployment, and comprehensive monitoring.

## 🌟 Key Features

- **Real-time Fraud Detection**: REST API endpoint for instant fraud prediction
- **MLOps Pipeline**: Automated data preprocessing, model training, and evaluation
- **Model Comparison**: Evaluates Random Forest, Logistic Regression, and Decision Tree
- **Production Monitoring**: Prometheus metrics and Grafana dashboards
- **Containerized Deployment**: Docker Compose for easy deployment
- **High Performance**: Sub-100ms prediction latency

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker Desktop
- 8GB RAM minimum

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/MrKunalSharma/fraud-detection-mlops.git
cd fraud-detection-mlops
```

2. **Run with Docker Compose**

```bash
docker-compose up --build
```

3. **Access the services**
- API Documentation: http://localhost:8000/docs
- Prometheus Metrics: http://localhost:9090
- Grafana Dashboard: http://localhost:3000 (admin/admin)

## 💻 Local Development

1. **Create virtual environment**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Download dataset**

```bash
python download_data.py
```

4. **Train models**

```bash
python -m src.data_preprocessing
python -m src.model_training
```

5. **Run API locally**

```bash
python run_api.py
```

## 📊 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| Random Forest | 99.95% | 95.12% | 82.93% | 88.61% | 0.9146 |
| Logistic Regression | 99.91% | 91.67% | 73.33% | 81.48% | 0.8666 |
| Decision Tree | 99.89% | 86.21% | 83.33% | 84.75% | 0.9165 |

## 🔄 API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Fraud Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "Time": 0,
       "V1": -1.359807,
       "V2": -0.072781,
       "V3": 2.536347,
       "V4": 1.378155,
       "V5": -0.338321,
       "V6": 0.462388,
       "V7": 0.239599,
       "V8": 0.098698,
       "V9": 0.363787,
       "V10": 0.090794,
       "V11": -0.551600,
       "V12": -0.617801,
       "V13": -0.991390,
       "V14": -0.311169,
       "V15": 1.468177,
       "V16": -0.470401,
       "V17": 0.207971,
       "V18": 0.025791,
       "V19": 0.403993,
       "V20": 0.251412,
       "V21": -0.018307,
       "V22": 0.277838,
       "V23": -0.110474,
       "V24": 0.066928,
       "V25": 0.128539,
       "V26": -0.189115,
       "V27": 0.133558,
       "V28": -0.021053,
       "Amount": 149.62
     }'
```

### Response

```json
{
  "prediction": 0,
  "probability": 0.02,
  "risk_level": "Low",
  "message": "Transaction seems legitimate"
}
```

## 📈 Monitoring & Metrics

The system tracks:
- Total predictions count by type (fraud/legitimate)
- Prediction latency histogram
- API request success/error rates
- Model performance metrics

Access Grafana dashboards to visualize:
- Real-time fraud detection rate
- Transaction risk distribution
- API response times
- System health metrics

## 🗂️ Project Structure

```
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
```

## 🔧 Configuration

Key configurations in `src/config.py`:
- Model hyperparameters
- API settings
- Monitoring intervals
- Data paths

## 📝 Key Learnings

This project demonstrates:
- End-to-end ML pipeline development
- REST API design with FastAPI
- Containerization with Docker
- Monitoring with Prometheus/Grafana
- MLOps best practices

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Dataset: [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- Inspired by real-world fraud detection systems
- Built with modern MLOps practices

## 📧 Contact

**Kunal Sharma**

- LinkedIn: [https://www.linkedin.com/in/kunal-sharma-1a8457257/](https://www.linkedin.com/in/kunal-sharma-1a8457257/)
- Email: kunalsharma13579kunals@gmail.com
- GitHub: [https://github.com/MrKunalSharma](https://github.com/MrKunalSharma)
- Project Link: [https://github.com/MrKunalSharma/fraud-detection-mlops](https://github.com/MrKunalSharma/fraud-detection-mlops)

⭐ If you found this project helpful, please consider giving it a star!