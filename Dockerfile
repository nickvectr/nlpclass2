FROM python:3.6

RUN apt-get update && apt-get install -y \
    vim
RUN mkdir /nlp
WORKDIR /nlp
ADD requirements.txt /nlp
RUN pip install -r requirements.txt
ADD .bashrc /root
ADD .vimrc /root
RUN mkdir -p /root/.vim/colors/
ADD .vim/colors/jellybeans.vim /root/.vim/colors
ADD init_nltk.py /nlp
RUN python init_nltk.py
