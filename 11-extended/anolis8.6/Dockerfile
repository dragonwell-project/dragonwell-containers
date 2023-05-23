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
FROM openanolis/anolisos:8.6

ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en'

RUN yum install -y tzdata openssl curl ca-certificates fontconfig gzip tar \
    && yum clean all

ENV JAVA_VERSION jdk-11.0.19.15+7

RUN set -eux; \
    ARCH="$(objdump="$(command -v objdump)" && objdump --file-headers "$objdump" | awk -F '[:,]+[[:space:]]+' '$1 == "architecture" { print $2 }')"; \
    case "${ARCH}" in \
       aarch64|arm64) \
         ESUM='7bf5187fc7882e3c6a3717ae852f3bc654e6e959d569da170bbfebc280e398b8'; \
         BINARY_URL='https://github.com/dragonwell-project/dragonwell11/releases/download/dragonwell-extended-11.0.19.15_jdk-11.0.19-ga/Alibaba_Dragonwell_Extended_11.0.19.15.7_aarch64_linux.tar.gz'; \
         ;; \
       amd64|i386:x86-64) \
         ESUM='98a113a260ce476c393aebda5d4ec6ef492d0aadcb7f9e8e86d0d899f1d9b2b1'; \
         BINARY_URL='https://github.com/dragonwell-project/dragonwell11/releases/download/dragonwell-extended-11.0.19.15_jdk-11.0.19-ga/Alibaba_Dragonwell_Extended_11.0.19.15.7_x64_linux.tar.gz'; \
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
