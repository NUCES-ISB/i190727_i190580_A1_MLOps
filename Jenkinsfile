pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Checkout code from repository
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                // Install required Python packages
                bat 'python -m pip install --upgrade pip'
                bat 'pip install pylint'
                bat 'pip install black'
                bat 'pip install pytest'
                bat 'pip install -r requirements.txt'
                echo 'STARTING TEST NOW'
            }
        }
        stage('Format Code with Black') {
            steps {
                // Run Black formatter on app.py
                bat 'black app.py'
                echo 'Black has formatted app.py'
            }
        }
        stage('Analyse Code with Pylint') {
            steps {
                // Run Pylint on app.py
                bat 'pylint app.py'
                echo 'TEST WENT VIRAL'
            }
        }
        stage('Test 404 Page') {
            steps {
                // Run Pytest on app.py
                bat 'python -m pytest'
                echo "TEST PASSED"
            }
        }
    }
    options {
        // Fail fast, abort pipeline as soon as any stage fails
        failFast true
    }
}

