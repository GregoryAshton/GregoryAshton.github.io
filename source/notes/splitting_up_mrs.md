# Splitting up a large Merge Request

It is common when developing a new feature on a branch to end up fixing a
number of bugs or extending functionality elsewhere in the code. After you are
done, however, the code reviewers may well ask that the bug fixes be separated
into a separate merge request. This makes their life easier. They can review
the bug fixes and get these merges into master quickly. Meanwhile, your new
feature may need a more in-depth review. It would not be sensible to hold up
fixing bugs based on the review of new code.

In this note, I'll describe the method I use to break such large merge requests up. Advice on merge requests in general can be found [here](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html).

## Figure out where the changes are

Let's say you are developing on `feature-branch` and want to merge into `main-branch`. First, let's figure out which files have been modified:

```
$ git diff --name-only main-branch feature-branch
src/utils.py
src/magic.py
```

Here we can see that both `utils.py` and `magic.py` have been modified. Let's
say that the changes to `utils.py` where all bug fixes while `magic.py` is a
new file introducing new features. The code reviewers want to split up our
merge request into two: one which only adds the bug fixes to `utils.py` and a
second one which adds the new functionality in `magic.py`.

## The Problem and Solution
The problem, from our perspective, is that the changes to `magic.py` depend on
the changes to `utils.py`! Of course, we fixed the bugs so that it would run.

To satisfy the code reviewers while not breaking our branch, we need to:

1. Create a new merge request with only the changes to `utils.py` included
2. Request the new merge request be merged into master
3. Rebase our `feature-branch` to master (bringing with it the changes to `utils.py`)
4. Now we have a `feature-branch` with only `magic.py` being changed, but all the while `feature-branch` never got broken.

## Technical how-to

The steps above can be done as follows:

**Create a new merge request with only the changes to `utils.py` included**
```
$ (main-branch) git checkout main-branch
$ (main-branch) git checkout -b fix-utils  # Create branch of main-branch
$ (fix-utils) git diff main-branch feature-branch -- src/utils.py > utils_changes.patch  # Write the diff between the main and feature branches to a patch
$ (fix-utils) git apply utils_changes.patch  # Apply the patch
$ (fix-utils) git commit -m "Fixing utils"
```
Now you can push this branch and create a merge request.

Once `fix-utils` gets merged into `main-branch`, all you need to do is rebase your `feature-branch` to `main-branch` and then your merge request will only contain changes to `magic.py`. Magic.
