az login
az acr login --name twharmonyacr
az acr update -n twharmonyacr --admin-enabled true
export COMMIT_ID=`git show -s --format=%ci_%h | sed s/[^_a-z0-9]//g | sed s/0[012]00_/_/g` && docker build -f Dockerfile_tika -t harmonywithtika -t harmonywithtika:latest -t harmonywithtika:$COMMIT_ID -t harmonydata/harmonywithtika:latest -t harmonydata/harmonywithtika:$COMMIT_ID -t twharmonyacr.azurecr.io/harmonywithtika -t twharmonyacr.azurecr.io/harmonywithtika:$COMMIT_ID --build-arg COMMIT_ID=$COMMIT_ID . && docker push twharmonyacr.azurecr.io/harmonywithtika:$COMMIT_ID  && echo "The container version is $COMMIT_ID" && echo "The container version is $COMMIT_ID"
