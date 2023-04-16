import json

import httpx
import openai
import pinecone
from ipdb import set_trace

from api.clients import database
from api.settings import settings

## OPENAI - GEN EMBEDDINGS

openai.api_key = settings.OPENAI_API_KEY

MODEL = "text-embedding-ada-002"

res = openai.Embedding.create(
    input=[
        "Sample document text goes here",
        "there will be several phrases in each batch",
    ],
    engine=MODEL,
)
# extract embeddings to a list
embeds = [record["embedding"] for record in res["data"]]  # pyright: ignore

## PINECONE - CREATE INDEX

pinecone.init(
    api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENVIRONMENT
)

# check if 'openai' index already exists (only create index if not)
if "openai" not in pinecone.list_indexes():
    pinecone.create_index("openai", dimension=len(embeds[0]))
# # connect to index

index = pinecone.Index("openai")

## LOAD DATASET

await database.connect()

recs = await database.fetch_many("select * from listings")


### create embeds

from tqdm.auto import tqdm

batch_size = 32  # process everything in batches of 32
for i in tqdm(range(0, len(recs), batch_size)):
    # set end position of batch
    i_end = min(i + batch_size, len(recs))
    # get batch of lines and IDs
    lines_batch = [rec["description"] for rec in recs[i : i + batch_size]]
    ids_batch = [str(n) for n in range(i, i_end)]
    # create embeddings
    res = openai.Embedding.create(input=lines_batch, engine=MODEL)
    embeds = [record["embedding"] for record in res["data"]]  # pyright: ignore
    # prep metadata and upsert batch
    meta = []
    for rec in recs[i : i + batch_size]:
        meta_data = {k: v or "" for k, v in rec.items()}
        meta.append(meta_data)
    # meta = [
    #     {
    #         k: v
    #         for k, v in rec.items()
    #         if k not in ["id", "listing_images", "address_images", "details"]
    #     }
    #     for rec in recs[i : i + batch_size]
    # ]
    # meta = [{"text": line} for line in lines_batch]
    to_upsert = zip(ids_batch, embeds, meta)
    # upsert to Pinecone
    index.upsert(vectors=list(to_upsert))


### QUERYING

query = "I wannt to live somewhere with lots of natural sunlight"

xq = openai.Embedding.create(input=query, engine=MODEL)["data"][0]["embedding"]
