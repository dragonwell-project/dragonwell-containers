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

RUN yum install -y binutils tzdata openssl curl ca-certificates fontconfig gzip tar \
    && yum clean all

ENV JAVA_VERSION jdk8u372-b01

RUN set -eux; \
    ARCH="$(objdump="$(command -v objdump)" && objdump --file-headers "$objdump" | awk -F '[:,]+[[:space:]]+' '$1 == "architecture" { print $2 }')"; \
    case "${ARCH}" in \
       aarch64|arm64) \
         ESUM='42f9f6630eb77c0a273c1952139edb3b87d5f14b6795eceb14f20b03df402c33
Content-Disposition:'; \
         BINARY_URL='https://github.com/dragonwell-project/dragonwell8/releases/download/dragonwell-extended-8.15.16_jdk8u372-ga/Alibaba_Dragonwell_Extended_8.15.16_aarch64_linux.tar.gz'; \
         ;; \
       amd64|i386:x86-64) \
         ESUM='f50a0695cce5cdfea78de4cc369ef1213137fc05ebdfe438be022a3d2cdde05a
Content-Disposition:'; \
         BINARY_URL='https://github.com/dragonwell-project/dragonwell8/releases/download/dragonwell-extended-8.15.16_jdk8u372-ga/Alibaba_Dragonwell_Extended_8.15.16_x64_linux.tar.gz'; \
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
    && echo javac -version && javac -version \
    && echo java -version && java -version \
    && echo Complete.
