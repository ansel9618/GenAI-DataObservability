from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2") #all-MiniLM-L6-v2 has 384 dimensions, use all-mpnet-base-v2 with 768 dimensions as alternative (worse)
'''
def embed_log(log: dict):
    summary = " | ".join([
        f"level={log['level']}",
        f"service={log['service']}",
        f"env={log['environment']}",
        f"job={log['job_name']}",
        f"step={log['step_name']}",
        f"message={log['message']}",
        f"status={log['status_code']}",
        f"duration={log['duration_ms']}ms",
        f"tags={','.join(log.get('tags', []))}",
    ])
    return model.encode(summary).tolist()

'''
# more natural sentence
def embed_log(log: dict):
    summary = (
        f"In the '{log['environment']}' environment, the '{log['job_name']}' job "
        f"started step '{log['step_name']}' using service '{log['service']}'. "
        f"The log level was '{log['level']}' and the message was: {log['message']}. "
        f"Status code: {log['status_code']}, duration: {log['duration_ms']} milliseconds. "
        f"Tags: {', '.join(log.get('tags', [])) or 'none'}."
    )
    return model.encode(summary).tolist()

