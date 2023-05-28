from warnings import filterwarnings
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

def preProcessing(data: str):
    df = pd.read_csv('coklama.csv')
    new_data = pd.DataFrame({'Cumle': [data], 'Target': None})

    df = pd.concat([df, new_data], ignore_index=True)

    df['Cumle'] = df['Cumle'].str.replace('[^\w\s]', '')
    df['Cumle'] = df['Cumle'].str.lower()

    vectorizer = TfidfVectorizer()
    tf_idf_matrix = vectorizer.fit_transform(df['Cumle'])

    data = pd.DataFrame(tf_idf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

    return [data.iloc[-1]]