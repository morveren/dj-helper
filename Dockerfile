# base image
FROM python:3.8

# ubuntu installing - python, pip, graphviz, nano, libpq (for psycopg2)
RUN apt-get update &&\
    apt-get install graphviz -y

RUN apt-get install -y ffmpeg

# RUN apt-get install watch -y



# making directory of app
WORKDIR /app




# copy over requirements
COPY requirements.txt ./requirements.txt

# install pip then packages
RUN pip install -r requirements.txt

RUN jupyter contrib nbextension install --user

RUN jupyter nbextension enable contrib_nbextensions_help_item/main & jupyter nbextension enable autosavetime/main & jupyter nbextension enable codefolding/main & jupyter nbextension enable code_font_size/code_font_size & jupyter nbextension enable code_prettify/code_prettify & jupyter nbextension enable collapsible_headings/main & jupyter nbextension enable comment-uncomment/main & jupyter nbextension enable equation-numbering/main & jupyter nbextension enable execute_time/ExecuteTime  & jupyter nbextension enable gist_it/main  & jupyter nbextension enable hide_input/main  & jupyter nbextension enable spellchecker/main & jupyter nbextension enable toc2/main & jupyter nbextension enable toggle_all_line_numbers/main

RUN alias my_notebook='jupyter notebook --port 8930 --allow-root --ip 0.0.0.0'

# ENTRYPOINT []