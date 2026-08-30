#EXERCISE 1
```
git start master
```

#EXERCISE 2

The first task was commit one of the two given files in the root project directory. I used “git add A. txt” to add only the required find and then commited it using “git commit -m“commiting””

git add A.txt
git commit -m"commiting"


#EXERCISE 3

The next task was to commit only one file from the two added files. I used “ git commit A. txt -m “commiting only A. txt” “ to commit only one file

git commit A.txt -m"commiting only A.txt"


#EXERCISE 4

exercise 4 helped me learn .gitignore. I had to commit files by ignoring specific files. I first created a .gitignore file and added the file extentions and directory conditions to be excluded by using nano .gitignore. Then i added and commited the file.

nano .gitignore
git add .
git commit -m"commiting"

#EXERCISE 5
Exercise 5 was to merge a branch to an ancestor branch. I used “git merge escaped” to merge chase branch and escaped.

git merge escaped

#TASK 6
Exercise 6 taught me how to resolve merge conflict manually. When i use git merge, it shows merge conflict. I had to manually remove the merge conflic using nano equation.txt. Then i commited the change .

#EXERCISE 7
This task taught me how to use stash in git to temporarily save the current working directory and work on a different task and then using git stash pop to return back to our previous work and saving the other work.

#EXERCISE 8
This task was to rebase a branch into the current branch using git rebase <branch name> . It organizes the commits in a linear order.

#EXERCISE 9
This task was just to remove a file using git rm <filename> from the working directory.

#EXERCISE 10
This task taught me how to rename a file using git mv


#EXERCISE11
This task taught me how to modify the previous commit using git commit — amend

nano file.txt
git add .
git commit --amend

#EXERCISE 12
This task was to change the date of a commit using git commit — amend — no-edit — date”YYYY-MM-DDTHH:MM:SS”.

git commit --amend --no-edit --date="1987-11-12T99:99:99"

#EXERCISE 13
I first used git rebase in interactive mode to modify one of the previous commits it replaced pick to edit for the commit. I changed the typo in file.txt and changed the commit message typo. when i tried to rebase — continue, the file showed a merge conflict. I had to manually resolve the merge conflict and rebase again.

git rebase -i
nano file.txt
git add file.txt
git commit --amend
git reabse --continue          #(==> merge conflict)
nano file.txt
git add .
git commit -m"commiting"
git rebase --continue

#EXERCISE 14
I used git reflog to view the commit history and found the old version of the commit. Then i forced the commit-lost branch to point to it.

git reflog
git reset --hard <commit-hash>


#EXERCISE 15
First is used git reflog to locate the commit hash of the commit. Then is used git reset — soft <> because soft reset undoes the commit but keeps the staged files. Then i commited the files individually.

git reflog
git reset --soft <commit-hash>
git add first.txt
git commit -m"commiting first"
git add second.txt
git commit -m"second commit"


#EXERCISE 16
I used git log -2 to view the last two commits and used git rebase in interactive mode and changed pick to squash to combine the last commit with the previous commit.


git log -2
git rebase -i


#EXERCISE 17
To add execute permission i used chmod +x <filename> and commited the change.Then i was able to execute the file.

chmod +x script.sh
git add .
git commit -m"commiting"
./script.sh


#EXERCISE 18
I used git add -p to open the git add interactive mode.I selected e mode to go to the interactive editor mode. I followed the instructions in the editor and selected only the line i want to be staged for the first commit. Then i made the first commit. I then added and committed the remaining lines.

cat file.txt
git add -p
git commit -m"First commit"
git add -p
got commit -m"second commit"


#EXERCISE 19
First I used git reflog to locate the feature commits. I used git cherry-pick <commit hash> to bring the feature branch commits to the main branch. There was a merge conflict while using cherry-pick on feature. I had to manually fix the merge conflict and add the changes. Then I used git cherry-pick — continue to complete the cherry-pick

git reflog
git cherry-pick <commit hash of feature A>
git cherry-pick <commit hash of feature B>
git cherry-pick <commit hash of feature C>
nano program.txt
git add .
git cherry-pick --continue


#EXERCISE 20
I used git rebase — onto to move the bug fix branch (rebase-complex) from issue-555 to the your-master branch


git rebase --onto your-master issue-555 rebase-complex

#EXERCISE 21
i used git rebase — interactive mode and changed the order of the commits by simply swapping the order of the commits in the editor.

git rebase --interactive



#EXERCISE 22
I first used git log -S ‘shit’ which is known as pickaxe mode to search within the files in the commits for the word. It gives me the log of the commits that contains the word. Then i individually go and edit each file in git rebase interactive mode by changeing pick to edit in the editor. Then I changed the word shit to flower in the files of each commits and added and committed and rebased them.

git log -S "shit"
git rebase -i
nano list.txt
git add .
git commit --amend
git rebase --continue
git rebase -i
nano words.txt
git add .
git commit --amend
git rebase --continue
git rebase -i
nano words.txt
git add .
git commit -amend
git rebase --continu


#EXERCISE 23
I used git bisect start to start the binary search. The Head commit contained jaskass so it was a bad case. I was given that the commit with the tag 1.0 was a good case go i used git bisect good 1.0. Then i used git bisect run sh -c “openssl enc -base64 -A -d < home-screen-text.txt | grep -v jackass” to automatically check if the cases are good or bad. If the home-screen-text.txt contains jackass then grep -v will return 1 and the case will be bad likewise if the file doesnt contatin the word the case will be good. It helped me locate the first bad commit.

git bisect start
git bisect bad HEAD
git bisect good 1.0
git bisect run sh -c "openssl enc -base64 -A -d < home-screen-text.txt | grep -v jackass"
git push origin 5e235e8ca5573dbb8e8bc65dbac9f399ed2f459
