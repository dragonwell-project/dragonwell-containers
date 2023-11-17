# Dragonwell容器规范

## 从openjdk迁移到Dragonwell
- 根据当前的大版本更换到对应的Dragonwell镜像
```
- FROM openjdk:11
+ FROM dragonwell-registry.cn-hangzhou.cr.aliyuncs.com/dragonwell/dragonwell:11
```
## 定制镜像需求
JRE/slim镜像开发中，对于镜像的疑问和需求请[提交此处](https://github.com/dragonwell-releng/dragonwell-containers/issues)


## Tags
```
${repository}:${version}
${repository}:${version}-${platform}
${repository}:${version}-${type}
```

### repository
目前Dragonwell官方维护的镜像将在阿里云容器仓库和Docker官方dockerhub(即将上线)维护。

| repository | Source |
|------------|--------|
| dragonwell-registry.cn-hangzhou.cr.aliyuncs.com|Alibaba Cloud|

### version/platform
不支持的系统/平台镜像无法拉取，同时将centos作为各个发行版本的默认镜像。

如dragonwell:8为基于centos的版本，如果希望使用基于ubuntu的镜像，请使用dragonwell:8-ubuntu。

Dragonwell 11和17针对alpine平台提供了alpine构建，体积更小，目前仅仅支持amd64架构。

| Version | Architecture  | Platform             |
|---------|---------------|----------------------|
| 8       | amd64,aarch64 | centos,ubuntu,anolis,alinux |
| 11      | amd64,aarch64 | alpine,centos,ubuntu,alinux |
| 17      | amd64,aarch64 | alpine,centos,ubuntu,alinux |

#### 小版本支持
- 对于每次的ga发布，保留以github tag命名的发行版本，如期望指定使用release-dragonwell-8.11.12_jdk8u332-ga而非当前最新版：
```
docker pull dragonwell-registry.cn-hangzhou.cr.aliyuncs.com/dragonwell/dragonwell:dragonwell-8.11.12_jdk8u332-ga
docker pull dragonwell-registry.cn-hangzhou.cr.aliyuncs.com/dragonwell/dragonwell:dragonwell-8.11.12_jdk8u332-ga-ubuntu
```


### type
默认类型为每三个月发布一次的正式发布版本, 如dragonwell:8这个tag会一直指向8版本最新的正式发布。
而8-nightly会指向每天晚上从master分支进行的构建产物，用于快速验证和特性尝试。

| type   | Explanation |
|-----|-----|
| nightly | Nightly build from master | 

- 示例
  docker pull dragonwell-registry.cn-hangzhou.cr.aliyuncs.com/dragonwell/dragonwell:11-nightly

