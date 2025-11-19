from fastapi import UploadFile

async def upload_file_to_oss(file: UploadFile) -> str:
    # Stub: in real implementation, stream to Alibaba OSS bucket
    # For MVP, return a predictable URL-like string
    return f"oss://mock-bucket/{file.filename}"
