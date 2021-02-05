echo "Stopping Elasticsearch Server"
docker rm -f haystack-elastic

echo "Chilling for 5 Seconds"
sleep 5s

echo "Starting Elasticsearch Server"
docker run -d -p 9200:9200 --name haystack-elastic -e "discovery.type=single-node" elasticsearch:7.9.2
echo "Waiting 30 seconds"
sleep 30s

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
gunicorn rest_api.application:app -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -t 300
