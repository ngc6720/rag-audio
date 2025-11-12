"""
Core logic of the feature: functions using the feature models.
"""

from .models import (
    ITranscriber,
    IEmbedder,
    IVectors,
    IChat,
    TranscriptUploadResponse,
    TranscriptSearchResponse,
    ScoredChunks,
)
from .implementations.embedder import write_to_json_file


def create_context_from_audio_file(
    name: str,
    filename: str,
    file: bytes,
    transcriber: ITranscriber,
    embedder: IEmbedder,
    vectors: IVectors,
) -> TranscriptUploadResponse:
    # Get text from the provided audio
    transcript = transcriber.get_transcription_from_file(
        file_name=filename,
        file=file,
    )
    # Embeddings are created directly from transcript segments
    # Bit simplistic and might need an intermediate structure
    embeddings = embedder.embed([s.text for s in transcript.segments])
    # Then save the vectors to db
    # NB: embeddings and segments are paired lists
    name = vectors.create(
        collection_name=name,
        embeddings=embeddings,
        segments=transcript.segments,
    )
    return {"transcript": transcript, "name": name}


def generate_query_with_context(
    q: str,
    name: str,
    embedder: IEmbedder,
    vectors: IVectors,
    chat: IChat,
) -> TranscriptSearchResponse:
    embeddings_prompt = embedder.embed_single(q)
    scored = vectors.search(name, embeddings_prompt)
    # Add adjacent segments to give more context
    padded = ScoredChunks()
    for c in scored.chunks:
        batch = vectors.getPoints(
            name,
            [
                c.id - 4,
                c.id - 3,
                c.id - 2,
                c.id - 1,
                c.id,
                c.id + 1,
                c.id + 2,
                c.id + 3,
                c.id + 4,
            ],
        )
        for chunk in batch.chunks:
            padded.chunks.append(chunk)
    # Format retrieval to object for prompt
    formated_ctx = {
        "chunks": [
            {"text": chunk.payload.text, "time": chunk.payload.start}
            for chunk in padded.chunks
        ]
    }
    prompt = make_prompt(ctx=str(formated_ctx), q=q)
    chat_response = chat.complete(prompt=prompt)
    return {"answer": chat_response}


def make_prompt(ctx: str, q: str):
    return f"""
    You are provided with a context coming from an audio transcript.
    Each "chunk" of the list represents a relevant part for you to use as context.
    In each "chunk", there is a "time" timestamp in seconds corresponding to the "text" that you should use to situate your quotes in time.

    CONTEXT:
    ---------------------
    {ctx}
    ---------------------
    Given the context information and not prior knowledge, answer the query.
    Query: {q}
    Answer:
    """
