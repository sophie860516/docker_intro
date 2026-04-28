# base Docker image that we will build on
FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# set up the working directory inside the container
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages
#Without ENV PATH - use system python -> no dependencies installed, pipeline will fail
# With ENV PATH - uses venv python  
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./


# set up our image by installing prerequisites; pandas in this case
#RUN pip install pandas pyarrow

# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

# copy the script to the container. 1st name is source file, 2nd is destination
COPY pipeline.py .

# define what to do first when the container runs
# in this example, we will just run the script
ENTRYPOINT ["uv", "run", "python", "pipeline.py"]
#Automatically finds and uses the virtual environment from pyproject.toml / uv.lock
#Doesn't require the ENV PATH line (though it won't hurt to have it)
#works even if ENV PATH is modified

#versus
#ENV PATH="/app/.venv/bin:$PATH"
#ENTRYPOINT ["python", "pipeline.py"]