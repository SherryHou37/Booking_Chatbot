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
train_file_path = 'test data/TestIntents.xlsx'
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

# 意图预测函数
def predict_intent(user_input, threshold=0.5):
    # 预处理用户输入
    user_input = preprocess_text(user_input)

    # 将用户输入转换为相同的 TF-IDF 向量
    input_vector = vectorizer.transform([user_input])

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

    return predicted_intent

# 读取测试数据（假设包含测试文本和真实意图）
test_file_path = 'test data/TestIntents1.xlsx'  # 这是你的测试文件
df_test = pd.read_excel(test_file_path)

# 初始化变量来计算准确率
correct_predictions = 0
total_predictions = len(df_test)

# 初始化预测和真实意图列表
predicted_intents_all = []
true_intents_all = []

# 遍历测试集进行预测
for index, row in df_test.iterrows():
    user_input = row['Text']
    true_intent = row['Intent']

    # 预测意图
    predicted_intent = predict_intent(user_input)

    predicted_intents_all.append(predicted_intent)
    true_intents_all.append(true_intent)

    # 如果预测意图与真实意图相同，则计为正确预测
    if predicted_intent == true_intent:
        correct_predictions += 1

# 计算准确率
accuracy = correct_predictions / total_predictions
print(f"Accuracy: {accuracy * 100:.2f}%")

# 生成混淆矩阵
cm = confusion_matrix(true_intents_all, predicted_intents_all, labels=list(df_train['Intent'].unique()) + ['Other'])

# 使用Seaborn绘制热图
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=list(df_train['Intent'].unique()) + ['Other'],
            yticklabels=list(df_train['Intent'].unique()) + ['Other'])
plt.xlabel('Predicted Intent')
plt.ylabel('True Intent')
plt.title('Confusion Matrix')
plt.show()

# 输出分类报告（包括精确度、召回率、F1 分数）
print("Classification Report:")
print(classification_report(true_intents_all, predicted_intents_all, target_names=list(df_train['Intent'].unique()) + ['Other'], labels=list(df_train['Intent'].unique()) + ['Other']))
