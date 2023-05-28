from warnings import filterwarnings
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer

filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

df = pd.read_csv('coklama.csv')

df['Cumle'] = df['Cumle'].str.replace('[^\w\s]', '')
df['Cumle'] = df['Cumle'].str.lower()

vectorizer = TfidfVectorizer()
tf_idf_matrix = vectorizer.fit_transform(df['Cumle'])

data = pd.DataFrame(tf_idf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
data['Target'] = df['Target']

X = data.drop(columns='Target', axis=1)
y = data['Target']

model = RandomForestClassifier().fit(X, y)
print(cross_val_score(model, X, y, cv=5, n_jobs=-1).mean())




