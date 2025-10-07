FROM python:3.13.7-alpine
RUN adduser -D application
RUN addgroup running
RUN addgroup application running
RUN pip install uv
WORKDIR /app
COPY pyproject.toml uv.lock .
RUN uv export --format=requirements.txt --all-groups --no-hashes > requirements.txt \
& pip install -r requirements.txt
COPY . .
RUN chgrp -R running ./
RUN chmod -R 070 ./
USER application
CMD ["./run.sh"]