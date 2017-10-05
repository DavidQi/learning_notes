# Git Notes

### git 配置文件

* git 配置文件

 针对所有用户：`/etc/gitconfig`

 针对当前用户：` ～/.gitconfig`


* 修改配置
    * 使用命令行
    ```sh
    $ git config --global user.name "test"  (修改的是～/.gitconfig)
    $ git config --system user.name "root"  (修改的是/etc/gitconfig)
    ```
    * 修改配置文件
    ```sh
    $ vim ～/.gitconfig
    [alias]
        co = checkout
        ci = commit
        br = branch
        st = status
        lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
    ```

Git alias command
```sh
$ git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
$ git config --global aliascat.co checkout
$ git config --global alias.ci commit
$ git config --global alias.br branch
$ git config --global alias.unstage 'reset HEAD'
```

### git 远程操作
* git clone
* git remote -- 获取远程仓库信息
  * $ git remote -v
  * $ git remote show <主机名>
  * $ git remote add <主机名> <网址>
  * $ git remote rm <主机名>
  * $ git remote rename <原名> <新名>

* git fetch -- 获取远程仓库的所有更新，但是不自动合并当前分支
* git pull -- 获取远程仓库的所有更新, 并且自动合并到当前分支， 相当于fetch + merge
* git push -- 上传更新（commit）至远程仓库

### git branch strategy
![git strategy](https://media.licdn.com/mpr/mpr/p/6/005/0b5/0b9/3f980f2.jpg)

### git merge vs git rebase
 [详解](https://segmentfault.com/a/1190000005013964)

 * merge 合并操作，会将两个分支的修改合并在一起
 * merge 遇见冲突后会直接停止，等待手动解决冲突并重新提交 commit 后，才能再次 merge
 * rebase 并不进行合并操作，只是提取了当前分支的修改，将其复制在了目标分支的最新提交后面
 * rebase 操作会丢弃当前分支已提交的 commit，故不要在已经 push 到远程，和其他人正在协作开发的分支上执行 rebase 操作
 * rebase 遇见冲突后会暂停当前操作，开发者可以选择手动解决冲突，然后 git rebase --continue 继续，
   或者 --skip 跳过（注意此操作中当前分支的修改会直接覆盖目标分支的冲突部分），亦或者 --abort 直接停止该次 rebase 操作

