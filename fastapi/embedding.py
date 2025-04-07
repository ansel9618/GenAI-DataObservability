from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

def embed_log(log: dict):
    summary = (
        f"[{log['level']}] {log['service']} | {log['environment']} | "
        f"{log['job_name']} > {log['step_name']} | {log['message']} | "
        f"status={log['status_code']}, duration={log['duration_ms']}ms, "
        f"tags={','.join(log.get('tags', []))}"
    )
    return model.encode(summary).tolist()
