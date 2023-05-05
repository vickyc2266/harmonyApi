import json
import os

import numpy as np
import requests

from harmony.matching.matcher import match_instruments_with_function
from harmony.schemas.requests.text import MatchBody, Question
from harmony.schemas.responses.text import MatchResponse
from pydantic import parse_obj_as

headers = {
    'Content-Type': 'application/json'
}

mhc_questions = []
mhc_all_metadatas = []
mhc_embeddings = np.zeros((0, 0))

print("Folder is", str(os.getcwd()))

try:
    data_path = "."
    with open(data_path + "/mhc_questions.json",
              "r", encoding="utf-8") as f:
        for l in f:
            mhc_question = Question.parse_raw(l)
            mhc_questions.append(mhc_question)
    with open(
            data_path + "/mhc_all_metadatas.json",
            "r", encoding="utf-8") as f:
        for l in f:
            mhc_meta = json.loads(l)
            mhc_all_metadatas.append(mhc_meta)
    with open(data_path + "/mhc_embeddings.npy",
              "rb") as f:
        mhc_embeddings = np.load(f)
except:
    print("Could not load MHC embeddings ", str(os.getcwd()))

print("Loaded embeddings", len(mhc_embeddings))


def vectorisation_function(all_texts: np.ndarray) -> np.ndarray:
    response = requests.post("https://uroe37564sqhuuczvqitupuv440zcdgf.lambda-url.eu-west-2.on.aws",
                             headers=headers,
                             json={"texts": all_texts})
    all_vectors = np.asarray(response.json())
    return all_vectors


def lambda_handler(event, context):
    print(json.dumps(event))

    match_body = parse_obj_as(MatchBody, json.loads(event["body"]))

    instruments = match_body.instruments
    query = match_body.query

    all_questions, similarity_with_polarity, query_similarity = match_instruments_with_function(instruments, query,
                                                                                                vectorisation_function,
                                                                                                mhc_questions,
                                                                                                mhc_all_metadatas,
                                                                                                mhc_embeddings)

    matches_jsonifiable = similarity_with_polarity.tolist()

    if query_similarity is not None:
        query_similarity = query_similarity.tolist()

    response = MatchResponse(questions=all_questions, matches=matches_jsonifiable, query_similarity=query_similarity)

    return response.json()