echo "Starting Elasticsearch Server"
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.9.2
echo "Waiting 30 seconds"
sleep 5s

echo "Installing Requirements"
pip install -r requirements.txt
echo "Done"

echo "Indexing Documents"
cd similar_documents
python index_documents.py
echo "Done"

echo "Starting API Server"
cd ..
cd rest_api
gunicorn rest_api.application:app -b 0.0.0.0:80 -k uvicorn.workers.UvicornWorker -t 300
