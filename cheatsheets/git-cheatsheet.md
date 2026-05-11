# 📦 Git Cheatsheet

> Essential Git commands for daily DevOps workflows.

---

## 🔄 Daily Workflow

```bash
git status                               # What's changed?
git diff                                 # Unstaged changes
git diff --staged                        # Staged changes
git add -p                               # Interactive staging (review hunks)
git commit -m "feat: add auth"           # Commit
git push origin feature/auth             # Push to remote
git pull --rebase origin main            # Sync with main (clean history)
```

## 🌿 Branching

```bash
git branch                               # List local branches
git branch -a                            # List all branches (incl. remote)
git checkout -b feature/auth             # Create and switch
git checkout main                        # Switch to main
git branch -d feature/auth              # Delete (merged only)
git branch -D feature/auth              # Force delete
git push origin --delete feature/auth   # Delete remote branch
```

## 🔀 Merging & Rebasing

```bash
git merge feature/auth                   # Merge into current branch
git merge --no-ff feature/auth           # Merge with merge commit
git rebase main                          # Rebase current on main
git rebase -i HEAD~3                     # Interactive rebase (squash, edit, reorder)
git cherry-pick <commit-hash>           # Apply specific commit
```

## ⏪ Undoing Mistakes

```bash
git checkout -- file.txt                 # Discard unstaged changes
git reset HEAD file.txt                  # Unstage a file
git reset --soft HEAD~1                  # Undo last commit (keep changes staged)
git reset --mixed HEAD~1                 # Undo last commit (keep changes unstaged)
git reset --hard HEAD~1                  # ⚠️ Undo last commit (DELETE changes)
git revert <commit>                      # Create a new commit that undoes a commit
git stash                                # Save changes temporarily
git stash pop                            # Restore stashed changes
git stash list                           # List all stashes
git reflog                               # 🆘 Recovery — shows ALL ref changes
```

## 🔍 Investigation

```bash
git log --oneline -20                    # Last 20 commits (compact)
git log --oneline --graph --all          # Visual branch graph
git log --author="name" --since="1 week" # Filter by author/date
git blame file.py                        # Who changed each line?
git show <commit>                        # Show commit details
git diff main..feature/auth              # Compare branches
git bisect start                         # Binary search for bug
```

## 🏷️ Tags

```bash
git tag v1.0.0                           # Lightweight tag
git tag -a v1.0.0 -m "Release 1.0.0"   # Annotated tag
git push origin v1.0.0                   # Push tag
git push origin --tags                   # Push all tags
git tag -d v1.0.0                        # Delete local tag
```

## ⚙️ Configuration

```bash
git config --global user.name "Name"     # Set name
git config --global user.email "e@x.com" # Set email
git config --global core.editor "vim"    # Set editor
git config --global pull.rebase true     # Default pull to rebase
git config --list                        # Show all config
```

## 🧹 Cleanup

```bash
git gc                                   # Garbage collection
git prune                                # Remove unreachable objects
git remote prune origin                  # Remove stale remote branches
git clean -fd                            # Remove untracked files/dirs
```

---

> 💡 **Tips:** Use `git add -p` always (review what you're committing). Set `pull.rebase = true` globally. Install [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens) in VS Code.
