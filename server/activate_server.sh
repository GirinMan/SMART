nohup uvicorn whisper_server:app --host=0.0.0.0 --port=9023 &
nohup uvicorn summary_server:app --host=0.0.0.0 --port=9024 &
nohup uvicorn translation_server:app --host=0.0.0.0 --port=9025 &
nohup uvicorn title_server:app --host=0.0.0.0 --port=9026 &
disown -a
