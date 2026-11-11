#!/usr/bin/env bash
PORT="${PORT:-8501}"
python -m streamlit run app.py --server.address 0.0.0.0 --server.port "$PORT" --server.headless true
