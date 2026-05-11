# 🤝 Contributing to Zero to SRE

First off, **thank you** for considering contributing to Zero to SRE! Every contribution — from fixing a typo to adding an entire module — helps the community learn and grow.

---

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How Can I Contribute?](#-how-can-i-contribute)
- [Content Style Guide](#-content-style-guide)
- [Module Template](#-module-template)
- [Pull Request Process](#-pull-request-process)
- [Reporting Issues](#-reporting-issues)

---

## 📜 Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## 🚀 How Can I Contribute?

### 📝 Documentation
- Fix typos, grammar, or unclear explanations
- Add or improve architecture diagrams (Mermaid.js preferred)
- Translate content to other languages

### 💻 Code & Scripts
- Add working scripts with comments and error handling
- Add configuration examples (Terraform, K8s manifests, etc.)
- Improve existing scripts with best practices

### 🧪 Hands-on Labs
- Create step-by-step exercises with real tools
- Add project-based labs that tie multiple concepts together
- Include cleanup/teardown instructions

### 🐛 Issues & Suggestions
- Report outdated information
- Suggest new topics or modules
- Identify broken links or missing content

---

## ✍️ Content Style Guide

### Markdown Formatting
- Use **emojis** in headings for visual scanning
- Use **tables** for comparisons and structured data
- Use **collapsible sections** (`<details>`) for optional deep-dives
- Use **Mermaid.js** for diagrams (no external image files needed)
- Use **code blocks** with proper language identifiers

### Writing Tone
- **Beginner-friendly explanations**, production-grade depth
- Write as a senior engineer mentoring a junior
- Use active voice and direct language
- Include "Pro Tips" and "Common Pitfalls" callouts

### Code Standards
- All scripts must include:
  - Header comment with description and usage
  - Inline comments explaining non-obvious logic
  - Error handling (don't just `set -e` and hope)
  - Usage examples in comments or accompanying README
- Use consistent naming: `snake_case` for files, descriptive names

### Tool References
- Always mention **multiple tools** when possible (avoid vendor lock-in)
- Default to open-source tools
- Note when something is cloud-provider specific

---

## 📐 Module Template

Every module should follow this structure:

```markdown
# 📖 Module Title

> One-line description of what this module covers.

## 📋 Table of Contents
- [Conceptual Overview](#conceptual-overview)
- [Key Concepts](#key-concepts)
- [Hands-on Lab](#hands-on-lab)
- [Real-world Use Case](#real-world-use-case)
- [Common Pitfalls](#common-pitfalls)
- [Further Reading](#further-reading)

## 📖 Conceptual Overview
What this is, why it matters, and how it works.
Include a Mermaid diagram if applicable.

## 🔑 Key Concepts
Detailed breakdown of important terms and ideas.

## 🔧 Hands-on Lab
### Prerequisites
### Step 1: ...
### Step 2: ...
### Cleanup

## 🏢 Real-world Use Case
How top companies use this in production.

## ⚠️ Common Pitfalls
| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|

## 📚 Further Reading
- [Link 1](url) — Description
- [Link 2](url) — Description
```

---

## 🔄 Pull Request Process

1. **Fork** the repository
2. **Create a branch** with a descriptive name:
   ```bash
   git checkout -b feature/add-kubernetes-module
   git checkout -b fix/typo-in-observability
   ```
3. **Make your changes** following the style guide
4. **Test your content**:
   - Ensure Markdown renders correctly
   - Verify all links work
   - Run any scripts to confirm they work
5. **Commit with a clear message**:
   ```bash
   git commit -m "feat: add Kubernetes container orchestration module"
   git commit -m "fix: correct Prometheus config port number"
   ```
6. **Push and create a Pull Request**
7. **Describe your changes** in the PR description

### Commit Message Convention

| Prefix | Use For |
|--------|---------|
| `feat:` | New content, modules, or scripts |
| `fix:` | Corrections, bug fixes in scripts |
| `docs:` | Documentation improvements |
| `refactor:` | Restructuring without content changes |
| `chore:` | Maintenance tasks |

---

## 🐛 Reporting Issues

Use [GitHub Issues](https://github.com/thejas0501/zero-to-sre/issues) with these labels:

| Label | Description |
|-------|-------------|
| `bug` | Something is incorrect or broken |
| `enhancement` | Suggest improvements |
| `new-module` | Request a new topic/module |
| `good-first-issue` | Great for first-time contributors |
| `help-wanted` | Extra attention needed |

---

<p align="center">
  <strong>Thank you for making Zero to SRE better! 🙏</strong>
</p>
