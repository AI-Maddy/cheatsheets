🐍 **PYTHON PROGRAMMING — Automation, ML & Analytics for Aircraft**
═══════════════════════════════════════════════════════════════════

**Context:** Python for CI/CD, ML inference, data analytics
**Focus:** Automation, TensorFlow Lite, Pandas, FastAPI
**Use Cases:** Build pipelines, recommendations, predictive maintenance

════════════════════════════════════════════════════════════════════

.. contents:: 📑 Quick Navigation
   :depth: 2
   :local:

════════════════════════════════════════════════════════════════════

🎯 **TL;DR — PYTHON IN 60 SECONDS**
────────────────────────────────────

**Aviation Use Cases:**

+-------------------------+--------------------------------------------+
| **Use Case**            | **Libraries**                              |
+=========================+============================================+
| CI/CD Automation        | pytest, GitLab CI, GitHub Actions          |
+-------------------------+--------------------------------------------+
| ML Inference            | TensorFlow Lite, ONNX Runtime              |
+-------------------------+--------------------------------------------+
| Data Analytics          | Pandas, NumPy, Matplotlib                  |
+-------------------------+--------------------------------------------+
| Recommendations         | scikit-learn, collaborative filtering      |
+-------------------------+--------------------------------------------+
| API Services            | FastAPI, Pydantic, uvicorn                 |
+-------------------------+--------------------------------------------+

**Quick Example:**

.. code-block:: python

    # FastAPI microservice
    from fastapi import FastAPI
    
    app = FastAPI()
    
    @app.get("/movies/{movie_id}")
    async def get_movie(movie_id: int):
        return {"id": movie_id, "title": "Top Gun"}

════════════════════════════════════════════════════════════════════

📖 **1. CI/CD AUTOMATION**
══════════════════════════

**1.1 pytest (Testing)**
------------------------

.. code-block:: python

    # test_sensor.py
    import pytest
    from sensor import TemperatureSensor
    
    @pytest.fixture
    def sensor():
        return TemperatureSensor(sensor_id=42)
    
    def test_read_temperature(sensor):
        temp = sensor.read()
        assert 0 <= temp <= 100, "Temperature out of range"
    
    def test_sensor_fault(sensor):
        sensor.simulate_fault()
        with pytest.raises(SensorException):
            sensor.read()
    
    @pytest.mark.parametrize("temp,expected", [
        (-10, "COLD"),
        (25, "NORMAL"),
        (90, "HOT"),
    ])
    def test_temperature_classification(temp, expected):
        assert classify_temp(temp) == expected

**Run tests:**

::

    pytest test_sensor.py -v
    pytest --cov=sensor --cov-report=html

**1.2 GitLab CI Pipeline**
--------------------------

**`.gitlab-ci.yml`:**

.. code-block:: yaml

    stages:
      - test
      - build
      - deploy
    
    test:
      stage: test
      image: python:3.11
      script:
        - pip install -r requirements.txt
        - pytest --cov=. --cov-report=xml
        - pylint src/
      coverage: '/TOTAL.*\s+(\d+%)/'
    
    build:
      stage: build
      script:
        - docker build -t ife-service:$CI_COMMIT_SHA .
        - docker push registry.airline.com/ife-service:$CI_COMMIT_SHA
      only:
        - main
    
    deploy:
      stage: deploy
      script:
        - kubectl set image deployment/ife-service 
              ife=registry.airline.com/ife-service:$CI_COMMIT_SHA
      only:
        - main
      when: manual

**1.3 Deployment Script**
-------------------------

.. code-block:: python

    #!/usr/bin/env python3
    """Deploy IFE service to Kubernetes"""
    
    import subprocess
    import sys
    import argparse
    
    def run_command(cmd):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            sys.exit(1)
        return result.stdout
    
    def deploy(environment, version):
        print(f"Deploying version {version} to {environment}...")
        
        # Build Docker image
        run_command(f"docker build -t ife-service:{version} .")
        
        # Push to registry
        run_command(f"docker push registry.airline.com/ife-service:{version}")
        
        # Update Kubernetes
        run_command(f"kubectl config use-context {environment}")
        run_command(f"kubectl set image deployment/ife-service "
                   f"ife=registry.airline.com/ife-service:{version}")
        
        # Wait for rollout
        run_command("kubectl rollout status deployment/ife-service")
        
        print(f"✅ Deployment complete!")
    
    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("--env", choices=["dev", "staging", "prod"], 
                          required=True)
        parser.add_argument("--version", required=True)
        args = parser.parse_args()
        
        deploy(args.env, args.version)

════════════════════════════════════════════════════════════════════

📖 **2. MACHINE LEARNING INFERENCE**
════════════════════════════════════

**2.1 TensorFlow Lite (On-Device ML)**
--------------------------------------

.. code-block:: python

    import numpy as np
    import tensorflow as tf
    
    class MovieRecommender:
        def __init__(self, model_path):
            # Load TensorFlow Lite model
            self.interpreter = tf.lite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
        
        def predict(self, user_id, viewing_history):
            # Prepare input (user ID + viewing history)
            input_data = np.array([user_id] + viewing_history, 
                                 dtype=np.float32).reshape(1, -1)
            
            # Set input tensor
            self.interpreter.set_tensor(
                self.input_details[0]['index'], 
                input_data
            )
            
            # Run inference
            self.interpreter.invoke()
            
            # Get output (predicted movie IDs)
            output_data = self.interpreter.get_tensor(
                self.output_details[0]['index']
            )
            
            return output_data[0].tolist()
    
    # Usage
    recommender = MovieRecommender("models/movie_recommender.tflite")
    
    user_id = 12345
    viewing_history = [101, 205, 308]  # Movie IDs watched
    
    recommendations = recommender.predict(user_id, viewing_history)
    print(f"Recommended movies: {recommendations[:5]}")  # Top 5

**2.2 ONNX Runtime (Cross-Platform)**
-------------------------------------

.. code-block:: python

    import onnxruntime as ort
    import numpy as np
    
    class ImageClassifier:
        """Classify images from seat cameras (e.g., detect empty seats)"""
        
        def __init__(self, model_path):
            self.session = ort.InferenceSession(model_path)
            self.input_name = self.session.get_inputs()[0].name
        
        def preprocess(self, image):
            # Resize to 224x224, normalize
            image = image.resize((224, 224))
            image_array = np.array(image).astype(np.float32) / 255.0
            image_array = np.transpose(image_array, (2, 0, 1))  # HWC -> CHW
            return np.expand_dims(image_array, axis=0)
        
        def classify(self, image):
            input_data = self.preprocess(image)
            outputs = self.session.run(None, {self.input_name: input_data})
            
            # Get class with highest probability
            class_id = np.argmax(outputs[0])
            confidence = outputs[0][0][class_id]
            
            return class_id, confidence
    
    # Usage
    classifier = ImageClassifier("models/seat_detector.onnx")
    
    from PIL import Image
    image = Image.open("seat_42.jpg")
    class_id, confidence = classifier.classify(image)
    
    classes = ["empty", "occupied"]
    print(f"Seat status: {classes[class_id]} ({confidence:.2%})")

**2.3 Model Optimization**
--------------------------

.. code-block:: python

    import tensorflow as tf
    
    # Convert Keras model to TensorFlow Lite
    def convert_to_tflite(keras_model_path, output_path):
        model = tf.keras.models.load_model(keras_model_path)
        
        # Convert with optimization
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.target_spec.supported_types = [tf.float16]  # Use FP16
        
        tflite_model = converter.convert()
        
        # Save
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        
        # Print size reduction
        import os
        original_size = os.path.getsize(keras_model_path)
        optimized_size = os.path.getsize(output_path)
        reduction = (1 - optimized_size / original_size) * 100
        
        print(f"Model size reduced by {reduction:.1f}%")
        print(f"Original: {original_size / 1024 / 1024:.2f} MB")
        print(f"Optimized: {optimized_size / 1024 / 1024:.2f} MB")

════════════════════════════════════════════════════════════════════

📖 **3. DATA ANALYTICS**
════════════════════════

**3.1 Pandas (Data Manipulation)**
----------------------------------

.. code-block:: python

    import pandas as pd
    import numpy as np
    
    # Load flight data
    df = pd.read_csv("flight_data.csv")
    
    # Basic exploration
    print(df.head())
    print(df.describe())
    print(df.info())
    
    # Filter flights
    long_haul = df[df['duration'] > 6]  # > 6 hours
    
    # Group by route
    route_stats = df.groupby(['origin', 'destination']).agg({
        'passengers': 'mean',
        'delay_minutes': 'mean',
        'satisfaction_score': 'mean'
    })
    
    # Find most delayed routes
    top_delayed = route_stats.nlargest(10, 'delay_minutes')
    
    # Time series analysis
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    monthly_passengers = df.resample('M')['passengers'].sum()
    
    # Pivot table
    pivot = df.pivot_table(
        values='satisfaction_score',
        index='airline',
        columns='cabin_class',
        aggfunc='mean'
    )

**3.2 Data Visualization**
--------------------------

.. code-block:: python

    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Passenger trend over time
    plt.figure(figsize=(12, 6))
    monthly_passengers.plot()
    plt.title("Monthly Passenger Count")
    plt.xlabel("Date")
    plt.ylabel("Passengers")
    plt.savefig("passenger_trend.png")
    
    # Correlation heatmap
    plt.figure(figsize=(10, 8))
    corr = df[['duration', 'delay_minutes', 'satisfaction_score', 
               'ife_usage_minutes']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title("Feature Correlation")
    plt.savefig("correlation.png")
    
    # Distribution plot
    plt.figure(figsize=(10, 6))
    sns.histplot(df['satisfaction_score'], kde=True, bins=20)
    plt.title("Passenger Satisfaction Distribution")
    plt.savefig("satisfaction_dist.png")

**3.3 Predictive Maintenance**
------------------------------

.. code-block:: python

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report
    
    # Load sensor data
    df = pd.read_csv("sensor_logs.csv")
    
    # Feature engineering
    df['temp_delta'] = df['temperature'].diff()
    df['vibration_avg'] = df['vibration'].rolling(window=10).mean()
    
    # Prepare data
    X = df[['temperature', 'vibration', 'pressure', 
            'temp_delta', 'vibration_avg']].dropna()
    y = df['failure_next_24h'].dropna()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    importance = pd.DataFrame({
        'feature': X.columns,
        'importance': clf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(importance)

════════════════════════════════════════════════════════════════════

📖 **4. RECOMMENDATION ENGINE**
════════════════════════════════

**4.1 Collaborative Filtering**
-------------------------------

.. code-block:: python

    import numpy as np
    from scipy.sparse.linalg import svds
    
    class MovieRecommender:
        def __init__(self, ratings_matrix):
            """
            ratings_matrix: users × movies
            """
            self.ratings = ratings_matrix
            self.user_ids = ratings_matrix.index
            self.movie_ids = ratings_matrix.columns
            
            # Perform SVD
            self.train()
        
        def train(self, n_factors=50):
            # Fill NaN with 0
            R = self.ratings.fillna(0).values
            
            # Demean
            user_mean = np.mean(R, axis=1)
            R_demeaned = R - user_mean.reshape(-1, 1)
            
            # SVD
            U, sigma, Vt = svds(R_demeaned, k=n_factors)
            sigma = np.diag(sigma)
            
            # Predicted ratings
            self.predictions = np.dot(np.dot(U, sigma), Vt) + \
                              user_mean.reshape(-1, 1)
        
        def recommend(self, user_id, n=10):
            user_idx = self.user_ids.get_loc(user_id)
            user_predictions = self.predictions[user_idx]
            
            # Get top N unwatched movies
            watched = self.ratings.loc[user_id].dropna().index
            unwatched_idx = [i for i, movie in enumerate(self.movie_ids) 
                            if movie not in watched]
            
            top_n_idx = np.argsort(user_predictions[unwatched_idx])[-n:]
            
            return [self.movie_ids[i] for i in unwatched_idx[top_n_idx]]
    
    # Usage
    ratings = pd.DataFrame({
        'user_1': [5, 3, None, 1],
        'user_2': [4, None, 5, 2],
        'user_3': [None, 2, 4, 5]
    }, index=['movie_A', 'movie_B', 'movie_C', 'movie_D']).T
    
    recommender = MovieRecommender(ratings)
    recommendations = recommender.recommend('user_1', n=2)

**4.2 Content-Based Filtering**
-------------------------------

.. code-block:: python

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    class ContentRecommender:
        def __init__(self, movies_df):
            """
            movies_df: DataFrame with columns [id, title, genre, description]
            """
            self.movies = movies_df
            
            # Combine text features
            self.movies['content'] = (
                self.movies['genre'] + ' ' + 
                self.movies['description']
            )
            
            # TF-IDF vectorization
            self.vectorizer = TfidfVectorizer(stop_words='english')
            self.tfidf_matrix = self.vectorizer.fit_transform(
                self.movies['content']
            )
        
        def recommend(self, movie_id, n=5):
            # Find movie index
            idx = self.movies[self.movies['id'] == movie_id].index[0]
            
            # Compute similarity
            sim_scores = cosine_similarity(
                self.tfidf_matrix[idx], 
                self.tfidf_matrix
            ).flatten()
            
            # Get top N similar movies (excluding itself)
            similar_idx = np.argsort(sim_scores)[-n-1:-1][::-1]
            
            return self.movies.iloc[similar_idx][['id', 'title']]

════════════════════════════════════════════════════════════════════

📖 **5. FASTAPI MICROSERVICES**
════════════════════════════════

**5.1 Basic API**
----------------

.. code-block:: python

    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from typing import List, Optional
    
    app = FastAPI(title="IFE Content API", version="1.0")
    
    class Movie(BaseModel):
        id: int
        title: str
        duration: int
        genre: str
        rating: Optional[float] = None
    
    movies_db = [
        Movie(id=1, title="Top Gun", duration=131, genre="Action", rating=8.5),
        Movie(id=2, title="Avatar", duration=192, genre="Sci-Fi", rating=7.8),
    ]
    
    @app.get("/")
    async def root():
        return {"message": "IFE Content API v1.0"}
    
    @app.get("/movies", response_model=List[Movie])
    async def get_movies(genre: Optional[str] = None):
        if genre:
            return [m for m in movies_db if m.genre == genre]
        return movies_db
    
    @app.get("/movies/{movie_id}", response_model=Movie)
    async def get_movie(movie_id: int):
        for movie in movies_db:
            if movie.id == movie_id:
                return movie
        raise HTTPException(status_code=404, detail="Movie not found")
    
    @app.post("/movies", response_model=Movie, status_code=201)
    async def create_movie(movie: Movie):
        movies_db.append(movie)
        return movie

**Run:**

::

    uvicorn main:app --reload
    # API docs at http://localhost:8000/docs

**5.2 Async Database Operations**
---------------------------------

.. code-block:: python

    from fastapi import FastAPI, Depends
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import select
    
    DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/ife_db"
    
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async def get_db():
        async with AsyncSessionLocal() as session:
            yield session
    
    @app.get("/movies/{movie_id}")
    async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(
            select(Movie).where(Movie.id == movie_id)
        )
        movie = result.scalar_one_or_none()
        
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        return movie

════════════════════════════════════════════════════════════════════

📝 **6. EXAM QUESTIONS**
═════════════════════════

**Q1:** How do you optimize a TensorFlow model for embedded deployment?

**A1:**

1. **Convert to TensorFlow Lite:**

.. code-block:: python

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

2. **Use quantization:**
   - FP16 (50% size reduction)
   - INT8 (75% size reduction, requires calibration)

3. **Prune weights** (remove near-zero weights)

4. **Reduce model complexity** (fewer layers, smaller hidden size)

────────────────────────────────────────────────────────────────────

**Q2:** Explain collaborative filtering vs content-based filtering.

**A2:**

**Collaborative Filtering:**

- Uses user-item interactions (ratings matrix)
- "Users who liked X also liked Y"
- Problem: Cold start (new users/items)

**Content-Based Filtering:**

- Uses item features (genre, description)
- "You liked action movies, here's another action movie"
- Problem: Limited diversity

**Hybrid:** Combine both approaches for best results

════════════════════════════════════════════════════════════════════

✅ **COMPLETION CHECKLIST**
────────────────────────────

- [ ] Write pytest tests with fixtures
- [ ] Set up CI/CD pipeline (GitLab/GitHub)
- [ ] Convert models to TensorFlow Lite
- [ ] Optimize models (quantization, pruning)
- [ ] Use Pandas for data analysis
- [ ] Build recommendation engines
- [ ] Create FastAPI microservices
- [ ] Use Pydantic for data validation
- [ ] Implement async database access
- [ ] Add API documentation (Swagger/OpenAPI)

════════════════════════════════════════════════════════════════════

🌟 **KEY TAKEAWAYS**
════════════════════

1️⃣ **Python excels at automation** → pytest, GitLab CI, deployment scripts

2️⃣ **TensorFlow Lite for edge ML** → Run models on seat units, optimize with 
quantization

3️⃣ **Pandas simplifies data analysis** → Group by, pivot, time series in 
few lines

4️⃣ **Collaborative filtering needs user history** → SVD for matrix factorization

5️⃣ **FastAPI is modern and fast** → Async support, auto-generated docs

6️⃣ **Pydantic validates data** → Type safety for API requests/responses

7️⃣ **Async improves throughput** → Handle 1000s of concurrent requests

════════════════════════════════════════════════════════════════════

**Document Status:** ✅ **PYTHON PROGRAMMING COMPLETE**
**Created:** January 14, 2026
**Coverage:** CI/CD, ML Inference, Analytics, Recommendations, FastAPI

════════════════════════════════════════════════════════════════════
