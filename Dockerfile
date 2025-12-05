# Use Miniforge as the base image (SV's Choice)
FROM condaforge/mambaforge:latest

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the environment.yml to the container
COPY environment.yml .

# Create conda environment from environment.yml (creates env named 'pcd')
RUN conda env create -f environment.yml

# --- THE FIX STARTS HERE ---
# We must install fpdf2 into the 'pcd' environment because it's likely missing from environment.yml
# We use 'conda run' to ensure it installs INSIDE the pcd environment
RUN conda run -n pcd pip install fpdf2 flask
# --- THE FIX ENDS HERE ---

# Use a bash shell for subsequent RUN/CMD
SHELL ["/bin/bash", "-lc"]

# Copy the entire project into the container
COPY . /usr/src/app

# Expose the port (Your SV used 5000, so we will use 5000)
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app:app
ENV FLASK_ENV=development
ENV PYTHONPATH=/usr/src/app

# Run Flask inside the conda environment named 'pcd' on Port 5000
CMD ["conda", "run", "--no-capture-output", "-n", "pcd", "flask", "run", "--host=0.0.0.0", "--port=5000"]