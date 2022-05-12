FROM nikolaik/python-nodejs:latest




# Create a working directory.
RUN mkdir wd
WORKDIR wd

# Install Python dependencies.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN npm -g config set user root \
 && npm install -g canvas \
 && npm install -g vega vega-lite vega-cli

# Copy the rest of the codebase into the image
COPY . ./





# RUN make

# docker build -t v1.0.0 -f Dockerfile .
# docker run v1.0.0 make