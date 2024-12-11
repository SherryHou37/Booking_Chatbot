import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report


# 文本预处理函数
def preprocess_text(text):
    # 转为小写
    text = text.lower()

    # 去除标点符号和特殊字符
    text = re.sub(r'[^\w\s]', '', text)

    # 去除停用词
    stop_words = set(stopwords.words('english'))
    tokens = text.split()
    filtered_tokens = [word for word in tokens if word not in stop_words]
    text = " ".join(filtered_tokens)

    # 词干提取
    stemmer = PorterStemmer()
    text = " ".join([stemmer.stem(word) for word in text.split()])

    return text


# 读取训练数据（例如，意图和相应的文本）
train_file_path = 'data/Intents.xlsx'
df_train = pd.read_excel(train_file_path)

# 初始化训练数据
all_phrases = []
all_intents = []

# 将训练数据中的"Text"列拆分并与意图关联
for index, row in df_train.iterrows():
    phrases = row['Text'].split(',')  # 将每个句子通过逗号分隔
    intent = row['Intent']

    for phrase in phrases:
        all_phrases.append(preprocess_text(phrase.strip()))  # 添加预处理后的句子
        all_intents.append(intent)  # 添加意图

# 使用 TF-IDF 向量化文本
vectorizer = TfidfVectorizer(ngram_range=(1, 3))
X_train = vectorizer.fit_transform(all_phrases)


def sentiment_analysis(user_input):
    # 定义积极和消极词汇
    positive_words = ["happy", "good", "great", "excited", "joy", "love", "amazing", "wonderful", "fantastic", "glad"]
    negative_words = ["sad", "bad", "terrible", "angry", "hate", "horrible", "upset", "disappointed", "depressed"]

    # 如果文本中包含积极词汇，返回积极情感回应
    if any(re.search(r'\b' + re.escape(word) + r'\b', user_input) for word in positive_words):
        return "I'm glad you're feeling good!"

    # 如果文本中包含消极词汇，返回消极情感回应
    if any(re.search(r'\b' + re.escape(word) + r'\b', user_input) for word in negative_words):
        return "I'm sorry you're feeling this way. How can I help?"

    # 如果没有匹配的积极或消极词汇，返回 None
    return None


# 意图预测函数
def predict_intent(user_input, threshold=0.3):
    # 预处理用户输入
    user_input_processed = preprocess_text(user_input)

    # 将用户输入转换为相同的 TF-IDF 向量
    input_vector = vectorizer.transform([user_input_processed])

    # 计算用户输入与训练文本之间的余弦相似度
    cosine_similarities = cosine_similarity(input_vector, X_train).flatten()

    # 获取最大相似度
    max_similarity = np.max(cosine_similarities)

    # 如果最大相似度低于阈值，则返回"Other"
    if max_similarity < threshold:
        return "Other"

    # 返回与训练数据中最相似的意图
    best_match_index = np.argmax(cosine_similarities)
    predicted_intent = all_intents[best_match_index]

    # 返回预测的意图
    return predicted_intent




