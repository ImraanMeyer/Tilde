#!/bin/sh

rm -rf core/migrations
rm -rf attendance/migrations
rm -rf curriculum_tracking/migrations
rm -rf git_real/migrations
rm -rf social_auth/migrations
rm -rf config/migrations
# rm -rf dev_helpers/migrations

git checkout master -- core/migrations
git checkout master -- attendance/migrations
git checkout master -- curriculum_tracking/migrations
git checkout master -- git_real/migrations
git checkout master -- social_auth/migrations
git checkout master -- config/migrations
# git checkout master -- dev_helpers/migrations





# rm -rf core/migrations
# rm -rf attendance/migrations
# rm -rf curriculum_tracking/migrations
# rm -rf git_real/migrations
# rm -rf social_auth/migrations
# # rm -rf dev_helpers/migrations

# git checkout develop -- core/migrations
# git checkout develop -- attendance/migrations
# git checkout develop -- curriculum_tracking/migrations
# git checkout develop -- git_real/migrations
# git checkout develop -- social_auth/migrations
# # git checkout master -- dev_helpers/migrations
