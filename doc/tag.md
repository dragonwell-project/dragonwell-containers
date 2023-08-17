# Dragonwell Container Specification


## Tags
```aidl
${repository}:${version}
${repository}:${version}-${platform}
${repository}:${version}-${type}
```
### repository
| repository | Source |
|------------|--------|
| dragonwell-registry.cn-hangzhou.cr.aliyuncs.com|Alibaba Cloud|

### version/platform
| Version | Architecture  | Platform             |
|---------|---------------|----------------------|
| 8       | amd64,aarch64 | centos,ubuntu,anolis |
| 11      | amd64,aarch64 | alpine,centos,ubuntu |
| 17      | amd64,aarch64 | alpine,centos,ubuntu |

### type
| type   | Explanation |
|-----|-----|
| nightly | Nightly build from master | 

- Example
docker pull dragonwell-registry.cn-hangzhou.cr.aliyuncs.com/dragonwell/dragonwell:11-alpine

