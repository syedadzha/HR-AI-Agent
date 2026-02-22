---
name: code-reviewer
description: Performs comprehensive code reviews, security audits, and architectural sanity checks. Use when the user requests a code review, PR audit, or wants to ensure adherence to project standards for FastAPI and Nuxt 3.
---

# Code Reviewer

## Overview
This skill transforms Gemini CLI into a senior software engineer specialized in the HR Policy RAG stack (FastAPI, Nuxt 3, Qdrant). It provides systematic reviews focusing on security, performance, type safety, and architectural consistency.

## Workflow

### 1. Context Gathering
Before reviewing, ensure you understand the purpose of the code:
- Identify if it's a new feature, bug fix, or refactor.
- Check relevant documentation (e.g., `GEMINI.md`, API specs).

### 2. Systematic Review
Follow the [Checklist](references/checklist.md) to ensure all critical areas are covered:
- **Security:** Check for hardcoded secrets, injection vulnerabilities, and proper authentication.
- **Architecture:** Verify alignment with the RAG service-oriented architecture.
- **Quality:** Ensure type hints (Python) and TypeScript types are used correctly.
- **Testing:** Verify that tests are included and cover edge cases.

### 3. Standards Compliance
Verify adherence to the [Project Standards](references/standards.md). This includes:
- Nuxt 3 patterns (composables, directory structure).
- FastAPI best practices (dependency injection, Pydantic models).
- Structured logging (using `logger_config.py`).

### 4. Output Generation
Provide the review in a structured format:
- **Summary:** High-level assessment.
- **Critical Issues:** Blocking bugs or security flaws.
- **Suggestions:** Non-blocking improvements for readability or performance.
- **Positive Findings:** What was done well.

## Example Requests
- "Review this PR for security issues."
- "Audit `backend/services/chat_service.py` for RAG best practices."
- "Does this new frontend component follow our Nuxt 3 standards?"
