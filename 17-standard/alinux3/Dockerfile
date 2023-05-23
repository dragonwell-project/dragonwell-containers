#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/alinux3:latest

ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

RUN yum install binutils -y tzdata openssl curl ca-certificates fontconfig gzip tar binutils \
    && yum clean all

ENV JAVA_VERSION jdk-17.0.7.0.7+7

RUN set -eux; \
    ARCH="$(objdump="$(command -v objdump)" && objdump --file-headers "$objdump" | awk -F '[:,]+[[:space:]]+' '$1 == "architecture" { print $2 }')"; \
    case "${ARCH}" in \
       aarch64|arm64) \
         ESUM='cc902e52879c37f0f77aafdb00bdbb37ae7cdebf5cf3de883528eb817fea6cc0'; \
         BINARY_URL='https://github.com/dragonwell-project/dragonwell17/releases/download/dragonwell-standard-17.0.7.0.7%2B7_jdk-17.0.7-ga/Alibaba_Dragonwell_Standard_17.0.7.0.7.7_aarch64_linux.tar.gz'; \
         ;; \
       amd64|i386:x86-64) \
         ESUM='190839919ed63f6ba9d1249311610145516e2c457974a418bbd9c74c24dfca54'; \
         BINARY_URL='https://github.com/dragonwell-project/dragonwell17/releases/download/dragonwell-standard-17.0.7.0.7%2B7_jdk-17.0.7-ga/Alibaba_Dragonwell_Standard_17.0.7.0.7.7_x64_linux.tar.gz'; \
         ;; \
       *) \
         echo "Unsupported arch: ${ARCH}"; \
         exit 1; \
         ;; \
    esac; \
    curl -LfsSo /tmp/openjdk.tar.gz ${BINARY_URL}; \
    echo "${ESUM} */tmp/openjdk.tar.gz" | sha256sum -c -; \
    mkdir -p /opt/java/openjdk; \
    cd /opt/java/openjdk; \
    tar -xf /tmp/openjdk.tar.gz --strip-components=1; \
    rm -rf /tmp/openjdk.tar.gz;

ENV JAVA_HOME=/opt/java/openjdk \
    PATH="/opt/java/openjdk/bin:$PATH"

RUN echo Verifying install ... \
    && echo javac --version && javac --version \
    && echo java --version && java --version \
    && echo Complete.

CMD ["jshell"]
