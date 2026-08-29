1.
git start
git verify
initialised and verified the task was done or not
2.
git add A.txt
git commit -m "Commit A.txt"
git verify
need to stage and commit only one file,either A.txt or B.txt,then verify it.
3.
  both files are already staged, so we unstage one and commit only the other.
git restore --staged B.txt
git commit -m "Commit A.txt"
git verify
 4.
  create a .gitignore file to tell Git not to track .exe, .o, .jar files and the libraries folder, then commit it.
nano .gitignore
*.exe
*.o
*.jar
libraries/
git add .gitignore
git commit -m "Add gitignore"
git verify
5.escaped is already at commit C, and chase-branch is at B. So I just moved chase-branch to the same commit as escaped.
git branch -f chase-branch escaped
git verify
6.merged another-piece-of-work into my current branch. This created a merge conflict, so I opened the conflicted file, resolved it manually, and then committed the changes.
git merge another-piece-of-work
git status
nano <conflicted-file>
git add <conflicted-file>
git commit -m "Resolve merge conflict"
git verify
7.I used git stash to temporarily save my unfinished work, fixed the bug in bug.txt, committed the bugfix, then brought back my earlier work and finished it.
git stash
git add bug.txt
git commit -m "Fix bug"
git stash pop
git add bug.txt
git commit -m "Finish work"
git verify
8.I moved the bugfix commit so it comes directly after the starting commit, while keeping my current work after it.
git rebase --onto hot-bugfix B change-branch-history
git verify
9.I removed ignored.txt from Git tracking while keeping the file itself in my folder.
git rm --cached ignored.txt
git verify
10.I renamed File.txt to file.txt and committed the filename change.
git mv File.txt temp.txt
git mv temp.txt file.txt
git commit -m "Rename File.txt to file.txt"
git verify
11.I fixed the typo in file.txt and changed the previous commit to include the correction without creating a new commit.
nano file.txt
git add file.txt
git commit --amend --no-edit
12.I changed the date of the last commit to make it look like the work was committed in 1987.
GIT_COMMITTER_DATE="1987-01-01 12:00:00" git commit --amend --no-edit --date="1987-01-01 12:00:00"
git verify
13.I fixed the typo in an older commit by going back in the commit history,correcting the file, and keeping the original commit message.
git rebase -i HEAD~2
nano file.txt
git add file.txt
git commit --amend --no-edit
git rebase --continue
git verify
14.I used the Git reflog to find the previous version of the amended commit,then moved commit-lost back to that commit.
git reflog
git branch -f commit-lost <old-commit-hash>
git verify
15.I split the previous commit into two commits,keeping first.txt in the first commit and second.txt in the second one.
git reset HEAD~1
git add first.txt
git commit -m "Commit first.txt"
git add second.txt
git commit -m "Commit second.txt"
git verify
16.I checked the last two commits and then combined them into a single commit.
git log -2
git reset --soft HEAD~2
git commit -m "Combine changes"
git verify
17.I added the executable permission to script.sh and committed the permission change.
chmod +x script.sh
git add script.sh
git commit -m "Make script executable"
git verify
18.I split the changes from one file into two commits by interactively staging only the lines containing Task 1 first, then committing the remaining changes separately.
git add -p
git commit -m "Add Task 1"
git add -p
git commit -m "Add remaining tasks"
git verify
19.i had three feature commits on separate branches. i used cherry-pick to bring those commits into my current branch one by one,so all three features were added as separate commits.
git cherry-pick A B C
git verify
20.I needed only the H and I commits from rebase-complex,not the issue-555 commits.I used rebase --onto to take the commits after B and place them directly after your-master (D).
git rebase --onto your-master B rebase-complex
git verify
21.I checked the last two commits and reordered them so the newer change comes before the older one in the history.
git log -2
git rebase -i HEAD~2
git verify
22.I need to find the commits where shit was added, then edit those commits so they contain flower instead. I can use an interactive rebase to go through the affected commits.
git log -S"shit" -- words.txt list.txt
git rebase -i --root
sed -i 's/shit/flower/g' words.txt list.txt
git add words.txt list.txt
git commit --amend --no-edit
git rebase --continue
git verify
23.i used git bisect to search through commits then i decoded the home-screen text and checked whether it contained jackass then git narrowed it down to first commit where the bug appeared
git bisect start
git bisect bad
git bisect good 1.0
sh -c "openssl enc -base64 -A -d < home-screen-text.txt | grep -v jackass"
git bisect good
git bisect bad
git bisect reset
git verify

















