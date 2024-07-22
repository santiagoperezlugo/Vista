# ArcadeAI

## Overview
ArcadeAI is a video game recommendation system that leverages game data from the RAWG API and user interaction data to provide personalized game suggestions. The system uses Flask for the backend and MongoDB for data storage, incorporating machine learning models to enhance recommendation accuracy.

## Installation
To set up the ArcadeAI project, follow these steps:
1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. ```bash
   python run.py
   ```

## Directory
```bash

├── app/                        # Application directory
│   ├── __init__.py             # Initializes the Flask app
│   ├── routes.py               # Defines all routes and endpoints
│   ├── models.py               # Contains machine learning models and data processing
│   ├── services.py             # Handles business logic
│   ├── utils/                  # Utility scripts and helpers
│   │   ├── database.py         # Database connection and operations
│   │   └── fetch_data.py     # Script for fetching and storing data from RAWG API
│   └── analysis/               # Data analysis and visualization
│       └── visualization.py    # Scripts for generating data visualizations
│
├── static/                     # Static files like CSS, JavaScript, and images
├── templates/                  # HTML templates
├── tests/                       # Contains automated tests for the application
├── venv/                       # Virtual environment for the project
├── .gitignore                  # Specifies intentionally untracked files to ignore
├── requirements.txt            # Lists all Python dependencies
└── run.py                      # Entry point for the Flask application
```


## SQL SETUP

```bash

├── USER               
│   ├── userID    
│   ├── Username   
│   ├── Password 

├── Games                      
│   ├── gameID            
│   ├── title              
│   ├── genre            
│   ├── description             
│   ├── publisher
│   ├── release_date

├── UserGamesPlayed                     
│   ├── userID            
│   ├── gameID          
│   ├── playtime            
│   ├── rating      
│   ├── review
```

245 tv shows per page
start on page 137 for more movies