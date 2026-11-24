# Environment Audit Report

> Generated: 2026-11-18  
> Project: Source-Locked / Test-Locked Coding Agent Evaluation

## 1. System & Hardware
- **OS**: macOS (Darwin 24.3.0, arm64)
- **CPUs**: 8 vCPUs
- **Total Memory**: 16 GB host / 7.75 GB allocated to Docker

## 2. Docker Daemon & Runtimes
- **Docker Client Version**: 29.9.0 (Context: desktop-linux)
- **Docker Server Engine**: 29.9.2
- **Docker Desktop Version**: 4.97.0
- **Base Images Cached**:
  - `aisiuk/inspect-tool-support:latest` (ID: `8571d6fb1d34`, Size: 1.47 GB)
  - `python:3.12-bookworm` (Cached and verified)
  - `python:3.12-slim` (ID: `5e2bdb1b0d54`)
  - `swebench/sweb.eval.x86_64.django_1776_django-10554:latest` (ID: `3e799bbbf2aa`, 4.18 GB)

## 3. Python Environment & Pinned Commits
- **Virtualenv**: `external/impossiblebench/.venv`
- **Python Version**: 3.12.14
- **Key Installed Packages**:
  - `inspect-ai`: 0.3.291
  - `inspect-evals`: 0.1.1
  - `swebench`: 5.0.2
  - `openai`: 3.55.0
  - `pytest`: 9.2.0
  - `pandas`: 2.2.3
  - `datasets`: 3.3.2
- **Upstream Repositories**:
  - `external/impossiblebench`: HEAD commit `d4f9a149db2b9cec0fed7bab01d91c07ee10aca2`
    - Source: `https://github.com/safety-research/impossiblebench`

## 4. Evaluated Model Endpoint
- **Actor Model ID**: `deepseek-v4.1-flash`
- **Endpoint Protocol**: OpenAI-compatible chat completion with Tool Calling & Reasoning Content
- **Base URL**: `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- **Client Configuration**: `client_timeout=300.0`, `max_subprocesses=1`

## 5. Security & Isolation Compliance
- No API keys committed or printed in logs/reports (read strictly via `.env`).
- All agent executions constrained within isolated Docker containers (non-root `devuser`, root-owned locked files with `chmod 444`).
