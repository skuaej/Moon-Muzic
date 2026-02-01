FROM nikolaik/python-nodejs:python3.10-nodejs19

WORKDIR /app

# Switch to archive repos for Debian Buster (since it's EOL)
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list \
 && sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list \
 && sed -i '/buster-updates/d' /etc/apt/sources.list \
 && rm -f /etc/apt/sources.list.d/yarn.list \
 && apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --no-install-recommends wget xz-utils \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Static FFmpeg (Modern Version)
RUN wget -q https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    && tar xf ffmpeg-release-amd64-static.tar.xz \
    && mv ffmpeg-*-amd64-static/ffmpeg /usr/local/bin/ \
    && mv ffmpeg-*-amd64-static/ffprobe /usr/local/bin/ \
    && rm -rf ffmpeg-*-amd64-static*

COPY . .

RUN pip3 install --upgrade pip \
 && pip3 install -r requirements.txt

CMD ["python3", "-m", "MoonXMusic"]
