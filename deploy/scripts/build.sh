set -e

path=`dirname $0`
cd $path
pwd
printf "输入 captcha server image tag: "
read captchaServerTag
printf "输入 extractor server image tag: "
read extractorServerTag

if test -z $captchaServerTag
then
  captchaServerTag=v0.0.1
fi

if test -z $extractorServerTag
then
  extractorServerTag=v0.0.1
fi

captchaServerImage=harbor.nadileaf.com/develop/zhaopin-captcha-server:$captchaServerTag
extractorServerImage=harbor.nadileaf.com/develop/zhaopin-extractor-server:$extractorServerTag

echo "开始构建 captchaServerTag: $captchaServerTag extractorServerTag: $extractorServerTag"

docker build -t $captchaServerImage -f ../../src/main/captcha/Dockerfile ../../src/main/captcha

docker build -t $extractorServerImage -f ../../src/main/extractorServer/Dockerfile ../../

docker push $captchaServerImage

docker push $extractorServerImage

echo "成功推送 $extractorServerImage"
echo "成功推送 $captchaServerImage"
