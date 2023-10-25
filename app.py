from flask import Flask, render_template, request
import os
import kaggle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
os.environ['KAGGLE_CONFIG_DIR'] = os.getcwd()

def textSplit(text):
    return ' '.join([word.lower() for word in text.split() if any(c.isalpha() for c in word) or any(c.isdigit() for c in word)])

def check_plagiarism(desc1, desc2):
    desc1 = textSplit(desc1)
    desc2 = textSplit(desc2)

    vectorizer = TfidfVectorizer().fit_transform([desc1, desc2])
    vectors = vectorizer.toarray()

    cosine_sim = cosine_similarity(vectors)
    return cosine_sim[0][1]

@app.route('/', methods=['GET', 'POST'])
def index():
    default_desc1 = ""
    default_desc2 = ""
 
    if os.path.exists('my_dataset_directory/sample_data.csv'):
        data = pd.read_csv('my_dataset_directory/sample_data.csv')
        default_desc1 = data['original_text'][0]
        default_desc2 = data['modified_text'][0]

    if request.method == 'POST':
        desc1 = request.form['desc1']
        desc2 = request.form['desc2']

        similarity_score = check_plagiarism(desc1, desc2)
        result = f"Similarity percentage: {similarity_score*100:.2f}%"
        
        if similarity_score > 0.4:
            result += ". Possible plagiarism detected!"
        else:
            result += ". Descriptions seem to be original."
        return render_template('index.html', result=result, default_desc1=desc1, default_desc2=desc2)

    return render_template('index.html', result=None, default_desc1=default_desc1, default_desc2=default_desc2)

@app.route('/download_dataset')
def download_dataset():
    kaggle.api.authenticate()
    dataset_identifier = "yufengsui/mobile-games-ab-testing"
    download_path = "my_dataset_directory"
    kaggle.api.dataset_download_files(dataset_identifier, path=download_path, unzip=True)
    return "Dataset downloaded and extracted successfully!"

if __name__ == '__main__':
    app.run(debug=True)


#dummy data for testing:-

#Blockchain technology, often heralded as a revolutionary system of decentralized trust, stands poised to redefine myriad sectors, from finance to supply chain management. This decentralized ledger's inherent security, derived from cryptographic hashing and consensus algorithms, ensures transparent and immutable transactions. Such features not only challenge traditional intermediaries like banks but also offer avenues for enhanced peer-to-peer interactions. As blockchain evolves, its capacity to foster trust in a decentralized manner has vast implications, particularly in ensuring transactional integrity and reshaping the dynamics of data ownership. This research seeks to delineate the potential transformative impact of blockchain, emphasizing its role in democratizing trust.

#Often lauded as a groundbreaking mechanism for distributed trust, blockchain technology is on the cusp of revolutionizing various industries, spanning from finance to logistics. This distributed ledger, fortified by cryptographic techniques and consensus protocols, guarantees clarity and permanence in transactions. These attributes not only contest the roles of conventional middlemen like banks but also pave the way for enriched direct interactions between parties. As the technology behind blockchain matures, its ability to establish trust in a distributed setting bears significant potential, especially in safeguarding transaction authenticity and redefining the paradigms of data rights. This study aims to unpack the transformative potential of blockchain, underscoring its significance in decentralizing trust.

#Artificial Intelligence (AI) is progressively shaping the frontier of technological advancements, orchestrating a new era of human-machine collaboration. Rooted in intricate algorithms and neural network architectures, AI systems replicate and, in certain domains, surpass human cognitive functions. Their adaptability and learning capacities promise not just efficiency gains, but also novel solutions to longstanding problems in sectors like healthcare, finance, and environmental conservation. However, with these advances comes a responsibility to address ethical quandaries, from bias in decision-making to job displacement concerns. This research endeavors to explore the multifaceted dimensions of AI, elucidating its transformative potential while weighing the ethical imperatives it necessitates.

