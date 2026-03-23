---
name: debug-image-generation
description: Investigate image generation issues using Logfire observability data and code analysis
---

# Debugging Image Generation Issues

When a user reports that image generation is not working, approach this like a real production debugging scenario.

## Start with observability (Logfire)

Use Logfire MCP tools to look at recent `/generate` requests.

Focus on:
- recent traces
- response status
- any fields indicating whether an image was actually returned

Do not assume there is an error just because the user reports one. Verify what the system is actually doing.

If needed, use `query_run` to explore recent traces and identify patterns.

---

## Look for mismatches or anomalies

Pay attention to situations where:
- requests succeed (HTTP 200)
- but the output doesn’t match what the frontend likely expects

For example:
- responses that are technically successful
- but missing expected fields (like an image URL)

These kinds of issues often don’t show up as explicit errors.

---

## Use logs to guide deeper investigation

If logs suggest something is “successful but odd”:
- inspect the backend response structure
- compare it with how the frontend is using the response

Avoid jumping into the code immediately — let the logs guide where to look.

---

## Determine the root cause

Explain clearly:
- what the system is returning
- why that doesn’t align with what the frontend expects
- why logs may look normal even though the user sees a failure

---

## Suggest a fix

Recommend a practical fix, such as:
- aligning response structure between backend and frontend
- adding validation for required fields
- improving error handling for invalid responses

---

## Important principles

- Treat Logfire as the primary source of truth
- Validate assumptions using real data before reasoning about code
- Think step-by-step like an engineer debugging a production issue
- Explain reasoning, not just conclusions