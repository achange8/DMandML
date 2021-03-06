# 特徴量の抽出とベクトル量子化とコサイン類似度
# 特徴量：AKAZE
import cv2.cv2 as cv
import numpy as np
import datetime
import scipy.cluster
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_features():
    # read images
    img0 = cv.imread('./imagedata/image0.jpg')
    img1 = cv.imread('./imagedata/image1.jpg')
    img2 = cv.imread('./imagedata/image2.jpg')
    img3 = cv.imread('./imagedata/image3.jpg')

    detector = cv.AKAZE_create()

    kp0, des0 = detector.detectAndCompute(img0, None)
    kp1, des1 = detector.detectAndCompute(img1, None)
    kp2, des2 = detector.detectAndCompute(img2, None)
    kp3, des3 = detector.detectAndCompute(img3, None)

    return des0, des1, des2, des3

# データをクラスタリング


def create_docs(des0, des1, des2, des3, kk):
    desall = np.vstack((des0, des1, des2, des3))
    npdesall = np.array(desall, dtype='float64')
    # ベクトル量子化
    codebook, destortion = scipy.cluster.vq.kmeans(
        npdesall, kk, iter=30, thresh=1e-06)
    code0, dist0 = scipy.cluster.vq.vq(des0, codebook)
    code1, dist1 = scipy.cluster.vq.vq(des1, codebook)
    code2, dist2 = scipy.cluster.vq.vq(des2, codebook)
    code3, dist3 = scipy.cluster.vq.vq(des3, codebook)
    print("------------------------------")
    print("kk = ", kk)
    print("画像0のコード数 =", len(code0))
    print("画像1のコード数 =", len(code1))
    print("画像2のコード数 =", len(code2))
    print("画像3のコード数 =", len(code3))
    # docsを作成する
    codeall = [code0, code1, code2, code3]
    docs = []
    for codes in codeall:
        words = ""
        for code in codes:
            words = words + " " + str(code)
        docs.append(words)
    return docs

# TF-IDF, cos類似度を計算


def calculate_similarity(docs):
    # create object
    npdocs = np.array(docs)
    vectorizer = TfidfVectorizer(norm=None, smooth_idf=False)
    vecs = vectorizer.fit_transform(npdocs)
    # TF-IDF
    tfidfs = vecs.toarray()
    # cos類似度
    similarity = cosine_similarity(tfidfs)

    return similarity

# print result


def print_result(result):
    docno = ["画像0 ", "画像1 ", "画像2 ", "画像3 "]
    print("画像No", end='')
    for n in docno:
        print("%6s  " % n, end='')
    print()
    for n, res in zip(docno, result):
        print("%s" % n, end='')
        for r in res:
            print("%9.4f" % r, end='')
        print()

    return


def main(i):
    des0, des1, des2, des3 = extract_features()
    # return err when kk = 10;
    # input kk=100 ~ 10
    kk = 100-(i*10)
    docs = create_docs(des0, des1, des2, des3, kk)
    similarity = calculate_similarity(docs)
    print_result(similarity)


# start
if __name__ == "__main__":
    for i in range(0, 10):
        start_time = datetime.datetime.now()
        main(i)
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print("経過時間 =", elapsed_time)
        print("すべて完了 !!!")
