FROM nikolaik/python-nodejs:python3.10-nodejs19

WORKDIR /app

# Fix Debian Buster + remove Yarn repo + install ffmpeg
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list \
 && sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list \
 && sed -i '/buster-updates/d' /etc/apt/sources.list \
 && rm -f /etc/apt/sources.list.d/yarn.list \
 && apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --no-install-recommends ffmpeg \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install --upgrade pip \
 && pip3 install -r requirements.txt

CMD ["python3", "-m", "MoonXMusic"]
