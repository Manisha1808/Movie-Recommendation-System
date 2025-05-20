# 🎬 Movie Recommendation System

A simple and visually appealing movie recommendation web app built using **Flask**, **MySQL**, and **scikit-learn**, with a dark-themed UI.

## 📌 Features

- Search for any movie and get similar movie recommendations.
- Recommendations are based on textual similarity of movie overviews using **TF-IDF** and **cosine similarity**.
- Fuzzy matching is used to tolerate minor typos in movie titles.
- Recommendations include **genres**, **ratings**, and **release dates**.
- Data is loaded dynamically from a **MySQL database**.

## 🧰 Technologies Used

- Python 3
- Flask
- MySQL
- Pandas
- scikit-learn
- fuzzywuzzy
- HTML & CSS (dark-themed UI)



## 🚀 How to Run

### 1. Clone the Repository
### 2. Create and Activate a Virtual Environment
### 3. Install Dependencies

```bash
git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system ```


```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```bash
pip install -r requirements.txt

