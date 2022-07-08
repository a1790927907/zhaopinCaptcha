# zhaopinCaptcha
用于过智联招聘公司页面滑动验证码

# deploy scripts
1. build.sh 可以推送镜像 可以根据需要填入 image 标签 来推送
    - 推送完毕后需要部署到 k8s yaml文件被我ignore了 别找了 这个是不会传上来的

2. local-deploy.sh 用于本地部署 使用的是 docker-compose

# 本地访问
> 这里就只是本地访问 k8s中请 port-forward 出来再访问 或者用 ingress
>> + 主要服务文档
    - http://localhost:9500/zhaopin/company/docs
