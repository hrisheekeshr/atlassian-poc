# atlassian-poc

#First Run Elasticsearch server
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.9.2

#Install requirements
pip install -r requirements.txt


#Index documents
cd similar_documents
python index_documents.py

#start api server
gunicorn rest_api.application:app -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -t 300